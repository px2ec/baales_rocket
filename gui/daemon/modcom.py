
from time import sleep
import serial
import serial.tools.list_ports
import sys
import glob

CHECK_DEV = 16
INIT_DEV = 9

blacklist = []

if sys.platform == "linux2":
	blacklist = ['/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6', '/dev/ttyS7', '/dev/ttyS8', '/dev/ttyS9', '/dev/ttyS10', '/dev/ttyS11', '/dev/ttyS12', '/dev/ttyS13', '/dev/ttyS14', '/dev/ttyS15', '/dev/ttyS16', '/dev/ttyS17', '/dev/ttyS18', '/dev/ttyS19', '/dev/ttyS20', '/dev/ttyS21', '/dev/ttyS22', '/dev/ttyS23', '/dev/ttyS24', '/dev/ttyS25', '/dev/ttyS26', '/dev/ttyS27', '/dev/ttyS28', '/dev/ttyS29', '/dev/ttyS30', '/dev/ttyS31']

def serial_list_ports_patch():
	"""Lists serial ports

	:raises EnvironmentError:
		On unsupported or unknown platforms
	:returns:
		A list of available serial ports
	"""
	if sys.platform.startswith('win'):
		ports = ['COM' + str(i + 1) for i in range(256)]

	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this is to exclude your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')

	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')

	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append((port, port))
		except (OSError, serial.SerialException):
			pass
	return result

class ModCom:
	# "Private" variables for instance
	__lps = [] # Global list keeps file descriptor from devices connected

	# "Private" variables for class
	_ser = serial.Serial()
	_fd = -1
	_assigned = False
	_dd = ""
	_md = ""

	def __init__(self):
		self.__init__(False)
		pass

	def __init__(self, activate = False):
		if not activate:
			return
		self.__lps = []
		ltmp = serial.tools.list_ports.comports()
		if sys.platform.startswith('win'):
			ltmp = serial_list_ports_patch()
			sleep(2)
		#--------
		if sys.platform == "linux2":
			ltmp.append(('/dev/rfcomm0', 'rfcomm0', 'Bluetooth'))
		#--------
		for e in ltmp:
			if not e[0] in ModCom.__lps and not e[0] in blacklist:
				# print e[0]
				self._ser = serial.Serial(e[0], 9600, timeout = 1, rtscts=1)
				if not self._ser.isOpen():
					self._ser.open()
				if self._checkdev():
					self._dd = e[0]
					ModCom.__lps.append(e[0])
					self._assigned = True
					break
			if self._ser.isOpen():
				self._ser.close()

	def __del__(self):
		if self._ser.isOpen():
			self._ser.close()
		if len(ModCom.__lps) != 0 and self._assigned and self._dd != '':
			ModCom.__lps.pop(ModCom.__lps.index(self._dd))

	def Comunicate(self, bufferlist, readdata = False, readsize = 0, rawbuffer = []):
		self._ser.flushInput()
		self._ser.flushOutput()
		self._ser.write(''.join(chr(e) for e in bufferlist))		
		buffin = [] 
		if not readdata:
			return buffin
		buff0 = self._ser.read() # first character (or byte) from input buffer
		if not buff0: # if empy input
			return buffin
		if ord(buff0) == 0xFF:
			buffin.append(ord(buff0))
			intr = ord(self._ser.read())
			buffin.append(intr)
			rawln = ord(self._ser.read())
			ln = rawln
			if readsize:
				ln = readsize
			buffin.append(ln)
			bufftemp = self._ser.read(ln) 
			rawbuffer.append(str(buff0) + str(chr(intr)) + str(chr(rawln)) + bufftemp)
			for e in bufftemp:
				buffin.append(ord(e))
		else:
			return []
		return buffin

	# "Private" functions -------------------------------------------------------------------------------------
	def _checkdev(self):
		self._initdev()
		linit = [0xFF, CHECK_DEV, 1, CHECK_DEV]
		lread = self.Comunicate(linit, True)
		if not lread == []:
			if lread[1] != CHECK_DEV:
				return False
			for c in lread[3:len(lread)]:
				self._md += chr(c)
			return True
		return False

	def _initdev(self):
		linit = [0xFF, INIT_DEV, 1, INIT_DEV]
		self.Comunicate(linit)
		if sys.platform.startswith('linux'):
			sleep(2)