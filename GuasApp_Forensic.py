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
language="english"
import modules.functions, hashdeep, modules.utils,whatsapp_db, whatsapp_log_forensic,io

#importamos subprocess para cambiarlo por el os
import subprocess
from subprocess import Popen, PIPE
import os, time, socket, requests
from time import sleep
from distutils.version import LooseVersion

# Importamos el diseño
from diseño_interfaz.model_ui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFileDialog

info_root = ()
label_root = False
root_posibility = None
popup_a = False
list_dbs=list()
whatsapp_log=list()
report=False
first_add=True
rute=""
fileName=None


# Creck os
if os.name == 'nt':
	modules.utils.adb_comm=modules.utils.adb_w
else:
	modules.utils.adb_comm=modules.utils.adb_l


# Get Whatsapp media files
def whatsapp_mm(root):
	if language=="spanish":
		mensaje_deb = "Extrayendo archivos multimedia..."
	elif language=="english":
		mensaje_deb = "Extracting multimedia files..."
	root.updateConsole(mensaje_deb)
	try:
		md5_cloned,md5_original=hashdeep.extract_mm(root,language)
		add_report((md5_cloned,md5_original),6)
		label_root=True
		if language=="spanish":
			root.updateConsole("el directorio de WhatsApp se ha encontrado de forma correcta \n")
		elif language=="english":
			root.updateConsole("WhatsApp directory has been found correctly \n")
	
	except:
		if language=="spanish":
			mensaje_deb = "No se ha encontrado el directorio de WhatsApp"
		elif language=="english":
			mensaje_deb = "WhatsApp directory not found"
		root.updateConsole(mensaje_deb)


# Check if the device is root
def info_root_f(root):
	global info_root
	global label_root
	global root_posibility
	global popup_a
	if language=="spanish":
		mensaje_deb = "Comprobando dispositivo..."
	elif language=="english":
		mensaje_deb = "Checking device..."
	root.updateConsole(mensaje_deb)
	info_root,roote=modules.functions.check_root(root,language)
	root_posibility=roote
	label_root = True
	add_report(info_root,0)


# Check different info about the device
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
		except (TypeError):
			pass
	if perfect_option != "none":
		return perfect_option
	elif other_option != "none":
		return other_option


# Check different info about the device
def check_data(root):
	command=modules.utils.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.utils.adb_comm+" shell getprop ro.product.manufacturer"
	objeto_version = Popen(command, stdout=PIPE, stderr=PIPE)
	android_v=objeto_version.communicate()[0].decode("utf-8").split("\r\n")[0]
	err=objeto_version.communicate()[1].decode("utf-8")

	objeto_marca=Popen(command2, stdout=PIPE, stderr=PIPE)
	marca=objeto_marca.communicate()[0].decode("utf-8")
	err=objeto_marca.communicate()[1].decode("utf-8")

	if android_v!="" and android_v!="\r\n":
		option = check_how_root(android_v, marca)
		return option, android_v , marca
	else:
		if language=="spanish":
			mensaje_deb ="No se ha encontrado la version del dispositivo"
		elif language=="english":
			mensaje_deb ="Version not found on device"
		root.updateConsole(mensaje_deb)


# Check different root info about the device
def whatsapp_root(root):
	if language=="spanish":
		try:
			option , version, marca = check_data(root)
			mensaje_deb = " \n Version: "+version
			mensaje_deb += "\n Marca del móvil: "+marca
			mensaje_deb += "\n Aplicación recomendada para rotear: "+option["app"] + "\n"
			mensaje_deb += option["observaciones"][65:130] + "\n"
			mensaje_deb += option["observaciones"][130:] +" \n"
			
			if len(option["observaciones"]) > 150 and len(option["observaciones"]) < 200:
				mensaje_deb += "Observaciones:\n"+option["observaciones"][:65] + "\n"
				mensaje_deb += option["observaciones"][65:130] + "\n"
				mensaje_deb +=option["observaciones"][130:195] + "\n"
			elif len(option["observaciones"]) > 60 and len(option["observaciones"]) < 150:
				mensaje_deb += "Observaciones:\n"+option["observaciones"][:65]  + "\n"
				mensaje_deb += option["observaciones"][195:]  + "\n"
			else:
				mensaje_deb += "Observaciones:\n"+option["observaciones"] + "\n"	
			root.updateConsole(mensaje_deb)
		except:
			pass
	elif language=="english":
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


# Extract the running database by file
def db_uploaded_file(root):
	global label_root
	if language=="spanish":
		mensaje_deb = "Extrayendo base de datos descifrada..."
	elif language=="english":
		mensaje_deb = "Extracting decrypted database ..."
	root.updateConsole(mensaje_deb)
	if language=="spanish":
		mensaje_num = "Obteniendo estadísticas de mensajes..."
	elif language=="english":
		mensaje_num = " Obtaining message statistics ..."
	root.updateConsole(mensaje_num)
	rows=whatsapp_db.extract_db_file(root,fileName,language)
	total_messages, byConversation_messages, groups_members = whatsapp_db.count_messages(root,language)
	removed_id = whatsapp_db.detect_breakID(total_messages)
	msg_analytics = []
	# Appending the msg analytics of each extraction for in a future will be able
	# to do a comparison among Whatsapp backup DBs and create knowledge from the 
	# differences between these 
	msg_analytics.append([[total_messages], [byConversation_messages], [removed_id], [groups_members]])
	add_report(msg_analytics, 5)
	label_root = True


# Extract the root databases
def whatsapp_db_root(root):
	global label_root
# Begin comments for offline development (using db files from another device (require one for root checker)):
	if language=="spanish":
		mensaje_deb = "Extrayendo base de datos descifrada..."
	elif language=="english":
		mensaje_deb = "Extracting decrypted database ..."
	root.updateConsole(mensaje_deb)
# end "for offline development"
	if language=="spanish":
		mensaje_num = "Obteniendo estadísticas de mensajes..."
	elif language=="english":
		mensaje_num = " Obtaining message statistics ..."
	root.updateConsole(mensaje_num)
	list_dbs,rows=whatsapp_db.extract_db_root(root,language)
	total_messages, byConversation_messages, groups_members = whatsapp_db.count_messages(root,language)
	removed_id = whatsapp_db.detect_breakID(total_messages)
	msg_analytics = []
	# Appending the msg analytics of each extraction for in a future will be able
	# to do a comparison among Whatsapp backup DBs and create knowledge from the 
	# differences between these 
	msg_analytics.append([[total_messages], [byConversation_messages], [removed_id], [groups_members]])
	add_report(msg_analytics, 5)
	label_root = True
	

# Extract and analyze Whatsapp logs 
def whatsapp_log_f(root):
	global whatsapp_log
	global label_root
	if language == "spanish":
		mensaje_deb = "Extrayendo/analizando logs..."
	elif language == "english":
		mensaje_deb = "Extracting / analyzing logs ..."
	root.updateConsole(mensaje_deb)
	whatsapp_log=whatsapp_log_forensic.extract_log(root,language)
	add_report(info_root, 1)
	label_root = True


# Extract encrypted databases
def whatsapp_db_f(root):
	global list_dbs
	global label_root
	if language == "spanish":
		mensaje_deb = "Extrayendo base de datos cifrada..."
	elif language == "english":
		mensaje_deb = "Extracting / analyzing logs ..."
	root.updateConsole(mensaje_deb)
	list_dbs=whatsapp_db.extract_db(root,language)
	add_report(list_dbs, 2)
	label_root = True


# Add data to the final report
def add_report(data, option):
	global info_root
	global list_dbs
	global whatsapp_log
	global rute
	global first_add
	text_final=""

	if first_add:
		text_final+= modules.utils.css
		text_final+="<h1>Guasap Forensic Report</h1><h2>QK14</h2>"
		first_add=False
	#Extrae la version de Android
	command = modules.utils.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.utils.adb_comm+" shell getprop ro.product.manufacturer"
	#Ejecuta los comandos para extraer version
	android_v,err=Popen(command, stdout=PIPE, stderr=PIPE).communicate()
	android_v=android_v.decode("utf-8")
	err=err.decode("utf-8")
	marca,err=Popen(command2, stdout=PIPE, stderr=PIPE).communicate()
	marca=marca.decode("utf-8")

	if android_v!="" and android_v!="\r\n":
		if option == 0:
			text_final+="<p class='cabecera'><b>Root check</b></p>"
		elif option == 1:
			text_final+="<p class='cabecera'><b>Log information</b></p>"
		elif option == 2:
			text_final+="<p class='cabecera'><b>Encrypt DB check</b></p>"
		elif option == 5:
			text_final+="<p class='cabecera'><b>Decrypt DB check</b></p>"
		elif option == 6:
			text_final+="<p class='cabecera'><b>Extracted media</b></p>"
		t = time.strftime('%A %B, %d %Y %H:%M:%S')

		# Add date to the report
		text_final+="<h3> Date of system: "+ str(t)+"</h3>"
		command = modules.utils.adb_comm+" shell date"

		time_device,err=Popen(command2, stdout=PIPE, stderr=PIPE).communicate()
		time_device=time_device.decode("utf-8")

		if ":" not in time_device:
			text_final+="Device Not found \n\n"
		else:
			text_final+="<h3> Date of device: "+ str(time_device)+"</h3>"
		text_final+="<p class='aversion'><b>Android version</b>: "+android_v+"</p>"
		text_final+="<p><b>Mobile brand</b>: "+ marca +"</p>"
	else:
		text_final+="<p class='cabecera'>Device Information</p><br>"
		text_final+="<p class='aversion'>Android version: Not found</p>"
	if option == 0:
		text_final+="""<p class='rootinfo'>"""
		divo=True

		for i in range(len(info_root)):
			if i == 0:
				if info_root[i]=="Root Device":
					text_final+= "<b>Root Device</b>: Yes</p><br>"
				else:
					text_final+= "<b>Root Device</b>: No</p><br>"
			else:
				if divo:
					text_final+="<div>"+"Root files: "+info_root[i]["file"]+", "+"Directory: "+info_root[i]["directory"]+", App used to root:"+info_root[i]["App"]+"<br>"
					divo=False
				else:
					text_final+= "Root files: "+info_root[i]["file"]+", "+"Directory: "+info_root[i]["directory"]+", App used to root:"+info_root[i]["App"]+"<br>"
		text_final+="</div>"

		commandd = modules.utils.adb_comm+" shell pm list packages -f"
		
		packages,err=Popen(commandd, stdout=PIPE, stderr=PIPE).communicate()
		packages=packages.decode("utf-8")
		packages = packages.split("\n")
		text_final+="</p>"
		text_final+="<p class='subcabecera'>Installed packages:</p>"
		if len(packages) >= 1:
			text_final+="<p>"+packages[0]+"</p>"
		if len(packages) >= 2:
			text_final+="<p>"+packages[1]+"</p>"
		if len(packages) >= 3:
			text_final+="<p>"+packages[2]+"</p>"
			text_final+="<div id='list'>"
		
		for i in range(3,len(packages)):
			text_final+="<p>"+packages[i]+"</p>"
		text_final+="</div>"
		text_final+='<a id="boton_" href="#" onclick="javascript:listar();return false">Show all</a>'

	elif option == 1:
		clase_list=0
		if whatsapp_log!=None:
			for log in whatsapp_log:
				text_final += "<p class='hash'><br>------------------------"+"<br>"
				text_final += "-------  <b>Cloned</b>  ------"+"<br>"
				text_final+="MD5 [>] "+str(log["hash_clonado"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(log["hash_clonado"].split(" ")[2])+"<br>"
				text_final+="--------<b>Original</b>-------"+"<br>"
				text_final+="MD5 [>] "+str(log["hash_origen"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(log["hash_origen"].split(" ")[2])+"<br>"
				text_final+="NAME LOG [>] "+log["log"]+"</p><br>"
				text_final+='<a id="boton_log_info_'+str(clase_list)+'" class="botonlog" href="#" onclick="javascript:listar_log_'+str(clase_list)+'();return false">Show analytics</a>'
				text_final+="<div id='log_info_"+str(clase_list)+"' style='display:none'>"
				if 'deleted_msg' in log:
					msg_deleted=log["deleted_msg"]
					text_final+="<p>Deleted messages on log:<br>"
					for msg in msg_deleted:
						text_final+=msg+"<br>"
					text_final+="</p>"
				if 'dates_backup' in log:
					dates_backup=log["dates_backup"]
					text_final+="<p>Dates of backups:<br>"
					for date in dates_backup:
						text_final+="DB backup on date: "+date+"<br>"
					text_final+="</p>"
				if 'cons' in log:
					cons=log["cons"]
					text_final+="<p>Dates of connect: <br>"
					for con in cons:
						first=con["first_change"]
						sec=con["second_change"]
						text_final+="Date: "+con["time"]+"<br>"
						text_final+="Action: "+first["state"]+" | Name: "+first["name"]+"<br>"
						text_final+="Action: "+sec["state"]+" | Name: "+sec["name"]+"<br>"
					text_final+="</p>"
				if "group_w" in log:
					groups = log["group_w"]
					text_final+="<p>Groups: \n"
					for group in groups:
						text_final+="Name: "+group["subject"]+", Owner: "+group["subject_owner"]+", Subject time: "+group["subject_time"]+"<br>"
						text_final+="Num creator: "+group["creator"]+", Date creation: "+group["date_creation"]+", Subject time: "+group["subject_time"]+"<br>"
						for user in group["users"]:	
							text_final+="Num de usuario del grupo: "+user+"<br>"
					text_final+="</p>"
				text_final+="</div>"
				text_final+="""<script>
function listar_log_"""+str(clase_list)+"""(){
        if ($('#log_info_"""+str(clase_list)+"""').css("display")=="none"){
          $('#log_info_"""+str(clase_list)+"""').show();
          $(boton_log_info_"""+str(clase_list)+""").text('Hide analytics');
        }
        else{
          $('#log_info_"""+str(clase_list)+"""').hide();
          $(boton_log_info_"""+str(clase_list)+""").text('Show analytics');
            }
      };</script>"""
				clase_list+=1
		else:
			text_final+= "WhatsApp Forensic doesn´t found WhatsApp"
	elif option == 2:
		i=0
		divo=False
		for dbs in list_dbs:
			if dbs["name"]!=None and dbs["name"]!="None" and "open ls" not in dbs["name"]:
				if i == 3:
					text_final+="<div id='list_dbs'>"
					divo=True
				db_v = dbs["name"].split(".")
				db_v = db_v[len(db_v)-1]
				text_final += "<p class='aversion'><b> Encrypt DB version</b>: "+db_v+"</p>"
				text_final += "<p class='hash'>------------------------"+"<br>"
				text_final += "-------  <b>Cloned</b>  ------"+"<br>"
				text_final+="MD5 [>] "+str(dbs["hash_d"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(dbs["hash_d"].split(" ")[2])+"<br>"
				text_final+="--------<b>Original</b>-------"+"<br>"
				text_final+="MD5 [>] "+str(dbs["hash_o"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(dbs["hash_o"].split(" ")[2])+"<br>"
				i+=1
			else:
				text_final += "<p> DataBase don´t found </p>"
		if divo:
			text_final+="</div>"
			text_final+='<a id="boton_dbs" href="#" onclick="javascript:listar_dbs();return false">Show all</a>'
	elif option == 5:
		i=0
		divo=False
		for dbs in list_dbs:
			if dbs["name"]!=None and dbs["name"]!="None" and "open ls" not in dbs["name"]:
				if i == 2:
					text_final+="<div id='list_dbs_root'>"
					divo=True
				db_v = dbs["name"].split(".")
				db_v = db_v[len(db_v)-1]
				text_final += "<p class='aversion'><b>Type DataBase</b>: "+db_v+"\n"
				text_final += "<p class='hash'>------------------------"+"<br>"
				text_final += "-------  <b>Cloned</b>  ------"+"<br>"
				text_final+="MD5 [>] "+str(dbs["hash_d"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(dbs["hash_d"].split(" ")[2])+"<br>"
				text_final+="--------<b>Original</b>-------"+"<br>"
				text_final+="MD5 [>] "+str(dbs["hash_o"].split(" ")[0])+"<br>"
				text_final+="Path [>] "+str(dbs["hash_o"].split(" ")[2])+"<br>"
				i+=1
			else:
				text_final += "<p>DataBase don´t found</p>"
		if divo:
			text_final+="</div>"
			text_final+='<a id="boton_dbs_root" href="#" onclick="javascript:listar_dbs_root();return false">Show all</a>'
		text_final += "<p class='subcabecera'>Messages Analytics</p>"
		for elem in data:
			text_final+="<b>Total messages: </b>"+str(elem[0][0])+"<br>"
			text_final+="<b>Messages by conversations: </b>"+"<br>"
			for conv, msg_num in elem[1][0].items():
				text_final+=conv+": "+str(msg_num)+"<br>"
			text_final+="<b>Groups members: </b><br>"
			for group, members in elem[3][0].items():
				text_final+=group+" Members: "
				for member in members:
					text_final+="&emsp;"+member+"<br>"
			text_final+="<b>Deleted messages:</b> Jumps in the database may indicate that messages have been deleted.<br>"
			text_final+="The following list exposes the IDs of the deleted messages:<br>"+str(elem[2][0])+"<br>"
	elif option == 6:
		md5_cloned=data[0]
		md5_original=data[1]
		text_final+= "<p class='aversion'><b>Number of Media files</b> [>] "+str(len(md5_original))+"</p>"
		text_final+= "<p class='hash'><br>"
		for i in range(len(md5_cloned)):
			for has in md5_original:
				if has[1] == md5_cloned[i][1]:
					text_final+="------------------------"+"<br>"
					text_final+="-------  <b>Cloned</b>  ------"+"<br>"
					text_final+="MD5 [>] "+str(md5_cloned[i][1])+"<br>"
					text_final+="Path [>] "+str(md5_cloned[i][0])+"<br>"
					text_final+="--------<b>Original</b>-------"+"<br>"
					text_final+="MD5 [>] "+str(has[1])+"<br>"
					text_final+="Path [>] "+str(has[0])+"<br>"
					if i == 2:
						text_final+="<div id='list_media'><p class='hash'>"
					out=i
		if out>2:
			text_final+="</p></div>"
			text_final+='<a id="boton_media" href="#" onclick="javascript:listar_media();return false">Show all</a>'
	with io.open(rute, "a", encoding="utf-8") as f:
		f.write(text_final)
	f.close()

# Create report with data
def create_report_f(t, root):
	global rute
	modules.functions.create_dir_report(root,language)
	t = t.split(",")[1].replace(" ","_").replace(":","_")
	rute = 'Reports_Guasap_Forensic/Report_guasap_forensic'+t+'.html'
	f = open(rute,'w')
	f.write("\n")
	f.close()
	return t

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.setWindowTitle('Guasap Forensic 2.0')
		texto=self.lblDirectory.text()+" /Reports_Guasap_Forensic"
		self.lblConsole.setStyleSheet("QLabel { background-color : black; color : white; padding: 0px 0px 10px 10px;}")
		self.lblDirectory.setText(texto)
		self.btnStart.clicked.connect(self.ejecucion)
		self.btnFile.clicked.connect(self.openFileNameDialog)
		self.rbEnglish.toggled.connect(lambda : self.english_screen())
		self.rbSpanish.toggled.connect(lambda : self.spanish_screen())
		if self.rbEnglish.isChecked():
			self.english_screen()
		elif self.rbSpanish.isChecked():
			self.spanish_screen()
		


	def openFileNameDialog(self):
		global fileName
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","all files(*)", options=options)
		file_checker=fileName.split(".")
		if file_checker[len(file_checker)-1] != "db":
			self.updateConsole("\n El archivo introducido no es valido o esta cifrado")
			self.btnStart.setEnabled(False)
		else:
			self.btnStart.setEnabled(True)

	def spanish_screen(self):
		self.btnStart.setText("Comienzo")
		self.btnLicense.setText("Licencia")
		self.btnHelp.setText("Ayuda")
		self.lblDirectory.setText("Directorio del informe: /Reports_Guasap_Forensic/")
		self.lblFooter.setText("CONTACTO: INFO@QUANTIKA14.COM / +34 954 96 55 51 / WWW.QUANTIKA14.COM")
		self.rbEnglish.setText("Inglés")
		self.rbSpanish.setText("Español")
		self.lblLenguage.setText("Lenguaje")
		self.btnFile.setText("Añadir Base de datos")
		self.lblImage.setText("Analizar Base de datos")

	def english_screen(self):
		self.btnStart.setText("Start")
		self.btnLicense.setText("License")
		self.btnHelp.setText("Help")
		self.lblDirectory.setText("Report directory: /Reports_Guasap_Forensic/")
		self.lblFooter.setText("CONTACT: INFO@QUANTIKA14.COM / +34 954 96 55 51 / WWW.QUANTIKA14.COM")
		self.rbEnglish.setText("English")
		self.rbSpanish.setText("Spanish")
		self.lblLenguage.setText("Language")
		self.btnFile.setText("Add DataBase")
		self.lblImage.setText("Analyze Data Base")

	def updateConsole(self, text):
		texto = self.lblConsole.text() + '\n' + text
		self.lblConsole.setText(texto)
		QtGui.QGuiApplication.processEvents()

	def ejecucion(self):
		global language
		if self.rbEnglish.isChecked():
			language="english"
		elif self.rbSpanish.isChecked():
			language="spanish"

		if fileName == None :
			info_root_f(self)
			whatsapp_mm(self)
			if root_posibility:
				whatsapp_root(self)
				whatsapp_db_f(self)
				whatsapp_db_root(self)
				whatsapp_log_f(self)
		
		else:
			db_uploaded_file(self)
		if language=="spanish":
			self.updateConsole(" \n La ejecucion se ha completado")
		elif language=="english":
			self.updateConsole("  \n Execution is complete")


	
if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	t=time.strftime('%A %B, %d %Y %H:%M:%S')
	create_report_f(t, window)
	app.exec_()
