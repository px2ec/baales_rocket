# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Jul  3 18:35:16 2015
#      by: PyQt4 UI code generator 4.10.4
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
        MainWindow.resize(242, 119)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(242, 119))
        MainWindow.setMaximumSize(QtCore.QSize(242, 119))
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
        self.lblState.setGeometry(QtCore.QRect(130, 50, 101, 41))
        self.lblState.setWordWrap(True)
        self.lblState.setObjectName(_fromUtf8("lblState"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GiveMeFive - Cliente", None))
        self.pbConnect.setText(_translate("MainWindow", "Conectar", None))
        self.pbEnable.setText(_translate("MainWindow", "Habilitar", None))
        self.lblStateLabel.setText(_translate("MainWindow", "Estado:", None))
        self.lblState.setText(_translate("MainWindow", "Desactivado", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

