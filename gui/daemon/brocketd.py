
from PyQt4 import QtCore
import modcom
import moddev
import brocketdev
import sys

from time import sleep

ENABLE_INTR = 48

class bRocketD(QtCore.QThread):

	_brd = None
	Available = False
	Initialized = False
	ErrorFlag = False # Error flag for any device error

	ToggleEnable = False

	def __init__(self):
		super(bRocketD, self).__init__()

	def __del__(self):
		if self._brd:
			del self._brd

	def scanDevices(self):
		self._mc = modcom.ModCom(True)
		if not self._mc._assigned:
			del self._mc
			#print "Error"
			return
		print "Device found"
		print "Device description: %s" % self._mc._md
		if self._mc._md == "BAALES_ROCKET":
			self._brd = brocketdev.bRocketDev()
			self._brd._mc = self._mc
			self.Available = True
			return
		if self._mc != None:
			del self._mc
	ErrorFlag = False # Error flag for any device error
				
	def run(self):
		while self.Available:
			self._refresh()
			print "Yaw:", self._brd.yaw, "Pitch:", self._brd.pitch, "Roll:", self._brd.roll, "Pressure:", self._brd.pressure, "Altitude:", self._brd.getAltitude(self._brd._p0)

	def _refresh(self):
		self._brd.getState()
		
