#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.config, modules.functions, os
from subprocess import Popen, PIPE, STDOUT

root_posibility=False

#A partir de esta línea comenzamos a verificar si el dispositivo está rooteado.
def check_root():
	root=check_su()
	count=1
	list_root_info=list()
	list_root_info.append(root)
	if root != "No adb installed":
		for directory in modules.config.directory:
			a = modules.config.adb_comm+" shell ls "+directory+"Download/"
			a = os.popen(a).read()
			print "Checking root... \n"
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
									print "Find root file"
									print "App: "+line[0].title() +" ---> "+apk 
									print "Directory: "+ directory+"Download/"+"\n"
									name_d="dict_"+str(count)
									name_d={"App":line[0].title(), "file":apk, "directory":directory}
									list_root_info.append(name_d)
									count+=1
			#A partir de esta línea comienza a buscar en todo el dispositivo alguna aplicación que permita realizar el rooteo.
			for line in open("modules/apks_to_root.txt", "r"):
				line = line.split("||")
				for lin in line:
					if "|" in lin:
						lin = lin.split("|")
						b = modules.config.adb_comm+" shell ls "+directory
						b = os.popen(b).read()
						b = b.replace("\r","").split("\n")
						for bpk in b:
							for li in lin:
								if li in bpk:
									print "Find root file"
									print "App: "+line[0].title() +" ---> Evidence: "+bpk 
									print "Directory: "+ directory+"\n"
									name_d="dict_"+str(count)
									name_d={"App":line[0].title(), "file":bpk, "directory":directory}
									list_root_info.append(name_d)
									count+=1
					else:
						b = modules.config.adb_comm+" shell ls "+directory
						b = os.popen(b).read()
						b = b.replace("\r","").split("\n")
						for bpk in b:
							if lin in bpk:
								print "Find root file"
								print "App: "+line[0].title() +" ---> "+apk
	 							print "Directory: "+ directory+"Download/"+"\n"
								name_d="dict_"+str(count)
								name_d={"App":line[0].title(), "file":bpk, "directory":directory}
								list_root_info.append(name_d)
								count+=1
			print "Change directory..."
		magisk=check_magisk()
		if magisk:
			list_root_info.append(magisk)
		if len(list_root_info)<2:
			print "No se han encontrado evidencias de root/Don't find root evidences"
#	list_root_info.append(root_posibility)
	return list_root_info, root_posibility

def check_magisk():
	a = modules.config.adb_comm+" shell cd data/adb && ls"
	a = os.popen(a).read()
	if "magisk" in a:
		print "Find root file"
		print "App: Magisk"
		print "Directory: data/adb\n"
		return {"directory":"data/adb","App":"Magisk","file":"magisk_debug.log"}
	else:
		return False

#Aquí comprobamos a través de un comando si el dispositivo dispone de permisos de root.
def check_su():
	global root_posibility
	command = modules.config.adb_comm+" shell su 0 ls /data/data/com.whatsapp"
	#p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	#output = p.stdout.read()
	en, output, error=os.popen3(command)

	err = error.read()
	out = output.read()

#Nos devolverá este error si en nuestro equipo no tenemos instalado ADB
	if "sh: 1: adb:" in err or "no se reconoce como un comando" in err:
		print "No adb installed"
		root_posibility=False
		return "No adb installed"
#Nos devolverá este error si no hemos autorizado la depuración USB en nuestro dispositivo
	elif "device unauthorized" in err:
		print "No debugging actve"
		root_posibility=False
		return "No debugging actve"
#Nos devolverá este error si el dispositivo no se encuentra conectado a nuestro equipo
	elif "error: device" in err:
		print "No such device..."
		root_posibility=False
		return "No such device"
	else:
#Nos devoverá este error si nuestro dispositivo no dispone de permisos de root o no se encuentra rooteado
		if "su: not found" in out:
			print "No root device..."
			root_posibility=False
			return "No root device"
#Nos devolverá este aviso en caso de que el dispositivo esté rooteado
		else:
			print "Root Device detect..."
			root_posibility=True
			return "Root Device"
