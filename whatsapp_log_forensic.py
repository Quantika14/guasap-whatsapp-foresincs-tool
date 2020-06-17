  
#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.utils, modules.functions, GuasApp_Forensic


def extract_log(root):
	#Create directory
	modules.functions.create_dir_log()
	#Extract logs names
	logs = modules.functions.count_logs()
	for log in logs:
		print ("-------*-------")
		if log=="":
			pass
		else:
			log=log.split(" ")
			for l in log :
				if l != "":
					#Extract logs
					mensaje_deb = "Logs extraidos, analizando..."
					root.updateConsole(mensaje_deb)
					l = modules.functions.get_whatsappLog(l)

					#Decompress gz
					if ".gz" in l:
						modules.functions.set_permission_log(l)
						modules.functions.decompress("WhatsappLOG/"+l)
						log_name = l+".txt"
					else:
						log_name = l
					#add name of logs for extract deleted messages
					modules.utils.analyze_logs.append(log_name)
	#Extract deleted messages
	log_list=modules.functions.extract_deleted_messages()
	return log_list