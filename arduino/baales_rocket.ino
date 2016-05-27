
char NOMBRE[10]  = "MODDEVBT_";    
char BPS         = '4';           // 1=1200 , 2=2400, 3=4800, 4=9600, 5=19200, 6=38400, 7=57600, 8=115200
char PASS[10]    = "0000";   

// Version 1.0 by Pedro Espinoza

// Tipo de instrucciones
// #define ENABLE_INTR      48
// #define DISABLE_INTR 56
// //--
// #define ENABLE_ALL       44
// #define DISABLE_ALL      52

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

int act_state = 0;
int enflag = 0; // enable flag from recieving packet

// working packet
packet lepacket;

//#include "libButtons.h"

//int buttonPins[3] = {16, 17, 15};     // the number of the pushbutton pin
//libButtons buttons(buttonPins, 3);

#include <Butter.h>

#include <Wire.h>
#include <ADXL345.h>
#include <L3G.h>
#include <SFE_BMP180.h>

#define betaDef  2.0f
#define nsamples 75

ADXL345 acc;
L3G gyro;

SFE_BMP180 pressure;
double baseline; // baseline pressure

butter10hz0_3 mfilter_accx;
butter10hz0_3 mfilter_accy;
butter10hz0_3 mfilter_accz;

float q0, q1, q2, q3;
float SEq_1 = 1, SEq_2 = 0, SEq_3 = 0, SEq_4 = 0;
float beta;
float gyro_sensitivity, gyro_off_x = 0, gyro_off_y = 0, gyro_off_z = 0;
float sampleFreq; // half the sample period expressed in seconds
unsigned long lastUpdate, now;

// Quaternions ----------------------------------------------------------------------------------------------------------------------------------
void MARGUpdateFilterIMU(float w_x, float w_y, float w_z, float a_x, float a_y, float a_z) {
	// Local system variables
	float norm; // vector norm
	float SEqDot_omega_1, SEqDot_omega_2, SEqDot_omega_3, SEqDot_omega_4; // quaternion derrivative from gyroscopes elements
	float f_1, f_2, f_3; // objective function elements
	float J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33; // objective function Jacobian elements
	float SEqHatDot_1, SEqHatDot_2, SEqHatDot_3, SEqHatDot_4; // estimated direction of the gyroscope error

	// Axulirary variables to avoid reapeated calcualtions
	float halfSEq_1 = 0.5f * SEq_1;
	float halfSEq_2 = 0.5f * SEq_2;
	float halfSEq_3 = 0.5f * SEq_3;
	float halfSEq_4 = 0.5f * SEq_4;
	float twoSEq_1 = 2.0f * SEq_1;
	float twoSEq_2 = 2.0f * SEq_2;
	float twoSEq_3 = 2.0f * SEq_3;

	float deltat = 1/sampleFreq;
	
	// Normalise the accelerometer measurement
	norm = sqrt(a_x * a_x + a_y * a_y + a_z * a_z);
	a_x /= norm;
	a_y /= norm;
	a_z /= norm;

	// Compute the objective function and Jacobian
	f_1 = twoSEq_2 * SEq_4 - twoSEq_1 * SEq_3 - a_x;
	f_2 = twoSEq_1 * SEq_2 + twoSEq_3 * SEq_4 - a_y;
	f_3 = 1.0f - twoSEq_2 * SEq_2 - twoSEq_3 * SEq_3 - a_z;
	J_11or24 = twoSEq_3; // J_11 negated in matrix multiplication
	J_12or23 = 2.0f * SEq_4;
	J_13or22 = twoSEq_1; // J_12 negated in matrix multiplication
	J_14or21 = twoSEq_2;
	J_32 = 2.0f * J_14or21; // negated in matrix multiplication
	J_33 = 2.0f * J_11or24; // negated in matrix multiplication

	// Compute the gradient (matrix multiplication)
	SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1;
	SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3;
	SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1;
	SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2;
	
	// Normalise the gradient
	norm = sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4);
	SEqHatDot_1 /= norm;
	SEqHatDot_2 /= norm;
	SEqHatDot_3 /= norm;
	SEqHatDot_4 /= norm;
	
	// Compute the quaternion derrivative measured by gyroscopes
	SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z;
	SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y;
	SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x;
	SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x;

	// Compute then integrate the estimated quaternion derrivative
	SEq_1 += (SEqDot_omega_1 - (beta * SEqHatDot_1)) * deltat;
	SEq_2 += (SEqDot_omega_2 - (beta * SEqHatDot_2)) * deltat;
	SEq_3 += (SEqDot_omega_3 - (beta * SEqHatDot_3)) * deltat;
	SEq_4 += (SEqDot_omega_4 - (beta * SEqHatDot_4)) * deltat;

	// Normalise quaternion
	norm = sqrt(SEq_1 * SEq_1 + SEq_2 * SEq_2 + SEq_3 * SEq_3 + SEq_4 * SEq_4);
	SEq_1 /= norm;
	SEq_2 /= norm;
	SEq_3 /= norm;
	SEq_4 /= norm;
	
	q0 = SEq_1;
	q1 = SEq_2;
	q2 = SEq_3;
	q3 = SEq_4;
}

void getValues(float * values) {
	// int sensor_sign[9] = {-1, -1, -1, 1, 1, 1, 1, 1, 1};
	// int sensor_order[9] = {0, 1, 2, 3, 4, 5, 6, 7, 8};
	int sensor_sign[9] = {-1, -1, 1, 1, 1, -1, 1, 1, 1};
	int sensor_order[9] = {1, 0, 2, 4, 3, 5, 6, 7, 8};
	float values_cal[9] = {0.,0.,0.,0.,0.,0.,0.,0.,0.};
	int accval[3];
    acc.readAccel(&accval[0], &accval[1], &accval[2]);
	accval[0] = mfilter_accx.filter((float) accval[0]);
    accval[1] = mfilter_accy.filter((float) accval[1]);
    accval[2] = mfilter_accz.filter((float) accval[2]);
    values_cal[0] = (float) accval[0];
	values_cal[1] = (float) accval[1];
	values_cal[2] = (float) accval[2];
	gyro.read();
	values_cal[3] = (float) gyro.g.x;
	values_cal[4] = (float) gyro.g.y;
	values_cal[5] = (float) gyro.g.z;
	// values_cal[0] = (values_cal[0] - acc_off_x) / acc_scale_x;
	// values_cal[1] = (values_cal[1] - acc_off_y) / acc_scale_y;
	// values_cal[2] = (values_cal[2] - acc_off_z) / acc_scale_z;
	values_cal[3] = (values_cal[3] - gyro_off_x) / gyro_sensitivity;  //Sensitivity set at 70 for +/-2000 deg/sec, L3GD20H
	values_cal[4] = (values_cal[4] - gyro_off_y) / gyro_sensitivity;
	values_cal[5] = (values_cal[5] - gyro_off_z) / gyro_sensitivity;
	for(int i = 0; i < 9; i++) {
		values[i] = sensor_sign[i] * values_cal[sensor_order[i]];
	}
}

void getQ (float * q, float * val) {
	now = micros();
	sampleFreq = 1.0 / ((now - lastUpdate) / 1000000.0);
	lastUpdate = now;
	getValues(val);
	MARGUpdateFilterIMU(val[3] * M_PI/180, val[4] * M_PI/180, val[5] * M_PI/180, val[0], val[1], val[2]);
	q[0] = q0;
	q[1] = q1;
	q[2] = q2;
	q[3] = q3;
}
// ----------------------------------------------------------------------------------------------------------------------------------------------


// Yaw, pitch and roll --------------------------------------------------------------------------------------------------------------------------
void getYawPitchRollRad(float * ypr) {
	float q[4]; // quaternion
	float val[11];
	float gx, gy, gz; // estimated gravity direction
	getQ(q, val);

	gx = 2 * (q[1]*q[3] - q[0]*q[2]);
	gy = 2 * (q[0]*q[1] + q[2]*q[3]);
	gz = q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3];

	ypr[0] = atan2(2 * q[1] * q[2] - 2 * q[0] * q[3], 2 * q[0]*q[0] + 2 * q[1] * q[1] - 1);
	ypr[1] = atan(gx / sqrt(gy*gy + gz*gz));
	ypr[2] = atan(gy / sqrt(gx*gx + gz*gz));
}

void arr3_rad_to_deg(float * arr) {
	arr[0] *= 180/M_PI;
	arr[1] *= 180/M_PI;
	arr[2] *= 180/M_PI;
}

void getYawPitchRoll(float * ypr) {
	getYawPitchRollRad(ypr);
	arr3_rad_to_deg(ypr);
}
// ----------------------------------------------------------------------------------------------------------------------------------------------


// Altitude -------------------------------------------------------------------------------------------------------------------------------------
double getPressure() {
	char status;
	double T,P,p0,a;

	// You must first get a temperature measurement to perform a pressure reading.
	
	// Start a temperature measurement:
	// If request is successful, the number of ms to wait is returned.
	// If request is unsuccessful, 0 is returned.

	status = pressure.startTemperature();
	if (status != 0) {
		// Wait for the measurement to complete:

		delay(status);

		// Retrieve the completed temperature measurement:
		// Note that the measurement is stored in the variable T.
		// Use '&T' to provide the address of T to the function.
		// Function returns 1 if successful, 0 if failure.

		status = pressure.getTemperature(T);
		if (status != 0) {
			// Start a pressure measurement:
			// The parameter is the oversampling setting, from 0 to 3 (highest res, longest wait).
			// If request is successful, the number of ms to wait is returned.
			// If request is unsuccessful, 0 is returned.

			status = pressure.startPressure(3);
			if (status != 0) {
				// Wait for the measurement to complete:
				delay(status);

				// Retrieve the completed pressure measurement:
				// Note that the measurement is stored in the variable P.
				// Use '&P' to provide the address of P.
				// Note also that the function requires the previous temperature measurement (T).
				// (If temperature is stable, you can do one temperature measurement for a number of pressure measurements.)
				// Function returns 1 if successful, 0 if failure.

				status = pressure.getPressure(P,T);
				if (status != 0) {
					return(P);
				}
				else Serial.println("error retrieving pressure measurement\n");
			}
			else Serial.println("error starting pressure measurement\n");
		}
		else Serial.println("error retrieving temperature measurement\n");
	}
	else Serial.println("error starting temperature measurement\n");
}
// ----------------------------------------------------------------------------------------------------------------------------------------------


// Initializarions ------------------------------------------------------------------------------------------------------------------------------
void init_all() {
	gyro.init();
	gyro.enableDefault();
	//					Sensitivity
	//+/-245:        0x00	8.75	
	//+/-500:        0x10	17.5
	//+/- 2000:      0x20	70
	gyro.writeReg(0x23, 0x20);
	gyro_sensitivity = 70.0f;
	beta = betaDef;
	delay(5);

	acc.init(ADXL345_ADDR_ALT_LOW);
	acc.set_bw(ADXL345_BW_100);
	acc.setRangeSetting(2);
	delay(5);

	pressure.begin()
    baseline = getPressure();
}

void software_Reset() { // Restarts program from beginning but does not reset the peripherals and registers
	asm volatile ("  jmp 0");  
}
// ----------------------------------------------------------------------------------------------------------------------------------------------


// Serial, Bluetooth and PC ---------------------------------------------------------------------------------------------------------------------
void printDeviceDescription() {
	Serial.write(0xFF);
	Serial.write(CHECK_DEV);
	Serial.write(13);
	Serial.write("BAALES_ROCKET");
}

void sendState() {
	float ypr[3];
	getYawPitchRoll(ypr);
	if (isnan(q0) || isnan(q1) || isnan(q2) || isnan(q3)) software_Reset();
	int x = map(ypr[1], -90, 90, -255, 255);
	int y = map(ypr[2], -90, 90, -255, 255);
	int sign = (x < 0 && y < 0)? 3: (y < 0 && x >= 0)? 2 : (y >= 0 && x < 0)? 1 : 0;
	int absx = abs(x);
	int absy = abs(y);
	double a,P;
	// Get a new pressure reading:
	P = getPressure();
	// Show the relative altitude difference between
	// the new reading and the baseline reading:
	a = pressure.altitude(P,baseline);
	buttons.reportButtons();
	Serial.write(0xFF);
	Serial.write(CHECK_STATE);
	Serial.write(4);
	Serial.write(sign);
	Serial.write(absx);
	Serial.write(absy);
	Serial.write(a);

}
// ----------------------------------------------------------------------------------------------------------------------------------------------


// Arduino setup and loop -----------------------------------------------------------------------------------------------------------------------
void setup() {
	Wire.begin();        // join i2c bus (address optional for master)
	// initialize the serial communication:
	delay(5);
	init_all();
	Serial.begin(9600);

	float ypr[3];
	lastUpdate = micros();
	getYawPitchRoll(ypr);
	if (isnan(q0) || isnan(q1) || isnan(q2) || isnan(q3)) software_Reset();

	Serial.print("AT"); 
	delay(1000);
 
	Serial.print("AT+NAME"); 
	Serial.print(NOMBRE);
	delay(1000);
 
	Serial.print("AT+BAUD"); 
	Serial.print(BPS); 
	delay(1000);
 
	Serial.print("AT+PIN");
	Serial.print(PASS); 
	delay(1000);   

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
				// readAccel();
				sendState();
			break;
		// case ENABLE_ALL: // activar todos

		//  }

		//  break;
		// case DISABLE_ALL: // desactivar todos

		//  break; 
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
// ----------------------------------------------------------------------------------------------------------------------------------------------