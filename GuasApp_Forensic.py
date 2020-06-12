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

import parser_db, whatsapp_log_forensic, modules.functions, whatsapp_db, check_root, hashdeep, modules.config, modules.dependencies

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
		


if __name__ == '__main__':
	print (modules.config.banner)
	print ("///////////////////////////////////////////////////////////////////////////////// ")
	print ("*********************************************************************************")
	print ("-- APP NAME: GUASAP FORENSIC                                                   --")
	print ("-- Description: WhatsApp Forensic App                                          --")
	print ("-- Created by QuantiKa14 Team                                                  --")
	print ("-- Licencia GNU V.3                      Quantika14 Servicios Integrales S.L.  --")
	print ("-- Authors: Jorge Coronado A.K.A @JorgeWebsec  / Ramon Bajona                  --")
	print ("-- Date: 10-05-2018 | 19/12/2018                                               --")
	print ("-- Email contact: info@quantika14.com                                          --")
	print ("*********************************************************************************")
	print ("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
	print ("*********************************************************************************")

	t=time.strftime('%A %B, %d %Y %H:%M:%S')

	create_report_f(t)

	#TO DOComprobamos que las dependencias están instaladas
	#modules.dependencies.check_dependencies()

	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()