
#include <Wire.h>
#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <HMC5883L.h>

#define CHECK_DEV       16
#define INIT_DEV        9

#define CHECK_STATE     42

typedef struct minipkt {
	int size; // bytes of parameters
	int gcount; // counter rx parameters
	int param[99]; // array of parameters
	int intr ; // instruction
	int ready; // packet status
	}packet;

int enflag = 0; // enable flag from recieving packet
packet lepacket;

char NOMBRE[10]  = "brocket";    
char BPS = '0';
char PASS[10]    = "0000";   

// Set the FreeSixIMU object
FreeSixIMU sixDOF = FreeSixIMU();
float angles[3]; // yaw pitch roll
HMC5883L compass;
float heading;
// Record any errors
int error = 0;

void BTconfig() {
	Serial.begin(115200);
	Serial.print("AT"); 
	delay(1000);
	Serial.print("AT+RENEW");
	delay(1000);
	Serial.print("AT+NAME"); 
	Serial.print(NOMBRE);
	delay(1000);
	//Serial.print("AT+BAUD"); 
	//Serial.print(BPS); 
	//delay(1000);
	Serial.print("AT+AUTH1");
	delay(1000);
	Serial.print("AT+PINE");
	Serial.print(PASS); 
	delay(1000);
	//Serial.print("AT+ROLB0");
	//delay(1000);
	//Serial.print("AT+MODE0");
	//delay(1000);
	//Serial.print("AT+SAVE1");
	//delay(1000);
}

char* bytes_presuredata(float presure_data) {
	char arrdata[3];
	long int data = (long int)(presure_data - presure_data%1)
	arrdata[0] = (char)(data & 0x000000FF);
	arrdata[1] = (char)((data & 0x0000FF00) >> 8);
	arrdata[2] = (char)((data & 0x00FF0000) >> 2*8);
	return arrdata;
}

char* bytes_floatdata(float ft) {
	char arrdata[2];
	int data = (int) ft;
	arrdata[0] = (char)(data & 0x00EF);
	arrdata[0] = (ft < 0)? arrdata[0] + 0x80: arrdata[0];
	arrdata[1] = (char)((int) (ft%1)*100);
	return arrdata;
}

void printDeviceDescription() {
	Serial.write(0xFF);
	Serial.write(CHECK_DEV);
	Serial.write(13);
	Serial.write("BAALES_ROCKET");
}

void sendState() {
	sixDOF.getEuler(angles);
	pressure = bmp085GetPressure(bmp085ReadUP());
	getHeading();
	char arr_bangles[3][2];
	for (int i = 0; i < 3; i++)
		arr_bangles[i] = bytes_floatdata(angles[i]);
	char arr_bpresure[3] = bytes_presuredata(presure);

	Serial.write(0xFF);
	Serial.write(CHECK_STATE);
	Serial.write(9);
	for (int i= 0; i < 3; i++) {
		Serial.write(arr_bangles[i][0]);
		Serial.write(arr_bangles[i][0]);
	}
	for (int i = 0; i < 3; i++)
		Serial.write(arr_bpresure[i]);
}

void software_Reset() { // Restarts program from beginning but does not reset the peripherals and registers
	asm volatile ("  jmp 0");  
}

void setup() {
	Serial.begin(115200);
	//BTconfig();
	Wire.begin();
 
	delay(5);
	sixDOF.init(); //init the Acc and Gyro
	delay(5);
	compass = HMC5883L(); // init HMC5883

	error = compass.SetScale(1.3); // Set the scale of the compass.
	error = compass.SetMeasurementMode(Measurement_Continuous); // Set the measurement mode to Continuous  
	if(error != 0) software_Reset(); // If there is an error, print it out.

	bmp085Calibration(); // init barometric pressure sensor

	lepacket.ready = 0;
	lepacket.intr = 0;
	lepacket.size = 0;
	lepacket.gcount = 0;
}

void loop() {

	//buttons.reportButtons();
	if ((enflag != 1) || !(lepacket.ready)) return;

	packet tmppacket = lepacket;
	int aux1 = 0;

	enflag = 0;
	lepacket.ready = 0;
	lepacket.intr = 0;
	lepacket.size = 0;
	lepacket.gcount = 0;

	int n_sucks = tmppacket.size;

	switch(tmppacket.intr){
		case INIT_DEV:
			//Serial.write(0);
			break;
		case CHECK_DEV:
			if (tmppacket.param[0] == CHECK_DEV)
				printDeviceDescription();
			break; 
		case CHECK_STATE:
			if (tmppacket.param[0] == CHECK_STATE)
				sendState();
			break;
		}
}

void serialEvent() {
	int input = 0; // temporally variable for serial cache
	while (Serial.available()) {
		input = (int)Serial.read();
		// while recieving bytes, keeps in packet's structure
		if ((input == 255) && (enflag == 0)) {
			enflag = 1;
		} else if ((enflag == 1) && (lepacket.intr == 0)) {
			lepacket.intr = input;
		} else if ((enflag == 1) && (lepacket.size == 0)) {
			lepacket.size = input;
		} else if ((enflag == 1) && (lepacket.size > 0) && (lepacket.size != lepacket.gcount)) {
			lepacket.param[lepacket.gcount++] = input;
			if(lepacket.size == lepacket.gcount){
				lepacket.ready = 1;
			}
		}
		//Serial.println(input);
	}
} 

void getHeading(){
	// Retrive the raw values from the compass (not scaled).
	MagnetometerRaw raw = compass.ReadRawAxis();
	// Retrived the scaled values from the compass (scaled to the configured scale).
	MagnetometerScaled scaled = compass.ReadScaledAxis();

	// Values are accessed like so:
	int MilliGauss_OnThe_XAxis = scaled.XAxis;// (or YAxis, or ZAxis)

	// Calculate heading when the magnetometer is level, then correct for signs of axis.
	heading = atan2(scaled.YAxis, scaled.XAxis);  

	float declinationAngle = 0.0457;
	heading += declinationAngle;

	// Correct for when signs are reversed.
	if(heading < 0)
		heading += 2*PI;
	 
	// Check for wrap due to addition of declination.
	if(heading > 2*PI)
		heading -= 2*PI;

	// Convert radians to degrees for readability.
	heading = heading * 180/M_PI; 
}