#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.config, modules.functions

def extract_log():
	#Create directory
	modules.functions.create_dir_log()
	#Extract logs names
	logs = modules.functions.count_logs()
	for log in logs:
		print "-------*-------"
		if log=="":
			pass
		else:
			#Extract logs
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
