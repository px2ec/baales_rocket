import moddev
import modcom
#import struct

CHECK_STATE = 42

class bRocketDev(moddev.ModDev):
	
	# "Public" variables for class
	ErrorFlag = False # Error flag for any device error

	# acX = 0
	# acY = 0
	# acZ = 0
	tX = 0
	tY = 0
	abstX = 0
	abstY = 0
	buttonI = 0
	buttonD = 0
	buttonTgl = 0

	def __init__(self):
		super(bRocketDev, self).__init__()

	def getState(self):
		lst = [0xFF, CHECK_STATE, 1, CHECK_STATE]
		lread = self._mc.Comunicate(lst, True)
		#print lread
		if lread:
			if lread[1] != CHECK_STATE :
				self.ErrorFlag = True
				return
			# self.acX = struct.unpack( "h", chr(lread[4]) + chr(lread[3]))[0]
			# self.acY = struct.unpack( "h", chr(lread[6]) + chr(lread[5]))[0]
			# self.acZ = struct.unpack( "h", chr(lread[8]) + chr(lread[7]))[0]
			# if (lread[4] >> 7) == 1:
			# 	self.acX = (((~lread[4] & 0x7F) << 8) | ~lread[3])
			# else:
			# 	self.acX = ((lread[4] & 0x7F) << 8) | lread[3]
			# if (lread[6] >> 7) == 1:
			# 	self.acY = (((~lread[6] & 0x7F) << 8) | ~lread[5])
			# else:
			# 	self.acY = ((lread[6] & 0x7F) << 8) | lread[5]
			# if (lread[8] >> 7) == 1:
			# 	self.acZ = (((~lread[8] & 0x7F) << 8) | ~lread[7])
			# else:
			# 	self.acZ = ((lread[8] & 0x7F) << 8) | lread[7]
			# self.buttonI = lread[10]
			# self.buttonD = lread[9]
			# self.buttonTgl = lread[11]
			sign = lread[3]
			#print lread[4], lread[5]
			self.abstX = lread[4]
			self.abstY = lread[5]
			value = sign
			result = {
			0: (lread[4], lread[5]),
			1: (-lread[4], lread[5]),
			2: (lread[4], -lread[5]),
			3: (-lread[4], -lread[5])
			}
			self.tX, self.tY = result[sign]
			#print self.tX, self.tY
			self.buttonI = lread[7]
			self.buttonD = lread[6]
			self.buttonTgl = lread[8]
			return
		self.ErrorFlag = True