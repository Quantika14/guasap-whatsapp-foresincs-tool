#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.utils as utils, modules.functions, os, GuasApp_Forensic
import subprocess
from subprocess import Popen, PIPE, STDOUT

root_posibility=False
#MagiskManager-v7.5.1.apk es nuestra aplicacion 
def check_root(window):
	root=check_su()
	mensaje_deb=check_su()+"\n"
	count=1
	list_root_info=list()
	list_root_info.append(root)
	if root != "No adb installed":
		mensaje_deb += "Buscando aplicaciones que requieren de Root..."
		window.updateConsole(mensaje_deb)
		for directory in modules.utils.directory:
			a = modules.utils.adb_comm+" shell ls "+directory+"Download/"

			if "No such file" not in a and "sh: 1: adb:" not in a:
				a = a.replace("\r","").split("\n")
				for apk in a:
					#A partir de esta línea, lee el archivo "apks_to_root.txt" y compara los nombre de las aplicaciones con el de los paquetes y/o aplicaciones en la carpeta de Descargas.
					for line in open("modules/apks_to_root.txt", "r"):
						line = line.split("||")
						for lin in line:
							if "|" in lin:
								continue
							else:
								if lin in apk:
									print("SE HA ENCONTRADO UNA APLICACION DE ROOTEO")
									#A partir de esta línea nos indica que se ha localizado una aplicación  en la carpeta de Descargas que permite realizar un rooteo.
									name_d="dict_"+str(count)
									name_d={"App":line[0].title(), "file":apk, "directory":directory}
									list_root_info.append(name_d)
									count+=1
			for line in open("modules/apks_to_root.txt", "r"):
				line = line.split("||")
				for lin in line:
					if "|" in lin:
						lin = lin.split("|")
						b = modules.utils.adb_comm+" shell ls "+directory
						b = b.replace("\r","").split("\n")
						for bpk in b:
							for li in lin:
								if li in bpk:
									name_d="dict_"+str(count)
									name_d={"App":line[0].title(), "file":bpk, "directory":directory}
									list_root_info.append(name_d)
									count+=1
					else:
						b = modules.utils.adb_comm+" shell ls "+directory
						b = b.replace("\r","").split("\n")
						for bpk in b:
							if lin in bpk:
								name_d="dict_"+str(count)
								name_d={"App":line[0].title(), "file":bpk, "directory":directory}
								list_root_info.append(name_d)
								count+=1
	magisk=check_magisk()
	if magisk:
		list_root_info.append(magisk)
	return list_root_info, root_posibility

def check_magisk():
	#no puede utilizar la aplicacion en windows por error de permiso
	if modules.utils.adb_comm == "c:\\adb\\adb":
		a = modules.utils.adb_comm+" shell cd data/data/adb && dir"
		b = modules.utils.adb_comm+" shell cd data/adb && dir"
	else:
		a = modules.utils.adb_comm+" shell cd data/data/adb && ls"
		b = modules.utils.adb_comm+" shell cd data/adb && ls"
	a = subprocess.Popen(a, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
	b = subprocess.Popen(b, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
	
	if "magisk" in a or "magisk" in b:
		return {"directory":"data/adb","App":"Magisk","file":"magisk_debug.log"}
	else:
		return False

#Aquí comprobamos a través de un comando si el dispositivo dispone de permisos de root.
def check_su():
	global root_posibility
	command = modules.utils.adb_comm+" shell su 0 ls /data/data/com.whatsapp"
	process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
	err = process.communicate()[0].decode('utf-8')
#Nos devolverá este error si en nuestro equipo no tenemos instalado ADB
	if "inaccessible or not found" in err:
		root_posibility=False
		return "Inaccessible or not found device make sure that your phone is connected and routed"

	elif "sh: 1: adb:" in err or "no se reconoce como un comando" in err: 
		root_posibility=False
		return "No adb installed"
#Nos devolverá este error si no hemos autorizado la depuración USB en nuestro dispositivo
	elif "device unauthorized" in err :
		root_posibility=False
		return "No debugging active"
#Nos devolverá este error si el dispositivo no se encuentra conectado a nuestro equipo
	elif "error: device" in err:
		root_posibility=False
		return "No such device"


	else:
#Nos devoverá este error si nuestro dispositivo no dispone de permisos de root o no se encuentra rooteado
		if "su: not found" in err:
			root_posibility=False
			return "No root device"
#Nos devolverá este aviso en caso de que el dispositivo esté rooteado
		else:
			root_posibility=True
			return "Root Device"

def get_whatsappDB(db):

	for directory in utils.directory:
		a = utils.adb_comm+" shell dd if='"+directory+"WhatsApp/Databases/"+db+"' of='"+directory+db+"' bs=1000"
		extract = utils.adb_comm+" pull "+directory+db+" WhatsappDB/"+db
		#command = os.popen(a)
		command=subprocess.Popen(a, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")

		print("Esto es la base de datos ######")
		print(command)
		command=command.replace("\r","").replace("\n","")
		if "file or directory" != command[len(command)-17:len(command)] and "unknown operand" not in command:
#			os.system(a)
			print ('USB debbuging active...')
			os.system(extract)
			print ('Extract whatsapp db...')
			return db 
		print ('Change directory...')
"""except :
	print (utils.error_alert[0])"""


def create_dir_media():
	try:
		os.mkdir("Whatsapp_Extracted_Media")
		print ('The directory was created correctly')
	except:
		print ('Verify that the Media directory is created')

def create_dir_db():
	try:
		os.mkdir("WhatsappDB")
		print ('The directory was created correctly')
	except:
		print ('Verify that the WhatsappDB directory is created')


def count_dbs():
	dbs_=list()
	for directory in utils.directory:
		command = utils.adb_comm+" shell ls "+directory+"WhatsApp/Databases/"
		#command = utils.adb_comm + " shell ls " + "/data/data/com.whatsapp/databases/"
		#dbs = os.popen(command).read()
		dbs=subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")

		if "No such file or directory" in dbs:
			continue
		else:
			dbs = dbs.replace("\r","").split("\n")
			for db in dbs:
				if " " in db:
					db = db.split(" ")
					for d in db:
						dbs_.append(d)
				else:
					dbs_.append(db)
			return dbs_

def get_hash(data, option):
	if option == "origin":
		for directory in utils.directory:
			command = utils.adb_comm+" shell md5 "+directory+"WhatsApp/Databases/"+data
			md5 = modules.utils.adb_comm+" shell md5sum "+directory+"WhatsApp/Databases/"+data
			hash_=subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			hash_2=subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			if "No such file" in hash_:
				pass
			else:
				if "not found" in hash_:
					pass
				else:
					break
			if "No such file" in hash_2:
				continue
			else:
				if "not found" in hash_2:
					continue
				else:
					return hash_2
	elif option == "clone":
		for directory in utils.directory:
			command = utils.adb_comm+" shell md5 "+directory+data
			md5 = modules.utils.adb_comm+" shell md5sum "+directory+data
			hash_=subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			hash_2=subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			
			if "No such file" in hash_:
				pass
			else:
				if "not found" in hash_:
					pass
				else:
					break
			if "No such file" in hash_2:
				continue
			else:
				if "not found" in hash_2:
					continue
				else:
					return hash_2
	return hash_