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

import modules.functions, hashdeep, modules.utils,whatsapp_db


#importamos subprocess para cambiarlo por el os
import subprocess
from subprocess import Popen, PIPE
import os, time, socket, requests
from time import sleep
from distutils.version import LooseVersion

# Importamos el diseño
from diseño_interfaz.model_ui import *
from diseño_interfaz.window_model import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

info_root = ()
label_root = False
root_posibility = None
popup_a = False

if os.name == 'nt':
	modules.utils.adb_comm=modules.utils.adb_w
else:
	modules.utils.adb_comm=modules.utils.adb_l

# Funcionalidades graficas

"""def extract_mm(directory, root):
	directory = hashdeep.check_directory()
	if directory is not None:
		hashdeep.pull_media(directory)
		mensaje_deb = "Creando hash y comparando... \n Este proceso varia su duracion en base a los archivos multimedia"
		root.updateConsole(mensaje_deb)
#TODO comprobar por que no encuentra la aplicacion de rooteo MagiskManager-v7.5.1.apk """

def whatsapp_mm(root):
	mensaje_deb = "Extrayendo archivos multimedia..."
	root.updateConsole(mensaje_deb)
	try:
		md5_cloned,md5_original=hashdeep.extract_mm(root)
		#add_report((md5_cloned,md5_original),6)
		label_root=True
		root.updateConsole("el directorio de WhatsApp se ha encontrado de forma correcta \n")
	
	except:
		mensaje_deb = "No se ha encontrado el directorio de WhatsApp"
		root.updateConsole(mensaje_deb)

def info_root_f(root):
	global info_root
	global label_root
	global root_posibility
	global popup_a
	mensaje_deb = "Comprobando dispositivo..."
	root.updateConsole(mensaje_deb)
	info_root,roote=modules.functions.check_root(root)
	root_posibility=roote
	label_root = True

def check_how_root(android_v, marca):
	perfect_option="none"
	other_option="none"
	pvm = LooseVersion(android_v)
	for dicts in modules.utils.dicts_root:
		try:
			if dicts["version"]=="all":
				pvd = LooseVersion("20.20.20") 
			else:
				pvd = LooseVersion(dicts["version"])
		except:
			pvd = LooseVersion("20.20.20")
		if dicts["marca"]==marca and (pvd==pvm or pvd<pvm):
			perfect_option=dicts
		try:
			if dicts["marca"]=="all" and (pvd==pvm or pvd<pvm):
				other_option=dicts
		#a veces las versiones no son comparables
		except (TypeError):
			pass
	if perfect_option != "none":
		return perfect_option
	elif other_option != "none":
		return other_option


def check_data(root):
	command=modules.utils.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.utils.adb_comm+" shell getprop ro.product.manufacturer"
	objeto_version = Popen(command, stdout=PIPE, stderr=PIPE)
	#TO DO checkear que tipo de objeto tiene que ser android_v
	android_v=objeto_version.communicate()[0].decode("utf-8").split("\r\n")[0]
	err=objeto_version.communicate()[1].decode("utf-8")

	objeto_marca=Popen(command2, stdout=PIPE, stderr=PIPE)
	marca=objeto_marca.communicate()[0].decode("utf-8")
	err=objeto_marca.communicate()[1].decode("utf-8")

	if android_v!="" and android_v!="\r\n":
		option = check_how_root(android_v, marca)
		return option, android_v , marca
	else:
		mensaje_deb ="Version not found on device"
		root.updateConsole(mensaje_deb)

def whatsapp_root(root):
	try:
		option , version, marca = check_data(root)
		mensaje_deb = " \n Version: "+version
		mensaje_deb += "\n Mobile brand: "+marca
		mensaje_deb += "\n App recommended to root: "+option["app"] + "\n"
		mensaje_deb += option["observaciones"][65:130] + "\n"
		mensaje_deb += option["observaciones"][130:] +" \n"
		
		if len(option["observaciones"]) > 150 and len(option["observaciones"]) < 200:
			mensaje_deb += "OBSERVATIONS:\n"+option["observaciones"][:65] + "\n"
			mensaje_deb += option["observaciones"][65:130] + "\n"
			mensaje_deb +=option["observaciones"][130:195] + "\n"
		elif len(option["observaciones"]) > 60 and len(option["observaciones"]) < 150:
			mensaje_deb += "OBSERVATIONS:\n"+option["observaciones"][:65]  + "\n"
			mensaje_deb += option["observaciones"][195:]  + "\n"
		else:
			mensaje_deb += "OBSERVATIONS:\n"+option["observaciones"] + "\n"
		root.updateConsole(mensaje_deb)

	except:
		pass
	
def whatsapp_db_f(root):
	global list_dbs
	global label_root
	mensaje_deb = "Extrayendo base de datos cifrada..."
	root.updateConsole(mensaje_deb)
	list_dbs=whatsapp_db.extract_db(root)
	#add_report(list_dbs, 2)
	label_root = True
	



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
		info_root_f(self)
		whatsapp_root(self)
		extract_mm(modules.utils.directory,self)
		whatsapp_mm(self)
		whatsapp_db_f(self)


if __name__ == '__main__':
	t=time.strftime('%A %B, %d %Y %H:%M:%S')

	#TO DOComprobamos que las dependencias están instaladas
	#modules.dependencies.check_dependencies()

	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()