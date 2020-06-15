#!/usr/bin/env python
#-*- coding:utf-8 -*-

import modules.utils
import subprocess
from subprocess import Popen, PIPE

def check_directory():
	for directory in modules.utils.directory:
		direct = modules.utils.adb_comm +" shell ls "+directory+"WhatsApp/Media/"
		b,c = Popen(direct, stdout=PIPE, stderr=PIPE).communicate()
		b=b.decode('utf-8').split("\r\n")[0]
		c=c.decode('utf-8').split("\r\n")[0]
		if "No such file or directory" in b or "No such file or directory" in c:
			continue
		else:
			return directory

#extrae los archivos multimetidas de WhatsApp
def pull_media(directory):
	pull = subprocess.call(modules.utils.adb_comm + " pull "  + directory + "WhatsApp/Media Whatsapp_Extracted_Media/")
	
