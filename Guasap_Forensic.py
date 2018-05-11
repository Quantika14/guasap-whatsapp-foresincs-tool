#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Copyright (C) 2018  QuantiKa14 Servicios Integrales S.L
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
#********************************************
#TEAM QUANTIKA14
#AUTHOR: JORGE CORONADO A.K.A @JORGEWEBSEC
#AUTHOR: RAMON BAJONA 
#DESCRIPTION: APP OPEN SOURCE FOR WHATSAPP FORENSIC
#DATE: 10-05-2018
#VERSION: 1.1
#********************************************

import whatsapp_log_forensic, modules.functions, whatsapp_db, check_root, hashdeep, modules.config

from Tkinter import *
import os, time, socket
from time import sleep
from pkg_resources import parse_version

licencia=""
rute= ""
inten=False
menu=True
report=False
list_dbs=list()
info_root=list()
whatsapp_log=list()
label_root=False
root_posibility=False
popup_a=False
debugging=False

if os.name == 'nt':
	modules.config.adb_comm=modules.config.adb_w
else:
	modules.config.adb_comm=modules.config.adb_l

def info_root_f(root):
	global info_root
	global label_root
	global root_posibility
	global popup_a
	info_root,roote=check_root.check_root()
	root_posibility=roote
	popup_a=True
	reloadd(root)


def popup():
	global info_root
	global label_root
	global root_posibility
	pop_root = Toplevel()
	pop_root.title("CHECK ROOT")
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


	elif info_root[0]=="No adb installed.":
		mensaje = Label(pop_root, text="No ADB installed. Please enter the folder 'adb' in the location of the app.")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	elif info_root[0]=="No debugging active.":
		mensaje = Label(pop_root, text="No debug permissions detected,\n please check device.")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	else:
		mensaje = Label(pop_root, text="No device connect!")
		mensaje.place(x=40,y=40)
		mensaje.configure(foreground="red")
	label_root = True

def whatsapp_deb(root, option):
	en,out,err=os.popen3(modules.config.adb_comm+" shell ls data")
	err = err.read()
	if "device unauthorized" in err:
		os.popen(modules.config.adb_comm+" kill-server")
		os.popen(modules.config.adb_comm+" start-server")
		print "Please connect your Android device with USB Debugging enabled:"
		os.popen(modules.config.adb_comm+" wait-for-device")
	elif "error: device" in err:
		print """[ES]No se ha encontrado ningún dispositivo conectado al ordenador. Por favor conecte uno para realizar las funcionalidades de la aplicación. Gracias.
[IN]No such device, please check the conection and restart app"""
		option = 0
	elif "sh: 1: adb:" in err or "no se reconoce como un comando" in err:
		print "adb not installed, please install and restart app "
		option = 0
	if option == 1:
		info_root_f(root)
	elif option == 2:
		whatsapp_root(root)
	elif option == 3:
		whatsapp_mm(root)
	elif option == 4:
		whatsapp_db_f(root)
	elif option == 5:
		whatsapp_db_root(root)
	elif option == 6:
		whatsapp_log_f(root)

def whatsapp_root(root):
	option , version, marca = check_data()
	pop_roote = Toplevel()
	pop_roote.title("ROOT DEVICE")
	pop_roote.configure(width=445, height=220)
	pop_roote.resizable(width=False, height=False)
	mensaje = Label(pop_roote, text="Version: "+version)
	mensaje.place(x=20,y=40)
	mensaje.configure(foreground="green")
	mensaje_2 = Label(pop_roote, text="Mobile brand: "+marca)
	mensaje_2.place(x=20,y=60)
	mensaje_2.configure(foreground="blue")
	mensaje_3 = Label(pop_roote, text="Recommended APP: "+option["app"])
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
	pvm = parse_version(android_v)
	for dicts in modules.config.dicts_root:
		try:
			if dicts["version"]=="all":
				pvd = parse_version("20.20.20")
			else:
				pvd = parse_version(dicts["version"])
		except:
			pvd = parse_version("20.20.20")
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

def whatsapp_mm(root):
	md5_cloned,md5_original=hashdeep.extract_mm()
	label_root=True
	reloadd(root)

def whatsapp_log_f(root):
	global whatsapp_log
	global label_root
	whatsapp_log=whatsapp_log_forensic.extract_log()
	label_root = True
	reloadd(root)

def whatsapp_db_f(root):
	global list_dbs
	global label_root
	list_dbs=whatsapp_db.extract_db()
	label_root = True
	reloadd(root)

def whatsapp_db_root(root):
	global list_dbs
	global label_root
	list_dbs,rows=whatsapp_db.extract_db_root()
	label_root = True
	reloadd(root)

def reloadd(root):
	root.destroy()

def on_closing(root):
	d = Dialog_exit(root)

def Dialog_exit(parent):
	top = Toplevel(parent)
	parent = parent
	top.title("EXIT")

	Label(top, text="ARE YOU SURE?").grid(row=0, column=0, columnspan=2)

	button1 = Button(top, text="EXIT", command= lambda: out(top,parent))
	button2 = Button(top, text="NO", command= lambda: icon(top, parent))
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
	print "****************************************************************"
	print "////////////////////////////////////////////////////////////////"
	print "****************************************************************"
	print "-- APP NAME: GUASAP FORENSIC                                  --"
	print "-- Description: WhatsApp Forensic App                         --"
	print "-- Created by QuantiKa14 Team                                 --"
	print "-- License GNU 3                                              --"
	print "-- Authors: Jorge Coronado A.K.A @JorgeWebsec & Ramon Bajona  --"
	print "-- Date: 10-05-2018                                           --"
	print "-- Email contact: info@quantika14.com                         --"
	print "****************************************************************"
	print "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
	print "****************************************************************"

	while(menu):
		root = Tk()
		root.configure(width=600, height=450)
		root.resizable(width=False, height=False)
		root.title("Guasap Forensic - WhatsApp Forensic App GNU 3")
		imagen = PhotoImage(file="images/logika14-2.PPM")
		widget = Label(root, image=imagen)
		widget.image = imagen
		widget.place(x=40,y=10)
		imagen2 = PhotoImage(file="images/logika14-1.PPM")
		widget2 = Label(root, image=imagen2)
		widget2.image = imagen2
		widget2.place(x=40,y=370)
		button_root = Button(root, text="Find ROOT in the device", width=61, state=NORMAL, command=lambda: whatsapp_deb(root, 1))
		button_root.place(x=40, y=75)
		button_roote = Button(root, text="Root device", width=61, state=NORMAL, command=lambda: whatsapp_deb(root, 2))
		button_roote.place(x=40, y=125)
		button_mm = Button(root, text="Extract WhatsApp multimedia", width=61, state=NORMAL, command=lambda: whatsapp_deb(root, 3))
		button_mm.place(x=40, y=175)
		button_dbc = Button(root, text="Extract Encrypt Data Base", width=61, state=NORMAL, command=lambda: whatsapp_deb(root, 4))
		button_dbc.place(x=40, y=225)
		button_db = Button(root, text="Extract/Analyze Data Base (Only root)", width=61, state=DISABLED, command=lambda: whatsapp_deb(root, 5))
		button_db.place(x=40, y=275)
		button_log = Button(root, text="Extract/Analyze Whatsapp log (Only root)", width=61, state=DISABLED, command=lambda: whatsapp_deb(root, 6))
		button_log.place(x=40, y=325)
		if root_posibility:
			button_root.config(background="green")
			button_log.config(state = NORMAL)
			button_db.config(state = NORMAL)
		else:
			button_root.config(background="red")
			button_log.config(state = DISABLED)
			button_db.config(state = DISABLED)
		if popup_a:
			popup()
			popup_a=False
		if label_root==True:
			label_Root = Label(root, text="Completed work.")
			label_Root.config(background="red")
			label_Root.place(x=300,y=345)
			label_root==False
		root.protocol("WM_DELETE_WINDOW", lambda:on_closing(root))
		root.mainloop()
