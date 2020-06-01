#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.config, modules.functions
# poner como un try y except
# from Tkinter import *
from tkinter import *

def extract_log(pop_wait):
	#Create directory
	modules.functions.create_dir_log()
	#Extract logs names
	logs = modules.functions.count_logs()
	for log in logs:
		print ("-------*-------")
		if log=="":
			pass
		else:
			#Extract logs
			mensaje_deb = Label(pop_wait, text="Logs extraidos, analizando...")
			mensaje_deb.place(x=20,y=80)
			pop_wait.update()
			log = modules.functions.get_whatsappLog(log)
			#Decompress gz
			if ".gz" in log:
				modules.functions.set_permission_log(log)
				modules.functions.decompress("WhatsappLOG/"+log)
				log_name = log+".txt"
			else:
				log_name = log
			#add name of logs for extract deleted messages
			modules.config.analyze_logs.append(log_name)
	#Extract deleted messages
	log_list=modules.functions.extract_deleted_messages()
	return log_list
