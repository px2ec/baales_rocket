
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
		self._gmdc = brocketd.bRocketD()
		self.pbConnect.clicked.connect(self.pbconnectclicked)
		self._enabletglstate = False
		self.pbEnable.clicked.connect(self.pbenableclicked)
		self.connect(self._gmdc, QtCore.SIGNAL('toggle()'), self.togglelabel)

	def pbconnectclicked(self):
		if self._gmdc.Available:
			return
		self._gmdc.scanDevices()
		if not self._gmdc.Available:
			QtGui.QMessageBox.information(self, "Error", "Device not found")
			return
		QtGui.QMessageBox.information(self, "Found", "Device: " + self._gmdc._mc._dd)
		self.pbEnable.setEnabled(True)
		self.pbConnect.setEnabled(False)

	def pbenableclicked(self):
		if not self._gmdc.Available:
			return
		if not self._enabletglstate:
			self._gmdc.ToggleEnable = False
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Oprima boton para activar", None))
			self._enabletglstate = not self._enabletglstate
			self.pbEnable.setText(ui_mainwindow._translate("MainWindow", "Deshabilitar", None))
			self._gmdc.start()
		else:
			self._enabletglstate = not self._enabletglstate
			self.pbEnable.setText(ui_mainwindow._translate("MainWindow", "Habilitar", None))
			self._gmdc.terminate()
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Desactivado", None))

	def togglelabel(self):
		if self._gmdc.ToggleEnable:
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Activado", None))
		else:
			self.lblState.setText(ui_mainwindow._translate("MainWindow", "Oprima boton para activar", None))