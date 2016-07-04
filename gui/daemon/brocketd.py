
from PyQt4 import QtCore
import modcom
import moddev
import brocketdev
import sys
sys.path.append("./uimodules")

import ui_mainwindow
from time import sleep

ENABLE_INTR = 48

class bRocketD(QtCore.QThread):

	_brd = None
	Available = False
	Initialized = False
	ErrorFlag = False # Error flag for any device error
	f1 = None
	_mw = None

	ToggleEnable = False

	def __init__(self, mw):
		super(bRocketD, self).__init__()
		self.f1 = open("datalog.csv", 'w')
		self.f1.write("Yaw,Pitch,Roll,Pressure,Altitude\n")
		self._mw = mw

	def __del__(self):
		if self._brd:
			del self._brd
		if self.f1:
			self.f1.close()

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
			#print "Yaw:", self._brd.yaw, "Pitch:", self._brd.pitch, "Roll:", self._brd.roll, "Pressure:", self._brd.pressure, "Altitude:", self._brd.getAltitude(self._brd._p0)
			fmt = "{0},{1},{2},{3},{4}\n"
			strtmp = fmt.format(self._brd.yaw, self._brd.pitch, self._brd.roll, self._brd.pressure, self._brd.getAltitude(self._brd._p0))
			self.f1.write(strtmp)
			self._showvalues()

	def _showvalues(self):
		self._mw.lblYaw.setText(ui_mainwindow._translate("MainWindow", "Yaw: " + str(self._brd.yaw), None))
		self._mw.lblPitch.setText(ui_mainwindow._translate("MainWindow", "Pitch: " + str(self._brd.pitch), None))
		self._mw.lblRoll.setText(ui_mainwindow._translate("MainWindow", "Roll: " + str(self._brd.roll), None))
		self._mw.lblPressure.setText(ui_mainwindow._translate("MainWindow", "Pressure: " + str(self._brd.pressure), None))
		self._mw.lblAltitude.setText(ui_mainwindow._translate("MainWindow", "Altitude: " + str(self._brd.getAltitude(self._brd._p0)), None))

	def _refresh(self):
		self._brd.getState()
		
