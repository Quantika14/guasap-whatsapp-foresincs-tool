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
        self.btnLicense.setGeometry(QtCore.QRect(580, 380, 75, 23))
        self.btnLicense.setObjectName("btnLicense")
        self.btnHelp = QtWidgets.QPushButton(self.centralwidget)
        self.btnHelp.setGeometry(QtCore.QRect(580, 410, 75, 23))
        self.btnHelp.setObjectName("btnHelp")
        self.lblDirectory = QtWidgets.QLabel(self.centralwidget)
        self.lblDirectory.setGeometry(QtCore.QRect(580, 90, 481, 16))
        self.lblDirectory.setObjectName("lblDirectory")
        self.lblFooter = QtWidgets.QLabel(self.centralwidget)
        self.lblFooter.setGeometry(QtCore.QRect(0, 490, 1091, 20))
        self.lblFooter.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFooter.setObjectName("lblFooter")
        self.lblImage = QtWidgets.QLabel(self.centralwidget)
        self.lblImage.setGeometry(QtCore.QRect(580, 170, 171, 31))
        self.lblImage.setObjectName("lblImage")
        self.btnFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnFile.setGeometry(QtCore.QRect(580, 200, 150, 50))
        self.btnFile.setObjectName("btnFile")
        self.rbEnglish = QtWidgets.QRadioButton(self.centralwidget)
        self.rbEnglish.setGeometry(QtCore.QRect(840, 40, 80, 17))
        self.rbEnglish.setChecked(True)
        self.rbEnglish.setObjectName("rbEnglish")
        self.rbSpanish = QtWidgets.QRadioButton(self.centralwidget)
        self.rbSpanish.setGeometry(QtCore.QRect(840, 60, 80, 17))
        self.rbSpanish.setObjectName("rbSpanish")
        self.lblLenguage = QtWidgets.QLabel(self.centralwidget)
        self.lblLenguage.setGeometry(QtCore.QRect(840, 20, 60, 20))
        self.lblLenguage.setObjectName("lblLenguage")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 541, 461))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblConsole = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lblConsole.setAutoFillBackground(False)
        self.lblConsole.setText("")
        self.lblConsole.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.lblConsole.setWordWrap(False)
        self.lblConsole.setObjectName("lblConsole")
        self.verticalLayout.addWidget(self.lblConsole)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnFile.setText(_translate("MainWindow", "Add DataBase"))
        self.btnLicense.setText(_translate("MainWindow", "License"))
        self.btnHelp.setText(_translate("MainWindow", "Help"))
        self.lblDirectory.setText(_translate("MainWindow", "Report directory: "))
        self.lblFooter.setText(_translate("MainWindow", "CONTACT: INFO@QUANTIKA14.COM / +34 954 96 55 51 / WWW.QUANTIKA14.COM"))
        self.lblImage.setText(_translate("MainWindow", "Analyze Data Base"))
        self.rbEnglish.setText(_translate("MainWindow", "English"))
        self.rbSpanish.setText(_translate("MainWindow", "Spanish"))
        self.lblLenguage.setText(_translate("MainWindow", "Lenguage"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

