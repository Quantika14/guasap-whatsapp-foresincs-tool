#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.utils, modules.functions, os, GuasApp_Forensic

root_posibility=False

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
			a = os.popen(a).read()
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
									#A partir de esta línea nos indica que se ha localizado una aplicación  en la carpeta de Descargas que permite realizar un rooteo.
									name_d="dict_"+str(count)
									name_d={"App":line[0].title(), "file":apk, "directory":directory}
									list_root_info.append(name_d)
									count+=1
			#A partir de esta línea comienza a buscar en todo el dispositivo alguna aplicación que permita realizar el rooteo.
			#si encuentra por que sigue buscando?
			for line in open("modules/apks_to_root.txt", "r"):
				line = line.split("||")
				for lin in line:
					if "|" in lin:
						lin = lin.split("|")
						b = modules.utils.adb_comm+" shell ls "+directory
						b = os.popen(b).read()
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
						b = os.popen(b).read()
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
	a = modules.utils.adb_comm+" shell cd data/data/adb && ls"
	a = os.popen(a).read()
	b = modules.utils.adb_comm+" shell cd data/adb && ls"
	b = os.popen(a).read()
	if "magisk" in a or "magisk" in b:
		return {"directory":"data/adb","App":"Magisk","file":"magisk_debug.log"}
	else:
		return False

#Aquí comprobamos a través de un comando si el dispositivo dispone de permisos de root.
def check_su():
	global root_posibility
	command = modules.utils.adb_comm+" shell su 0 ls /data/data/com.whatsapp"
	#p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	#output = p.stdout.read()
	process = Popen(command, stdout=PIPE, stderr=PIPE)
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