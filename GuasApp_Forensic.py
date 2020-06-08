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
from tkinter import *
import os, time, socket, requests
from time import sleep
from distutils.version import LooseVersion

# Importamos el diseño
from diseño_interfaz.model_ui import *
from diseño_interfaz.window_model import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMessageBox, QVBoxLayout

licencia=""
rute= ""
inten=False
menu=True
report=False
list_dbs=list()
info_root=list()
whatsapp_log=list()
label_root=False
root_posibility=None
popup_a=False
debugging=False
first_add=True

if os.name == 'nt':
	modules.config.adb_comm=modules.config.adb_w
	width_w = 72
	width_e = 63
else:
	modules.config.adb_comm=modules.config.adb_l
	width_w = 61
	width_e = 53

def enviar_licencia(licenci, root):
	global licencia
	global inten

	inten = True
	licencia = "true"
	root.destroy()
	print ("[INFO][>] Licencia GNU V.3. Recuerde que siempre podrá contribuir con la causa aportando mejoras a la aplicación desde el repositorio de GITHUB.")
	print ("[INFO][>] ----------------------------------> WWWW.QUANTIKA14.COM/GUASAP-FORENSIC")

def info_root_f(root):
	global info_root
	global label_root
	global root_posibility
	global popup_a
	mensaje_deb = "Comprobando dispositivo..."
	root.updateConsole(mensaje_deb)
	info_root,roote=check_root.check_root(root)
	root_posibility=roote
	popup_a=True

def popup(root):
	print("llama a la funcion pop up")
	global info_root
	global label_root
	global root_posibility

	print("este es info root")
	print(type(info_root))
	print("longitud")
	print(len(info_root))
	
	if info_root[0]=="No adb installed":
		mensaje ="No se ha detectado adb por favor reintente despues de instalar"
		root.updataConsole(mensaje)
		
	elif info_root[0]=="No debugging actve":
		mensaje ="No se han detectado permisos de depuración usb,\n por favor revise el telefono"
		root.updataConsole(mensaje)
	else:
		mensaje ="Ningún dispositivo conectado"
		root.updataConsole(mensaje)
	label_root = True
	print("llama al add report")
	add_report(info_root, 0)


def whatsapp_root(root):
	option , version, marca = check_data()
	
	mensaje_total = ""
	
	mensaje = "Version: "+version
	mensaje_total += mensaje
	mensaje2 = "Mobile brand: "+marca
	mensaje_total += mensaje2
	mensaje3 = "App recommended to root: "+option["app"]
	mensaje_total += mensaje3
	
	if len(option["observaciones"]) > 60 and len(option["observaciones"]) < 150:
		mensaje4 = "OBSERVATIONS:\n"+option["observaciones"][:65]
		mensaje_total += mensaje4
		mensaje5 = option["observaciones"][65:130]
		mensaje_total += mensaje5
		mensaje6 = option["observaciones"][130:]
		mensaje_total += mensaje6
	elif len(option["observaciones"]) > 150 and len(option["observaciones"]) < 200:
		mensaje4 = "OBSERVATIONS:\n"+option["observaciones"][:65]
		mensaje_total += mensaje4
		mensaje5 = option["observaciones"][65:130]
		mensaje_total += mensaje5
		mensaje6 = option["observaciones"][130:195]
		mensaje_total += mensaje6
		mensaje6 = option["observaciones"][195:]
		mensaje_total += mensaje6
	else:
		mensaje4 = "OBSERVATIONS:\n"+option["observaciones"]
		mensaje_total += mensaje4
	
	root.updateConsole(mensaje_total)
	



def check_how_root(android_v, marca):
	perfect_option="none"
	other_option="none"
	pvm = LooseVersion(android_v)
	for dicts in modules.config.dicts_root:
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

def check_data():
	command=modules.config.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.config.adb_comm+" shell getprop ro.product.manufacturer"
	objeto_version = Popen(command, stdout=PIPE, stderr=PIPE)
	#TO DO checkear que tipo de objeto tiene que ser android_v
	android_v=objeto_version.communicate()[0].decode("utf-8").split("\r\n")[0]
	err=objeto_version.communicate()[1].decode("utf-8")

	if(err==""):
		print("Este es la version de tu dispositivo "+android_v)
	else:
		print(err)

	objeto_marca=Popen(command2, stdout=PIPE, stderr=PIPE)
	marca=objeto_marca.communicate()[0].decode("utf-8")
	err=objeto_marca.communicate()[1].decode("utf-8")
	if(err==""):
		print("Este es la marca de tu dispositivo "+marca)
	else:
		print(err)

	if android_v!="" and android_v!="\r\n":
		option = check_how_root(android_v, marca)
		return option, android_v , marca
	else:
		print ("Version not found on device")

def whatsapp_mm(root):
	mensaje_deb = "Extrayendo archivos multimedia..."
	root.updateConsole(mensaje_deb)
	try:
		md5_cloned,md5_original=hashdeep.extract_mm(root)
		add_report((md5_cloned,md5_original),6)
		label_root=True
		print("el directorio de WhatsApp se ha encontrado de forma correcta")
	except:
		mensaje_deb = "No se ha encontrado el directorio de WhatsApp"
		root.updateConsole(mensaje_deb)


def whatsapp_log_f(root):
	global whatsapp_log
	global label_root
	mensaje_deb = "Extrayendo/analizando logs..."
	root.updateConsole(mensaje_deb)
	whatsapp_log=whatsapp_log_forensic.extract_log(root)
	add_report(info_root, 1)
	label_root = True

def whatsapp_db_f(root):
	global list_dbs
	global label_root
	mensaje_deb = "Extrayendo base de datos cifrada..."
	root.updateConsole(mensaje_deb)
	list_dbs=whatsapp_db.extract_db(root)
	add_report(list_dbs, 2)
	label_root = True

def whatsapp_db_root(root):
	global list_dbs
	global label_root
# Begin comments for offline development (using db files from another device (require one for root checker)):
	mensaje_deb = "Extrayendo base de datos descifrada..."
	root.updateConsole(mensaje_deb)
	list_dbs,rows=whatsapp_db.extract_db_root(root)
# end "for offline development"
	# Adding last Trello tasks
	mensaje_num = "Obteniendo estadísticas de mensajes..."
	root.updateConsole(mensaje_num)
	list_dbs,rows=whatsapp_db.extract_db_root(root)
	total_messages, byConversation_messages, groups_members = whatsapp_db.count_messages()
	removed_id = whatsapp_db.detect_breakID(total_messages)
	msg_analytics = []
	# Appending the msg analytics of each extraction for in a future will be able
	# to do a comparison among Whatsapp backup DBs and create knowledge from the 
	# differences between these 
	msg_analytics.append([[total_messages], [byConversation_messages], [removed_id], [groups_members]])
	add_report(msg_analytics, 5)
	# end Trello tasks
# Begin comments for message analytics report while the final workflow is under construction:
	# add_report(rows, 5)
# end "for message analytics"
	label_root = True

def add_report(data, option):
	global info_root
	global list_dbs
	global whatsapp_log
	global rute
	global first_add
	text_final=""

	if first_add:
		text_final+= modules.config.css
		text_final+="<h1>Guasap Forensic Report</h1><h2>QK14</h2>"
		first_add=False
	#Extrae la version de Android
	command = modules.config.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.config.adb_comm+" shell getprop ro.product.manufacturer"
	#Ejecuta los comandos para extraer version
	android_v,err=Popen(command, stdout=PIPE, stderr=PIPE).communicate()
	android_v=android_v.decode("utf-8")
	err=err.decode("utf-8")
	marca,err=Popen(command2, stdout=PIPE, stderr=PIPE).communicate()
	marca=marca.decode("utf-8")

	print("esta es el android v")
	print(android_v)

	
	if(len(err)>0 and err != "b''"):
		print("este es el posible error")
		print(err)

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

		#Crea en el informe fecha y hora de Android
		text_final+="<h3> Date of system: "+ str(t)+"</h3>"
		#Obtiene la fecha y hora
		command = modules.config.adb_comm+" shell date"

		#continuar con los cambios en las librerias
		time_device,err=Popen(command2, stdout=PIPE, stderr=PIPE).communicate()
		time_device=time_device.decode("utf-8")
		#en,time_device,err = os.popen3(command)
		#time_device=time_device.read()

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

		commandd = modules.config.adb_comm+" shell pm list packages -f"
		#en,packages,err = os.popen3(commandd)
		
		packages,err=Popen(commandd, stdout=PIPE, stderr=PIPE).communicate()
		packages=packages.decode("utf-8")
		print("estos son los paquetes que debe coger")
		print("paquetes")
		packages = packages.split("\n")
		text_final+="</p>"
		text_final+="<p class='subcabecera'>Installed packages:</p>"
		text_final+="<p>"+packages[0]+"</p>"
		text_final+="<p>"+packages[1]+"</p>"
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
				if log.has_key('deleted_msg'):
					msg_deleted=log["deleted_msg"]
					text_final+="<p>Deleted messages on log:<br>"
					for msg in msg_deleted:
						text_final+=msg+"<br>"
					text_final+="</p>"
				if log.has_key('dates_backup'):
					dates_backup=log["dates_backup"]
					text_final+="<p>Dates of backups:<br>"
					for date in dates_backup:
						text_final+="DB backup on date: "+date+"<br>"
					text_final+="</p>"
				if log.has_key('cons'):
					cons=log["cons"]
					text_final+="<p>Dates of connect: <br>"
					for con in cons:
						first=con["first_change"]
						sec=con["second_change"]
						text_final+="Date: "+con["time"]+"<br>"
						text_final+="Action: "+first["state"]+" | Name: "+first["name"]+"<br>"
						text_final+="Action: "+sec["state"]+" | Name: "+sec["name"]+"<br>"
					text_final+="</p>"
				if log.has_key("group_w"):
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
		#text_final += "<p class='subcabecera'>Deleted Messages</p>"
		# for row in data:
		# 	text_final += """<p class='messages'>"""+row.replace("Numero de telefono de whatsapp borrado", "WhatsApp phone number deleted").replace("\nTimestamp","; Timestamp")+"<br>"
		# text_final+="</p>"
		# Adding message analytics:
		# TODO: Create a new window that can offer  interaction to select or order messages by 
		# groups, users, dates,  etc.  and show message analysis customized by users. 
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
			text_final+="<b>Deleted messages: </b>"+str(elem[2][0])+"<br>"
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
	f = open (rute,'a')
	f.write(text_final)
	f.close()

def create_report_f(t):
	global rute
	t = t.split(",")[1].replace(" ","_").replace(":","_")
	rute = 'Reports_Guasap_Forensic/Report_guasap_forensic'+t+'.html'
	f = open (rute,'w')
	f.write("\n")
	f.close()
	return t

def reloadd(root):
	time.sleep(3)
	root.accept()
	root.close()

def on_closing(root):
	d = Dialog_exit(root)

def Dialog_exit(parent):
	top = Toplevel(parent)
	parent = parent
	imgicon = PhotoImage(file=os.path.join("images",'ico.gif'))
	top.tk.call('wm', 'iconphoto', top._w, imgicon)
	top.title("Salir")

	Label(top, text="¿Está seguro?").grid(row=0, column=0, columnspan=2)

	button1 = Button(top, text="Si, salir de la app", command= lambda: out(top,parent))
	button2 = Button(top, text="No.", command= lambda: icon(top, parent))
	button1.grid(row=1, column=0, padx=5, pady=5)
	button2.grid(row=1, column=1, padx=5, pady=5)

def out(top,parent):
	global menu
	menu=False
	top.destroy()
	parent.destroy()

def icon(top,parent):
	top.destroy()


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
		option=0
		try:
			#si el adb no esta instalado se va al except porque este comando dara error
			process = Popen(modules.config.adb_comm + " shell ls data", stdout=PIPE, stderr=PIPE)
			out, err = process.communicate()
			adb_instalado = True
			out = out.decode('utf-8')
			err = err.decode('utf-8')
			print("se ha comprobado el adb de forma correcta")
			#comprobamos que el adb se encuentre en el sistema el fichero que contiene adb
			print("este es el resultado")
			print(out)
			print("este es el error")
			print(err)
			
			#esto es si el adb esta instalado el el ordenador pero no hay dispositivo conectado
			if "error: no devices/emulators found" in err:
				print("NO DISPOSITIVO")
				mensaje_deb2 = "No se ha encontrado dispotivo, redirigiendo al menu..."
				self.updateConsole(mensaje_deb2)
				sleep(5)
			
		except:
			adb_instalado = False
			mensaje_deb2 = "No se ha encontrado dispotivo, redirigiendo al menu..."
			self.updateConsole(mensaje_deb2)
			sleep(5)
			print("no se ha encontrado el archivo adb en el sistema")
			print("por favor instalo para que podamos continuar")

		if adb_instalado == True and "error: no devices/emulators found" not in err:
			print("hemos encontrado el fichero adb asi que continuamos")
				
			#WIN LIN
			if "Permission denied" in err:
				print ("Error de permiso")
				subprocess.call(modules.config.adb_comm+" kill-server")
				subprocess.call(modules.config.adb_comm+" start-server")
				print ("Please connect your Android device with USB Debugging enabled:")
				#no tiene la ventana principal si esta seleccionada la opció 2 por que?

				# TODO corregir este codigo ver la ejecucion de pop_wait
				"""mensaje_deb = Label(pop_wait, text="Por favor, conecte el modo depuración en la pantalla de su dispositivo")
				mensaje_deb.place(x=20,y=60)
				pop_wait.update()"""
				subprocess.call(modules.config.adb_comm+" wait-for-device")
				#mensaje_deb.destroy()
				print("hasta aqui va")
			#WIN LIN
			elif "error: device" in err:
				print ("No such device, please check the conection and restart app")
				mensaje_deb = "No se encuentra ningun dispositivo, por favor, compruebe la conexion y prueba de nuevo"
				self.updateConsole(mensaje_deb)
				time.sleep(1)
				option = 1
			#LIN									WIN
			elif "sh: 1: adb:" in err  or "no se reconoce como un comando" in err:
				print ("adb not installed, please install and restart app ")
				mensaje_deb = "Adb no se encuentra en el ordenador, por favor, instala adb y prueba de nuevo"
				self.updateConsole(mensaje_deb)
				time.sleep(1)
				option = 1
			while option < 7:
				if option == 0:
					print("ejecuta la opcion 0")
					popup(self)
				elif option == 1:
					print("ejecuta la opcion 1")
					info_root_f(self)
				elif option == 2:
					print("ejecuta la opcion 2")
					whatsapp_root(self)
				elif option == 3:
					print("ejecuta la opcion 3")
					whatsapp_mm(self)
				elif option == 4:
					print("ejecuta la opcion 4")
					whatsapp_db_f(self)
				elif option == 5:
					print("ejecuta la opcion 5")
					whatsapp_db_root(self)
				elif option == 6:
					print("ejecuta la opcion 6")
					whatsapp_log_f(self)
				option+=1
			
			print("llega a las comprobaciones ultimas")

			if popup_a:
			popup()
			popup_a=False
			
			if label_root==True:
				text="Trabajo finalizado."
				self.updateConsole(text)
				label_root==False


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