# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_modelo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1089, 521)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(580, 20, 231, 51))
        self.btnStart.setObjectName("btnStart")
        self.btnLicense = QtWidgets.QPushButton(self.centralwidget)
        self.btnLicense.setGeometry(QtCore.QRect(920, 20, 75, 23))
        self.btnLicense.setObjectName("btnLicense")
        self.btnHelp = QtWidgets.QPushButton(self.centralwidget)
        self.btnHelp.setGeometry(QtCore.QRect(990, 20, 75, 23))
        self.btnHelp.setObjectName("btnHelp")
        self.lblDirectory = QtWidgets.QLabel(self.centralwidget)
        self.lblDirectory.setGeometry(QtCore.QRect(580, 90, 481, 16))
        self.lblDirectory.setObjectName("lblDirectory")
        self.lblFooter = QtWidgets.QLabel(self.centralwidget)
        self.lblFooter.setGeometry(QtCore.QRect(0, 490, 1091, 20))
        self.lblFooter.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFooter.setObjectName("lblFooter")
        self.Imagen = QtWidgets.QGraphicsView(self.centralwidget)
        self.Imagen.setGeometry(QtCore.QRect(580, 120, 481, 351))
        self.Imagen.setObjectName("Imagen")
        self.lblConsole = QtWidgets.QLabel(self.centralwidget)
        self.lblConsole.setGeometry(QtCore.QRect(30, 20, 521, 451))
        self.lblConsole.setText("")
        self.lblConsole.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.lblConsole.setWordWrap(False)
        self.lblConsole.setObjectName("lblConsole")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnLicense.setText(_translate("MainWindow", "License"))
        self.btnHelp.setText(_translate("MainWindow", "Help"))
        self.lblDirectory.setText(_translate("MainWindow", "Report directory: "))
        self.lblFooter.setText(_translate("MainWindow", "CONTACT: INFO@QUANTIKA14.COM / +34 954 96 55 51 / WWW.QUANTIKA14.COM"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

