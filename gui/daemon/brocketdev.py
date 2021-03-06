import moddev
import modcom
#import struct

PARACHUTE_TRIGGER = 41
CHECK_STATE = 42
TIMER_TRIGGER = 40
RESET_SW = 3
DIFF_TRIGER = 8

class bRocketDev(moddev.ModDev):
	
	# "Public" variables for class
	ErrorFlag = False # Error flag for any device error
	yaw = 0;
	pitch = 0;
	roll = 0;
	sealevelPressure = 101325
	fst_refresh = False

	pressure = 0;
	_p0 = 0;

	def __init__(self):
		super(bRocketDev, self).__init__()

	def getAltitude(self, pressure_offset = sealevelPressure):
		if not pressure_offset:
			pressure_offset = self.sealevelPressure
		return 44330 * (1.0 - pow(float(self.pressure) / float(pressure_offset),1./5.255));

	def parachuteTrigger(self):
		lst = [0xFF, PARACHUTE_TRIGGER, 1, PARACHUTE_TRIGGER]
		lread = self._mc.Comunicate(lst, True)

	def resetDevice(self):
		lst = [0xFF, RESET_SW, 1, RESET_SW]
		lread = self._mc.Comunicate(lst, True)

	def timerTrigger(self, time):
		lst = [0xFF, TIMER_TRIGGER, 1, (time & 0xFF)]
		lread = self._mc.Comunicate(lst, True)

	def diffTrigger(self, integer, decimal):
		lst = [0xFF, DIFF_TRIGER, 2, (integer & 0xFF), (decimal & 0xFF)]
		lread = self._mc.Comunicate(lst, True)

	def getState(self):
		lst = [0xFF, CHECK_STATE, 1, CHECK_STATE]
		lread = self._mc.Comunicate(lst, True)
		#print lread
		if lread:
			if lread[1] != CHECK_STATE :
				self.ErrorFlag = True
				return
			yawt = lread[4] + (lread[3] / 100.)
			if lread[5]:
				self.yaw = -yawt
			else:
				self.yaw = yawt

			pitcht = lread[7] + (lread[6] / 100.)
			if lread[8]:
				self.pitch = -pitcht
			else:
				self.pitch = pitcht
			
			rollt = lread[10] + (lread[9] / 100.)
			if lread[11]:
				self.roll = -rollt
			else:
				self.roll = rollt;

			#self.pressure = (lread[12] + lread[13] * 256) * 8 + lread[14]
			self.pressure = lread[12] + ((lread[13]) * 256) + (lread[14] * (2 ** 16)) + (lread[15] * (2 ** 24))
			if not self.fst_refresh:
				self._p0 = self.pressure
				self.fst_refresh = True

			return
		self.ErrorFlag = True