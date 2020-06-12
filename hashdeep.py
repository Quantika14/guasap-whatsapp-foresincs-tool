#!/usr/bin/env python
#-*- coding:utf-8 -*-

import modules.utils
import subprocess
from subprocess import Popen, PIPE

def check_directory():
	for directory in modules.utils.directory:
		direct = "c:\\adb\\adb shell ls "+directory+"WhatsApp/Media/"
		b,c = Popen(direct, stdout=PIPE, stderr=PIPE).communicate()
		b=b.decode('utf-8').split("\r\n")[0]
		c=c.decode('utf-8').split("\r\n")[0]
		if "No such file or directory" in b or "No such file or directory" in c:
			print("no se ha encontrado el directorio de Whatsapp en esta ubicacion")
			continue
		else:
			print("se ha encontrado el directorio")
			return directory

def pull_media(directory):
	pull = subprocess.call("c:\\adb\\adb pull " + directory + "WhatsApp/Media Whatsapp_Extracted_Media/")
	#a = Popen("c:\\adb\\adb pull shell ls data", stdout=PIPE, stderr=PIPE)
	#a = a.communicate()

	#print(a)
	print (pull)
	#a = os.popen(pull)
	#print (a.read())