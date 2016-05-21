
import sys
from PyQt4 import QtCore, QtGui

sys.path.append("./daemon")
sys.path.append("./gmouseui")
sys.path.append("./gmouseui/uimodules")

from mainwindow import MainWindow

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myWindow = MainWindow()
	myWindow.show()
	app.exec_()