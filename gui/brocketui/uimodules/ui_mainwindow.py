# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(433, 183)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(433, 183))
        MainWindow.setMaximumSize(QtCore.QSize(433, 183))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pbConnect = QtGui.QPushButton(self.centralwidget)
        self.pbConnect.setGeometry(QtCore.QRect(20, 20, 94, 29))
        self.pbConnect.setObjectName(_fromUtf8("pbConnect"))
        self.pbEnable = QtGui.QPushButton(self.centralwidget)
        self.pbEnable.setEnabled(False)
        self.pbEnable.setGeometry(QtCore.QRect(20, 70, 94, 29))
        self.pbEnable.setObjectName(_fromUtf8("pbEnable"))
        self.lblStateLabel = QtGui.QLabel(self.centralwidget)
        self.lblStateLabel.setGeometry(QtCore.QRect(130, 20, 65, 21))
        self.lblStateLabel.setObjectName(_fromUtf8("lblStateLabel"))
        self.lblState = QtGui.QLabel(self.centralwidget)
        self.lblState.setGeometry(QtCore.QRect(130, 40, 101, 41))
        self.lblState.setWordWrap(True)
        self.lblState.setObjectName(_fromUtf8("lblState"))
        self.pbEnableTimer = QtGui.QPushButton(self.centralwidget)
        self.pbEnableTimer.setGeometry(QtCore.QRect(20, 130, 94, 29))
        self.pbEnableTimer.setObjectName(_fromUtf8("pbEnableTimer"))
        self.lblTimerSt = QtGui.QLabel(self.centralwidget)
        self.lblTimerSt.setGeometry(QtCore.QRect(130, 80, 101, 41))
        self.lblTimerSt.setWordWrap(True)
        self.lblTimerSt.setObjectName(_fromUtf8("lblTimerSt"))
        self.pbEnableParachute = QtGui.QPushButton(self.centralwidget)
        self.pbEnableParachute.setGeometry(QtCore.QRect(130, 130, 94, 29))
        self.pbEnableParachute.setObjectName(_fromUtf8("pbEnableParachute"))
        self.lblYaw = QtGui.QLabel(self.centralwidget)
        self.lblYaw.setGeometry(QtCore.QRect(250, 50, 151, 21))
        self.lblYaw.setObjectName(_fromUtf8("lblYaw"))
        self.lblPitch = QtGui.QLabel(self.centralwidget)
        self.lblPitch.setGeometry(QtCore.QRect(250, 80, 151, 21))
        self.lblPitch.setObjectName(_fromUtf8("lblPitch"))
        self.lblRoll = QtGui.QLabel(self.centralwidget)
        self.lblRoll.setGeometry(QtCore.QRect(250, 110, 151, 21))
        self.lblRoll.setObjectName(_fromUtf8("lblRoll"))
        self.lblPressure = QtGui.QLabel(self.centralwidget)
        self.lblPressure.setGeometry(QtCore.QRect(250, 140, 151, 21))
        self.lblPressure.setObjectName(_fromUtf8("lblPressure"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(240, 10, 171, 161))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.lblAltitude = QtGui.QLabel(self.frame)
        self.lblAltitude.setGeometry(QtCore.QRect(10, 10, 151, 21))
        self.lblAltitude.setObjectName(_fromUtf8("lblAltitude"))
        self.frame.raise_()
        self.pbConnect.raise_()
        self.pbEnable.raise_()
        self.lblStateLabel.raise_()
        self.lblState.raise_()
        self.pbEnableTimer.raise_()
        self.lblTimerSt.raise_()
        self.pbEnableParachute.raise_()
        self.lblYaw.raise_()
        self.lblPitch.raise_()
        self.lblRoll.raise_()
        self.lblPressure.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Baales Rocket", None))
        self.pbConnect.setText(_translate("MainWindow", "Conectar", None))
        self.pbEnable.setText(_translate("MainWindow", "Habilitar", None))
        self.lblStateLabel.setText(_translate("MainWindow", "Estado:", None))
        self.lblState.setText(_translate("MainWindow", "Desactivado", None))
        self.pbEnableTimer.setText(_translate("MainWindow", "Temporizador", None))
        self.lblTimerSt.setText(_translate("MainWindow", "Timer Desactivado", None))
        self.pbEnableParachute.setText(_translate("MainWindow", "Parachute", None))
        self.lblYaw.setText(_translate("MainWindow", "Yaw: ", None))
        self.lblPitch.setText(_translate("MainWindow", "Pitch: ", None))
        self.lblRoll.setText(_translate("MainWindow", "Roll: ", None))
        self.lblPressure.setText(_translate("MainWindow", "Pressure: ", None))
        self.lblAltitude.setText(_translate("MainWindow", "Altitude (relative): ", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

