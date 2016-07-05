#include <Wire.h>
#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <HMC5883L.h>
// Servo library
#include <Servo.h> 
#define SERVO_PIN		9
Servo myservo;

#define BMP085_ADDRESS 0x77  // I2C address of BMP085

const unsigned char OSS = 0;  // Oversampling Setting

// Calibration values
int ac1;
int ac2; 
int ac3; 
unsigned int ac4;
unsigned int ac5;
unsigned int ac6;
int b1; 
int b2;
int mb;
int mc;
int md;

// b5 is calculated in bmp085GetTemperature(...), this variable is also used in bmp085GetPressure(...)
// so ...Temperature(...) must be called before ...Pressure(...).
long b5; 

short temperature;
long pressure;
long pressure_offset;
float maxaltitude = 0;

long lastmillisec;
long mstimer;
float diff_triger_val = 0;

float angles[3]; // yaw pitch roll
float heading;
 
// Set the FreeSixIMU object
FreeSixIMU sixDOF = FreeSixIMU();
 
HMC5883L compass;
// Record any errors that may occur in the compass.
int error = 0;

typedef struct fb1 {
	char arrbyte[4];
}fb;

fb arr_bangles[3];
fb bpressure;

#define CHECK_DEV       	16
#define INIT_DEV        	9

#define CHECK_STATE     	42
#define PARACHUTE_TRIGGER	41
#define TIMER_TRIGGER		40
#define RESET_SW			3
#define DIFF_TRIGER			8

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

bool checktimer(long ms) {
	if ((millis() - lastmillisec) >= ms) {
		lastmillisec = millis();
		return 1;
	}
	return 0;
}

void parachutetrigger() {
	myservo.attach(9);
	myservo.write(15);
}

float getaltitude() {
	return 44330. * (1.0 - pow(float(pressure) /101500.,0.1903));
}

void bytes_pressuredata(long pressure_data, fb *out) {
	out->arrbyte[0] = (uint8_t)(pressure_data & 0x00FF);
	out->arrbyte[1] = (uint8_t)((pressure_data >> 8) & 0x00FF);
	out->arrbyte[2] = (uint8_t)((pressure_data >> 16) & 0x00FF);
	out->arrbyte[3] = (uint8_t)((pressure_data >> 24) & 0x00FF);
}

void bytes_floatdata(float ft, fb *out) {
	int data = (int) ft;
	int dec = (int)((ft - data)*100);
	out->arrbyte[0] = (char)abs(dec);
	out->arrbyte[1] = (char)(abs(data) & 0x00FF);
	out->arrbyte[2] = (ft < 0)? 1: 0;
}

void printDeviceDescription() {
	Serial.write(0xFF);
	Serial.write(CHECK_DEV);
	Serial.write(13);
	Serial.write("BAALES_ROCKET");
}

void sendState() {
	sixDOF.getEuler(angles);
	temperature = bmp085GetTemperature(bmp085ReadUT());
	pressure = bmp085GetPressure(bmp085ReadUP());
	getHeading();
/*
	char arr_bpressure[3];
	bytes_pressuredata(pressure, arr_bpressure);*/

	for (int i = 0; i < 3; i++)
		bytes_floatdata(angles[i], &arr_bangles[i]);
	bytes_pressuredata(pressure, &bpressure);

	Serial.write(0xFF);
	Serial.write(CHECK_STATE);
	Serial.write(13);
	for (int i = 0; i < 3; i++) 
		for (int j = 0; j < 3; j++)
			Serial.write(arr_bangles[i].arrbyte[j]);
	for (int i = 0; i < 4; i++)
		Serial.write((uint8_t)bpressure.arrbyte[i]);
}

void software_Reset() { // Restarts program from beginning but does not reset the peripherals and registers
	asm volatile ("  jmp 0");  
}

void setup(){
 
	Serial.begin(9600);
	Wire.begin();
 
	delay(5);
	sixDOF.init(); //init the Acc and Gyro
	delay(5);
	compass = HMC5883L(); // init HMC5883
	 
	error = compass.SetScale(1.3); // Set the scale of the compass.
	error = compass.SetMeasurementMode(Measurement_Continuous); // Set the measurement mode to Continuous  
	if(error != 0) // If there is an error, print it out.
		Serial.println(compass.GetErrorText(error));
 
	bmp085Calibration(); // init barometric pressure sensor
	//temperature = bmp085GetTemperature(bmp085ReadUT());
	
	lepacket.ready = 0;
	lepacket.intr = 0;
	lepacket.size = 0;
	lepacket.gcount = 0;
}
 
void loop(){
	 
	
	//PrintData();
	 
	//delay(300);

	if (checktimer(mstimer) && mstimer != 0)
		parachutetrigger();

	if ((enflag != 1) || !(lepacket.ready)){ 
		temperature = bmp085GetTemperature(bmp085ReadUT());
		pressure = bmp085GetPressure(bmp085ReadUP());
		float current_altitude = getaltitude();
		if (current_altitude > maxaltitude)
			maxaltitude = current_altitude;
		if (maxaltitude - current_altitude > diff_triger_val && diff_triger_val != 0){
			parachutetrigger();
		}
		return;
	}

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
		case PARACHUTE_TRIGGER:
			RESET_SW			3
				parachutetrigger();
			break;
		case TIMER_TRIGGER:
			if (tmppacket.param[0] != 0)
				mstimer = (int)tmppacket.param[0] * 1000;
				lastmillisec = millis();
			break;
		case RESET_SW:
			if (tmppacket.param[0] == RESET_SW)
				software_Reset();
			break;
		case DIFF_TRIGER:
			if (tmppacket.param[0] != 0 || tmppacket.param[1] != 0)
			diff_triger_val = float(tmppacket.param[1]) + float(tmppacket.param[0])/10;
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
		// Serial.println(input);
	}
} 
// ---------------------------------------------------------------------------------------------------------------
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
 
void PrintData(){
	sixDOF.getEuler(angles);
	 
	temperature = bmp085GetTemperature(bmp085ReadUT());
	pressure = bmp085GetPressure(bmp085ReadUP());
 	float current_altitude = getaltitude();

	getHeading();

	/*bytes_pressuredata(pressure, &bpressure);
	Serial.print("Pressure arr values: ");
	for (int i = 0; i < 4; i++) {
		Serial.print((uint8_t)bpressure.arrbyte[i], DEC);
		Serial.print("  ");
	}*/

	Serial.println("  ");
	Serial.print("Eular Angle: ");
	Serial.print(angles[0]);
	Serial.print("  ");  
	Serial.print(angles[1]);
	Serial.print("  ");
	Serial.print(angles[2]);
	Serial.print("  ");
	Serial.print("Heading: ");
	Serial.print(heading);
	Serial.print("  ");
	Serial.print("Altitude: ");
	Serial.print(current_altitude);
	Serial.print("  ");
	Serial.print("Max Altitude: ");
	Serial.print(maxaltitude);
	Serial.print("  ");
	Serial.print("Pressure: ");
	Serial.print(pressure, DEC);
	Serial.println(" Pa");
	 
}

// ---------------------------------------------------------------------------------------------------------------
// Stores all of the bmp085's calibration values into global variables
// Calibration values are required to calculate temp and pressure
// This function should be called at the beginning of the program
void bmp085Calibration()
{
	ac1 = bmp085ReadInt(0xAA);
	ac2 = bmp085ReadInt(0xAC);
	ac3 = bmp085ReadInt(0xAE);
	ac4 = bmp085ReadInt(0xB0);
	ac5 = bmp085ReadInt(0xB2);
	ac6 = bmp085ReadInt(0xB4);
	b1 = bmp085ReadInt(0xB6);
	b2 = bmp085ReadInt(0xB8);
	mb = bmp085ReadInt(0xBA);
	mc = bmp085ReadInt(0xBC);
	md = bmp085ReadInt(0xBE);
}

// Calculate temperature given ut.
// Value returned will be in units of 0.1 deg C
short bmp085GetTemperature(unsigned int ut)
{
	long x1, x2;
	
	x1 = (((long)ut - (long)ac6)*(long)ac5) >> 15;
	x2 = ((long)mc << 11)/(x1 + md);
	b5 = x1 + x2;

	return ((b5 + 8)>>4);  
}

// Calculate pressure given up
// calibration values must be known
// b5 is also required so bmp085GetTemperature(...) must be called first.
// Value returned will be pressure in units of Pa.
long bmp085GetPressure(unsigned long up)
{
	long x1, x2, x3, b3, b6, p;
	unsigned long b4, b7;
	
	b6 = b5 - 4000;
	// Calculate B3
	x1 = (b2 * (b6 * b6)>>12)>>11;
	x2 = (ac2 * b6)>>11;
	x3 = x1 + x2;
	b3 = (((((long)ac1)*4 + x3)<<OSS) + 2)>>2;
	
	// Calculate B4
	x1 = (ac3 * b6)>>13;
	x2 = (b1 * ((b6 * b6)>>12))>>16;
	x3 = ((x1 + x2) + 2)>>2;
	b4 = (ac4 * (unsigned long)(x3 + 32768))>>15;
	
	b7 = ((unsigned long)(up - b3) * (50000>>OSS));
	if (b7 < 0x80000000)
		p = (b7<<1)/b4;
	else
		p = (b7/b4)<<1;
		
	x1 = (p>>8) * (p>>8);
	x1 = (x1 * 3038)>>16;
	x2 = (-7357 * p)>>16;
	p += (x1 + x2 + 3791)>>4;
	
	return p;
}

// Read 1 byte from the BMP085 at 'address'
char bmp085Read(unsigned char address)
{
	unsigned char data;
	
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(address);
	Wire.endTransmission();
	
	Wire.requestFrom(BMP085_ADDRESS, 1);
	while(!Wire.available())
		;
		
	return Wire.read();
}

// Read 2 bytes from the BMP085
// First byte will be from 'address'
// Second byte will be from 'address'+1
int bmp085ReadInt(unsigned char address)
{
	unsigned char msb, lsb;
	
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(address);
	Wire.endTransmission();
	
	Wire.requestFrom(BMP085_ADDRESS, 2);
	while(Wire.available()<2)
		;
	msb = Wire.read();
	lsb = Wire.read();
	
	return (int) msb<<8 | lsb;
}

// Read the uncompensated temperature value
unsigned int bmp085ReadUT()
{
	unsigned int ut;
	
	// Write 0x2E into Register 0xF4
	// This requests a temperature reading
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF4);
	Wire.write(0x2E);
	Wire.endTransmission();
	
	// Wait at least 4.5ms
	delay(5);
	
	// Read two bytes from registers 0xF6 and 0xF7
	ut = bmp085ReadInt(0xF6);
	return ut;
}

// Read the uncompensated pressure value
unsigned long bmp085ReadUP()
{
	unsigned char msb, lsb, xlsb;
	unsigned long up = 0;
	
	// Write 0x34+(OSS<<6) into register 0xF4
	// Request a pressure reading w/ oversampling setting
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF4);
	Wire.write(0x34 + (OSS<<6));
	Wire.endTransmission();
	
	// Wait for conversion, delay time dependent on OSS
	delay(2 + (3<<OSS));
	
	// Read register 0xF6 (MSB), 0xF7 (LSB), and 0xF8 (XLSB)
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF6);
	Wire.endTransmission();
	Wire.requestFrom(BMP085_ADDRESS, 3);
	
	// Wait for data to become available
	while(Wire.available() < 3)
		;
	msb = Wire.read();
	lsb = Wire.read();
	xlsb = Wire.read();
	
	up = (((unsigned long) msb << 16) | ((unsigned long) lsb << 8) | (unsigned long) xlsb) >> (8-OSS);
	
	return up;
}


