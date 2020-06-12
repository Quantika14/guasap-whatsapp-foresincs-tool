#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Copyright (C) 2018  QuantiKa14 Servicios Integrales S.L
'''

#********************************************
#TEAM QUANTIKA14
#AUTHOR: JORGE CORONADO A.K.A @JORGEWEBSEC
#AUTHOR: RAMON BAJONA 
#DESCRIPTION: APP FOR WHATSAPP FORENSIC
#DATE: 10-05-2018
#VERSION: 1.1
#********************************************

import modules.functions, hashdeep, modules.utils

#importamos subprocess para cambiarlo por el os
import subprocess
from subprocess import Popen, PIPE

# poner como un try y except
# from Tkinter import *
import os, time, socket, requests
from time import sleep
from distutils.version import LooseVersion

# Importamos el diseño
from diseño_interfaz.model_ui import *
from diseño_interfaz.window_model import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMessageBox, QVBoxLayout

# Funcionalidades graficas

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		texto=self.lblDirectory.text()+" /Reports_Guasap_Forensic"
		self.lblDirectory.setText(texto)
		self.btnStart.clicked.connect(self.ejecucion)

	def updateConsole(self, text):
		texto = self.lblConsole.text() + '\n' + text
		self.lblConsole.setText(texto)
		QtGui.QGuiApplication.processEvents()

	def ejecucion(self):
		directory = hashdeep.check_directory()
		if directory is not None:
			hashdeep.pull_media(directory)
			mensaje_deb = "Creando hash y comparando... \n Este proceso varia su duracion en base a los archivos multimedia"
			self.updateConsole(mensaje_deb)


if __name__ == '__main__':
	t=time.strftime('%A %B, %d %Y %H:%M:%S')

	#TO DOComprobamos que las dependencias están instaladas
	#modules.dependencies.check_dependencies()

	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()