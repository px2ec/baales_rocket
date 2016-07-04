
import sys
sys.path.append("./uimodules")
sys.path.append("../daemon")

# From Qt 4 Designer --------------------------------------------------------------------------------------
import ui_mainwindow

import brocketd

from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self._brdc = brocketd.bRocketD(self)
		self.pbConnect.clicked.connect(self.pbconnectclicked)
		self._enabletglstate = False
		self.pbEnable.clicked.connect(self.pbenableclicked)
		self.pbEnableTimer.clicked.connect(self.pbenabletimerclicked)
		self.pbEnableParachute.clicked.connect(self.pbenableparachute)

	def pbconnectclicked(self):
		if self._brdc.Available:
			return
		self._brdc.scanDevices()
		if not self._brdc.Available:
			QtGui.QMessageBox.information(self, "Error", "Device not found")
			return
		QtGui.QMessageBox.information(self, "Found", "Device: " + self._brdc._mc._dd)
		self.pbEnable.setEnabled(True)
		self.pbConnect.setEnabled(False)
		self.lblState.setText(ui_mainwindow._translate("MainWindow", "Oprima boton para activar", None))

	def pbenableclicked(self):
		if not self._brdc.Available:
			return
		if not self._enabletglstate:
			self._brdc.ToggleEnable = False
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Activado", None))
			self._enabletglstate = not self._enabletglstate
			self.pbEnable.setText(ui_mainwindow._translate("MainWindow", "Deshabilitar", None))
			self._brdc.start()
		else:
			self._enabletglstate = not self._enabletglstate
			self.pbEnable.setText(ui_mainwindow._translate("MainWindow", "Habilitar", None))
			self._brdc.terminate()
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Oprima boton para activar", None))

	def pbenabletimerclicked(self):
		text, boolean = QtGui.QInputDialog.getText(self, 'Set timer', 'Time 1 - 60 [s]')
		if not boolean:
			return None
		tstr = ''.join([str(x) for x in text])
		if self._enabletglstate:
			self._brdc.terminate()
		self._brdc._brd.timerTrigger(int(tstr))
		if self._enabletglstate:
			self._brdc.start()
		self.lblTimerSt.setText(ui_mainwindow._translate("MainWindow", "Timer activado", None))

	def pbenableparachute(self):
		if self._enabletglstate:
			self._brdc.terminate()
		self._brdc._brd.parachuteTrigger()
		if self._enabletglstate:
			self._brdc.start()

	def togglelabel(self):
		if self._brdc.ToggleEnable:
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Oprima boton para activar", None))
		else:
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Activado", None))
