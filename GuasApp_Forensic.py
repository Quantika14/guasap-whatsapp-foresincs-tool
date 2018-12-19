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

import whatsapp_log_forensic, modules.functions, whatsapp_db, check_root, hashdeep, modules.config, modules.dependencies

from Tkinter import *
import os, time, socket, requests
from time import sleep
from distutils.version import LooseVersion

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
	print "[INFO][>] Licencia GNU V.3. Recuerde que siempre podrá contribuir con la causa aportando mejoras a la aplicación desde el repositorio de GITHUB."
	print "[INFO][>] ----------------------------------> WWWW.QUANTIKA14.COM/GUASAP-FORENSIC"

def info_root_f(root, pop_wait):
	global info_root
	global label_root
	global root_posibility
	global popup_a
	mensaje_deb = Label(pop_wait, text="Comprobando dispositivo...")
	mensaje_deb.place(x=20,y=60)
	pop_wait.update()
	info_root,roote=check_root.check_root(pop_wait)
	root_posibility=roote
	popup_a=True
	reloadd(root)


def popup():
	global info_root
	global label_root
	global root_posibility
	pop_root = Toplevel()
	imgicon = PhotoImage(file=os.path.join("images",'ico.gif'))
	pop_root.tk.call('wm', 'iconphoto', pop_root._w, imgicon)
	pop_root.title("Comprobar root")
	pop_root.configure(width=450, height=450)
	pop_root.resizable(width=False, height=False)
	if info_root[0]=="Root Device":
		imagen = PhotoImage(file="images/SI-ROOT.PPM")
		widget = Label(pop_root, image=imagen)
		widget.image = imagen
		widget.place(x=20,y=20)

	elif info_root[0]=="No root device":
		imagen = PhotoImage(file="images/NO-ROOT.PPM")
		widget = Label(pop_root, image=imagen)
		widget.image = imagen
		widget.place(x=20,y=20)
	elif info_root[0]=="No adb installed":
		mensaje = Label(pop_root, text="No se ha detectado adb por favor reintente despues de instalar")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	elif info_root[0]=="No debugging actve":
		mensaje = Label(pop_root, text="No se han detectado permisos de depuración usb,\n por favor revise el telefono")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	else:
		mensaje = Label(pop_root, text="Ningún dispositivo conectado")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	label_root = True
	add_report(info_root, 0)

def whatsapp_deb(root, option):
	if option != 2:
		pop_wait = Toplevel()
		icon = PhotoImage(file=os.path.join("images",'ico.gif'))
		pop_wait.tk.call('wm', 'iconphoto', pop_wait._w, icon)
		pop_wait.title("Información WhatsApp Forensic")
		pop_wait.configure(width=500, height=220)
		pop_wait.resizable(width=False, height=False)
		mensaje = Label(pop_wait, text="Espere mientras se realiza el proceso")
		mensaje.place(x=20,y=40)
		pop_wait.update()
	en,out,err=os.popen3(modules.config.adb_comm+" shell ls data")
	err = err.read()
	#WIN LIN
	if "device unauthorized" in err:
		os.popen(modules.config.adb_comm+" kill-server")
		os.popen(modules.config.adb_comm+" start-server")
		print "Please connect your Android device with USB Debugging enabled:"
		mensaje_deb = Label(pop_wait, text="Por favor, conecte el modo depuración en la pantalla de su dispositivo")
		mensaje_deb.place(x=20,y=60)
		pop_wait.update()
		os.popen(modules.config.adb_comm+" wait-for-device")
		mensaje_deb.destroy()
	#WIN LIN
	elif "error: device" in err:
		print "No such device, please check the conection and restart app"
		mensaje_deb = Label(pop_wait, text="No se encuentra ningun dispositivo, por favor,")
		mensaje_deb.place(x=20,y=60)
		mensaje_deb2 = Label(pop_wait, text="compruebe la conexion y prueba de nuevo")
		mensaje_deb2.place(x=20,y=80)
		pop_wait.update()
		time.sleep(1)
		option = 0
	#LIN									WIN
	elif "sh: 1: adb:" in err  or "no se reconoce como un comando" in err:
		print "adb not installed, please install and restart app "
		mensaje_deb = Label(pop_wait, text="Adb no se encuentra en el ordenador, por favor,")
		mensaje_deb.place(x=20,y=60)
		mensaje_deb2 = Label(pop_wait, text="instala adb y prueba de nuevo")
		mensaje_deb2.place(x=20,y=80)
		pop_wait.update()
		time.sleep(1)
		option = 0
	if option == 1:
		info_root_f(root, pop_wait)
	elif option == 2:
		whatsapp_root(root)
	elif option == 3:
		whatsapp_mm(root, pop_wait)
	elif option == 4:
		whatsapp_db_f(root, pop_wait)
	elif option == 5:
		whatsapp_db_root(root, pop_wait)
	elif option == 6:
		whatsapp_log_f(root, pop_wait)
	elif option == 0:
		reloadd(root)

def whatsapp_root(root):
	option , version, marca = check_data()
	pop_roote = Toplevel()
	pop_roote.title("Information to Root device")
	pop_roote.configure(width=445, height=220)
	imgicon = PhotoImage(file=os.path.join("images",'ico.gif'))
	pop_roote.tk.call('wm', 'iconphoto', pop_roote._w, imgicon)
	pop_roote.resizable(width=False, height=False)
	mensaje = Label(pop_roote, text="Version: "+version)
	mensaje.place(x=20,y=40)
	mensaje.configure(foreground="green")
	mensaje_2 = Label(pop_roote, text="Mobile brand: "+marca)
	mensaje_2.place(x=20,y=60)
	mensaje_2.configure(foreground="blue")
	mensaje_3 = Label(pop_roote, text="App recommended to root: "+option["app"])
	mensaje_3.place(x=20,y=80)
	mensaje_3.configure(foreground="brown")
	
	if len(option["observaciones"]) > 60 and len(option["observaciones"]) < 150:
		mensaje_4 = Label(pop_roote, text="OBSERVATIONS:\n"+option["observaciones"][:65])
		mensaje_4.place(x=20,y=100)
		mensaje_4.configure(foreground="red")
		mensaje_5 = Label(pop_roote, text=option["observaciones"][65:130])
		mensaje_5.place(x=20,y=140)
		mensaje_5.configure(foreground="red")
		mensaje_6 = Label(pop_roote, text=option["observaciones"][130:])
		mensaje_6.place(x=20,y=140)
		mensaje_6.configure(foreground="red")
	elif len(option["observaciones"]) > 150 and len(option["observaciones"]) < 200:
		mensaje_4 = Label(pop_roote, text="OBSERVATIONS:\n"+option["observaciones"][:65])
		mensaje_4.place(x=20,y=100)
		mensaje_4.configure(foreground="red")
		mensaje_5 = Label(pop_roote, text=option["observaciones"][65:130])
		mensaje_5.place(x=20,y=140)
		mensaje_5.configure(foreground="red")
		mensaje_6 = Label(pop_roote, text=option["observaciones"][130:195])
		mensaje_6.place(x=20,y=160)
		mensaje_6.configure(foreground="red")
		mensaje_6 = Label(pop_roote, text=option["observaciones"][195:])
		mensaje_6.place(x=20,y=160)
		mensaje_6.configure(foreground="red")
	else:
		mensaje_4 = Label(pop_roote, text="OBSERVATIONS:\n"+option["observaciones"])
		mensaje_4.place(x=20,y=100)
		mensaje_4.configure(foreground="red")


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
		if dicts["marca"]=="all" and (pvd==pvm or pvd<pvm):
			other_option=dicts
	if perfect_option != "none":
		return perfect_option
	elif other_option != "none":
		return other_option

def check_data():
	command=modules.config.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.config.adb_comm+" shell getprop ro.product.manufacturer"
	en,android_v,err = os.popen3(command)
	android_v=android_v.read()
	en,marca,err = os.popen3(command2)
	marca=marca.read()
	if android_v!="" and android_v!="\r\n":
		option = check_how_root(android_v, marca)
		return option , android_v, marca
	else:
		print "Version not found on device"

def whatsapp_mm(root, pop_wait):
	mensaje_deb = Label(pop_wait, text="Extrayendo archivos multimedia...")
	mensaje_deb.place(x=20,y=60)
	pop_wait.update()
	md5_cloned,md5_original=hashdeep.extract_mm(pop_wait)
	add_report((md5_cloned,md5_original),6)
	label_root=True
	reloadd(root)

def whatsapp_log_f(root, pop_wait):
	global whatsapp_log
	global label_root
	mensaje_deb = Label(pop_wait, text="Extrayendo/analizando logs...")
	mensaje_deb.place(x=20,y=60)
	pop_wait.update()
	whatsapp_log=whatsapp_log_forensic.extract_log(pop_wait)
	add_report(info_root, 1)
	label_root = True
	reloadd(root)

def whatsapp_db_f(root, pop_wait):
	global list_dbs
	global label_root
	mensaje_deb = Label(pop_wait, text="Extrayendo base de datos cifrada...")
	mensaje_deb.place(x=20,y=60)
	pop_wait.update()
	list_dbs=whatsapp_db.extract_db(pop_wait)
	add_report(list_dbs, 2)
	label_root = True
	reloadd(root)

def whatsapp_db_root(root, pop_wait):
	global list_dbs
	global label_root
	mensaje_deb = Label(pop_wait, text="Extrayendo base de datos descifrada...")
	mensaje_deb.place(x=20,y=60)
	pop_wait.update()
	list_dbs,rows=whatsapp_db.extract_db_root(pop_wait)
	add_report(rows, 5)
	label_root = True
	reloadd(root)

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
	command = modules.config.adb_comm+" shell getprop ro.build.version.release"
	command2=modules.config.adb_comm+" shell getprop ro.product.manufacturer"
	en,android_v,err = os.popen3(command)
	en,marca,err = os.popen3(command2)
	android_v=android_v.read()
	marca=marca.read()
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

		text_final+="<h3> Date of system: "+ str(t)+"</h3>"
		command = modules.config.adb_comm+" shell date"
		en,time_device,err = os.popen3(command)
		time_device=time_device.read()
		if ":" not in time_device:
			text_final+="Device Not found \n\n"
		else:
			text_final+="<h3> Date of device: "+ str(time_device)+"</h3>"
		text_final+="<p class='aversion'><b>Android version</b>: "+android_v+"</p>"
		text_final+="<p><b>Mobile brand</b>: "+marca+"</p>"
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
		en,packages,err = os.popen3(commandd)
		packages=packages.read()
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
				text_final += "<p class='aversion'><b> DataBase cript version</b>: "+db_v+"</p>"
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
		text_final += "<p class='subcabecera'>Deleted Messages</p>"
		for row in data:
			text_final += """<p class='messages'>"""+row.replace("Numero de telefono de whatsapp borrado", "WhatsApp phone number deleted").replace("\nTimestamp","; Timestamp")+"<br>"
		text_final+="</p>"
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
	root.destroy()
#	root.update()

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

if __name__ == '__main__':
	print modules.config.banner
	print "*********************************************************************************"
	print "/////////////////////////////////////////////////////////////////////////////////"
	print "*********************************************************************************"
	print "-- APP NAME: GUASAP FORENSIC                                                   --"
	print "-- Description: WhatsApp Forensic App                                          --"
	print "-- Created by QuantiKa14 Team                                                  --"
	print "-- Licencia GNU V.3                      Quantika14 Servicios Integrales S.L.  --"
	print "-- Authors: Jorge Coronado A.K.A @JorgeWebsec  / Ramon Bajona                  --"
	print "-- Date: 10-05-2018 | 19/12/2018                                                           --"
	print "-- Email contact: info@quantika14.com                                          --"
	print "*********************************************************************************"
	print "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
	print "*********************************************************************************"

	t=time.strftime('%A %B, %d %Y %H:%M:%S')

	create_report_f(t)
	
	#Comprobamos que las dependencias están instaladas
	modules.dependencies.check_dependencies()

	while(menu):
		root = Tk()
		root.configure(width=600, height=550)
		root.resizable(width=False, height=False)
		imgicon = PhotoImage(file=os.path.join("images",'ico.gif'))
		root.tk.call('wm', 'iconphoto', root._w, imgicon)
		imagen = PhotoImage(file="images/logika14-2.PPM")
		widget = Label(root, image=imagen)
		widget.image = imagen
		widget.place(x=40,y=10)
		imagen2 = PhotoImage(file="images/logika14-1.PPM")
		widget2 = Label(root, image=imagen2)
		widget2.image = imagen2
		widget2.place(x=40,y=500)
		root.title("Guasap Forensic version GNU V.3")
		w = Label(root, text="Introduzca número de licencia:")
		w.place(x=40,y=80)
		e = Entry(root, width=width_e, state=NORMAL)
		e.place(x=40,y=95)
		button = Button(root, text='Enviar', command= lambda: enviar_licencia(e.get(), root), height=1)
		button.place(x=495, y=90)
		if root_posibility == None:
				button_root = Button(root, text="CHECK indicios de ROOT", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 1))
				button_root.place(x=40, y=150)
				if licencia:
					button_root.config(state = NORMAL)
		button_roote = Button(root, text="Rootear dispositivo", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 2))
		button_roote.place(x=40, y=200)
		button_mm = Button(root, text="Extracción de Whatsapp multimedia", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 3))
		button_mm.place(x=40, y=250)
		button_dbc = Button(root, text="Extracción de Data Base cifrada", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 4))
		button_dbc.place(x=40, y=300)
		button_db = Button(root, text="Extracción/Análisis de DB (root)", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 5))
		button_db.place(x=40, y=350)
		button_log = Button(root, text="Extracción/Análisis de Whatsapp Log (root)", width=width_w, state=DISABLED, command=lambda: whatsapp_deb(root, 6))
		button_log.place(x=40, y=400)
		info = Label(root, text="Informe:")
		info.place(x=35,y=450)
		rute_la = Label(root, text=rute)
		rute_la.place(x=90,y=450)
		if root_posibility == True:
			button_root = Button(root, text="Comprobar rooteo en el dispositivo (Dispositivo rooteado)", width=width_w, command=lambda: whatsapp_deb(root, 1))
			button_root.place(x=40, y=150)
			button_root.config(foreground="green")
			button_log.config(state = NORMAL)
			button_db.config(state = NORMAL)
		elif root_posibility == False:
			button_root = Button(root, text="Comprobar rooteo en el dispositivo (Dispositivo no rooteado)", width=width_w, command=lambda: whatsapp_deb(root, 1))
			button_root.place(x=40, y=150)
			button_root.config(foreground="red")
			button_log.config(state = DISABLED)
			button_db.config(state = DISABLED)
		if inten:
			if licencia:
				button_roote.config(state = NORMAL)
				button_mm.config(state = NORMAL)
				button_dbc.config(state = NORMAL)
				e.config(state = DISABLED)
				a = Label(root, text="Licencia validada correctamente")
				a.config(foreground="#75507b")
				a.place(x=40,y=115)
			else:
				a = Label(root, text="Licencia no valida")
				a.place(x=40,y=115)
		if popup_a:
			popup()
			popup_a=False
		if label_root==True:
			label_Root = Label(root, text="Trabajo finalizado.")
			label_Root.config(foreground="red")
			label_Root.place(x=250,y=430)
			label_root==False
		root.protocol("WM_DELETE_WINDOW", lambda:on_closing(root))
		root.mainloop()
 

