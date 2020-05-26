# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diseño_menu.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import diseño
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 60, 71, 61))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 50, 401, 91))
        self.label_2.setObjectName("label_2")
        self.encontrar_root = QtWidgets.QPushButton(self.centralwidget)
        self.encontrar_root.setGeometry(QtCore.QRect(180, 160, 421, 24))
        self.encontrar_root.setObjectName("encontrar_root")
        self.rootear = QtWidgets.QPushButton(self.centralwidget)
        self.rootear.setGeometry(QtCore.QRect(180, 210, 421, 24))
        self.rootear.setObjectName("rootear")
        self.multimedia = QtWidgets.QPushButton(self.centralwidget)
        self.multimedia.setGeometry(QtCore.QRect(180, 260, 421, 24))
        self.multimedia.setObjectName("multimedia")
        self.base_datos = QtWidgets.QPushButton(self.centralwidget)
        self.base_datos.setGeometry(QtCore.QRect(180, 310, 421, 24))
        self.base_datos.setObjectName("base_datos")
        self.analizar_bbdd = QtWidgets.QPushButton(self.centralwidget)
        self.analizar_bbdd.setGeometry(QtCore.QRect(180, 360, 421, 24))
        self.analizar_bbdd.setObjectName("analizar_bbdd")
        self.log = QtWidgets.QPushButton(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(180, 400, 421, 24))
        self.log.setObjectName("log")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 440, 481, 91))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/imagen/Qk_imagen.PNG\"/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">PERITOS INFORMÁTICOS | INVESTIGADORES</span></p><p align=\"center\">______________________________________________</p><p align=\"center\">WWW.QUÁNTIKA14.COM</p></body></html>"))
        self.encontrar_root.setText(_translate("MainWindow", "Find ROOT in the device "))
        self.rootear.setText(_translate("MainWindow", "Root device"))
        self.multimedia.setText(_translate("MainWindow", "Extract WhatsApp multimedia"))
        self.base_datos.setText(_translate("MainWindow", "Extract Encript Data Base"))
        self.analizar_bbdd.setText(_translate("MainWindow", "Extract/Analize Data Base (Only root)"))
        self.log.setText(_translate("MainWindow", "Extract/Analize Whatsapp log (Only root)"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p>AYUDANOS A ENCONTRAR MENORES DESAPARECIDOS CON SOLO 1 EURO AL MES</p><p><span style=\" font-size:9pt;\">https://www.teaming.net/ayudaabuscaramenoresdesaparecidosatravesdelastecnologias- </span></p></body></html>"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
