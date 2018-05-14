#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
import config
import gzip, time, datetime, modules.config

#FORENSIC FUNCTIONS

def extract_deleted_messages():
	try:
		log_list=list()
		print config.analyze_logs
		for log in config.analyze_logs:
			texts=list()
			count = 0
			count_n = 0
			count_dict = 0
			con_list=list()
			times=list()
			list_groups=list()
			f = open("WhatsappLOG/"+log, "r")
			lines = f.readlines()
			for line in lines:
				users=list()
				c_messages = 0
				if "msgstore/deletemessages" in line:
					message_delete = line.split(" ")
					l = len(message_delete)
					date = message_delete[0]
					hour = message_delete[1]
					c_messages = int(message_delete[l-1].replace("\n", ""))
					tel_list = [lines[count -1],lines[count -2],lines[count -3],lines[count -4],lines[count -5],lines[count -6],lines
[count -7],lines[count -8],lines[count -9],lines[count -10]]
					for tel in tel_list:
						if "getMediaMessagesTailCursor" in tel:
							num=True
							count_n=0
							tel = tel.split("getMediaMessagesTailCursor:")[1].split("@")[0]
							for n in tel:
								if n.isdigit(): 
									if count_n == 10 and num != False:
										tel_d = tel
									count_n+=1
									continue
								else:
									num=False
							if tel_d and num:
								text = "Found " + str(c_messages) + " deleted messages [" + str(date) + "] [" + str(hour) + "]" + "-> " + str(tel_d) + " of file ->" + log 
								texts.append(text)
								print text
						elif "stanzaKey" in tel:
							num=True
							count_n=0
							tel = tel.split("StanzaKey")[1].split("@")[0].split("=")[1]
							for n in tel:
								if n.isdigit():
									if count_n == 10 and num != False:
										tel_d = tel
									count_n+=1
									continue
								else:
									num=False
							if tel_d and num:
								text = "Found " + str(c_messages) + " deleted messages [" + str(date) + "] [" + str(hour) + "]" + "-> " + str(tel_d) + " of file ->" + log 
								print text
								texts.append(text)
						else:
							num=True
							count_n=0
							tel = tel.split(" ")
							l_tel = len(tel)
							tel = tel[l_tel-2].split("@")[0]
							for n in tel:
								if n.isdigit(): 
									if count_n == 10 and num != False:
										tel_d = tel
									count_n+=1
									continue
								else:
									num=False
							if tel_d and num:
								text = "Found " + str(c_messages) + " deleted messages [" + str(date) + "] [" + str(hour) + "]" + "-> " + str(tel_d) + " of file ->" + log 
								print text
								texts.append(text)
				if "msgstore/backupdb\n" in line:
					time_backup = line.split(" ")
					time_backup = time_backup[0]+" "+time_backup[1]
					print "Backup DBs on time [>] "+time_backup
					times.append(time_backup)
				if "onGroupInfoFromList/gjid" in line:
					group_info = line.split(" ")
					group_info = group_info.split("/")
					num_creator = group_info[3].split(":")[1].split("@")[0]
					date_creation = group_info[4].split(":")[1]
					if len(date_creation)>10:
						date_creation = date_creation[:len(date_creation)-3]
					date_creation=datetime.datetime.fromtimestamp(int(date_creation)).strftime('%Y-%m-%d %H:%M:%S')
					#1521624826948
					subject_owner = group_info[5].split(":")[1].split("@")[0]
					subject = group_info[6].split(":")[1]
					subject_time = group_info[7].split(":")[1]
					if len(subject_time)>10:
						subject_time = subject_time[:len(subject_time)-3]
					subject_time=datetime.datetime.fromtimestamp(int(subject_time)).strftime('%Y-%m-%d %H:%M:%S')
					line_users=lines[count -1]
					if "onGroupInfoFromList/{" in line_users:
						line_users=line_users.split("{")[1][:len(line_users)-1].split(",")
						for user in line_users:
							user_num = user.split("@")[0]
							users.append(user_num)
					group = {"creator":num_creator,"date_creation":date_creation,"subject_owner":subject_owner,"subject":subject,"subject_time":subject_time,"users":users}
					print "Group [>] "+subject+"\nNum creator [>] "+num_creator+" | Date creation [>] "+str(date_creation)+"\n Subject [>] "+subject+"| Subject owner num [>] "+subject_owner+" Subject time [>] "+str(subject_time)+"\n Users [>] "+str(users)
					list_groups.append(group)

				if "network/info" in line:
					con = [lines[count +1],lines[count +2]]
					time_con = line.split(" ")
					time_con = time_con[0]+" "+time_con[1]
					pri_con = con[0].split(",")
					sec_con = con[1].split(",")
					type_pri = pri_con[0].split(":")[1]
					state_pri = pri_con[1].split(":")[1]
					extra_pri = pri_con[3].split(":")[1]
					type_sec = sec_con[0].split(":")[1]
					state_sec = sec_con[1].split(":")[1]
					extra_sec = sec_con[3].split(":")[1]

					print "Time of change network [>] "+time_con
					print "Tipo: "+type_pri+", Estado: "+state_pri+", Nombre: "+extra_pri
					print "Tipo: "+type_sec+", Estado: "+state_sec+", Nombre: "+extra_sec 
					con_dict={"time":time_con,"first_change":{"state":state_pri, "name":extra_pri},"second_change":{"state":state_sec, "name":extra_sec}}
					if con_dict not in con_list:
						con_list.append(con_dict)
				count += 1

			if int(c_messages)>=0 or len(times)>0 or len(con_list)>0 or len(list_groups)>0:
				if log[len(log)-4:]==".txt":
					log=log[:len(log)-4]
				for directory in config.directory:
					hash_origen_c=config.adb_comm+" shell su 0 md5 /data/data/com.whatsapp/files/Logs/"+log
					hash_clonado_c=config.adb_comm+" shell su 0 md5 "+directory+log
					hash_origen=os.popen(hash_origen_c).read()
					hash_clonado=os.popen(hash_clonado_c).read()
					if "directory" in hash_origen or "directory" in hash_clonado:
						continue
					else:
						dict_final={"deleted_msg":texts,"dates_backup":times, "group_w":list_groups, "cons":con_list,"hash_origen":hash_origen, "hash_clonado":hash_clonado, "log":log}
						if dict_final not in log_list:
							log_list.append(dict_final)
						count_dict+=1
						break
		return log_list
	except:
		print config.error_alert[0]

def decompress(filename):
	comprimido=gzip.open(filename, "r");
	descomprimido=comprimido.read();
	txt = open(filename+".txt", "w")
	txt.write(descomprimido)
	txt.close()

def get_whatsappLog(log):
	try:
		for directory in config.directory:
			a = config.adb_comm+" shell su 0 dd if='/data/data/com.whatsapp/files/Logs/"+log+"' of='"+directory+log+"' bs=1000"
			Extract = config.adb_comm+" pull "+directory+log+" WhatsappLOG/"+log
			command = os.popen(a).read()
			if "directory" not in command:
				os.system(a)
				print 'USB debbuging active...'
				os.system(Extract)
				print'Extract whatsapp log...'
				return log
			print 'Change directory...'
	except :
		print config.error_alert[0]

def get_whatsappDB(db):
	try:
		for directory in config.directory:
			a = config.adb_comm+" shell dd if='"+directory+"WhatsApp/Databases/"+db+"' of='"+directory+db+"' bs=1000"
			print a
			Extract = config.adb_comm+" pull "+directory+db+"  WhatsappDB/"+db
			command = os.popen(a)
			command=command.read().replace("\r","").replace("\n","")
			if "file or directory" != command[len(command)-17:len(command)] and "unknown operand" not in command:
	#			os.system(a)
				print 'USB debbuging active...'
				os.system(Extract)
				print'Extract whatsapp db...'
				return db 
			print 'Change directory...'
	except :
		print config.error_alert[0]

def get_whatsappDB_root(db):
	try:
		for directory in config.directory:
			a = config.adb_comm+" shell su 0 dd if='/data/data/com.whatsapp/databases/"+db+"' of='"+directory+db+"' bs=1000"
			Extract = config.adb_comm+" pull "+directory+db+" WhatsappDB/"+db
			command = os.popen(a)
			command=command.read().replace("\r","").replace("\n","")
			if "file or directory" != command[len(command)-17:len(command)]:
	#			os.system(a)
				print 'USB debbuging active...'
				os.system(Extract)
				print'Extract whatsapp db...'
				return db 
			print 'Change directory...'
	except :
		print config.error_alert[0]

def set_permission_log(filename):
	print filename
	command = "chmod 777 WhatsappLOG/"+filename
	os.system(command)

def set_permission_db(filename):
	print filename
	command = "chmod 777 WhatsappDB/"+filename
	os.system(command)

def count_logs():
	command = config.adb_comm+" shell su 0 ls /data/data/com.whatsapp/files/Logs/"
	logs = os.popen(command).read()
	logs = logs.replace("\r","").split("\n")
	return logs

def count_dbs_root():
	command = config.adb_comm+" shell su 0 ls /data/data/com.whatsapp/databases"
	dbs = os.popen(command).read()
	dbs = dbs.replace("\r","").split("\n")
	return dbs

def count_dbs():
	for directory in config.directory:
		command = config.adb_comm+" shell ls "+directory+"WhatsApp/Databases/"
		dbs = os.popen(command).read()
		if "No such file or directory" in dbs:
			continue
		else:
			if "\n" in dbs:
				dbs = dbs.replace("\r","").split("\n")
				if len(dbs) <= 2 and dbs[1]=='':
					dbs = dbs[0].split(" ")
				return dbs
			else:
				dbs = dbs.split(" ")
return dbs

def create_dir_log():
	try:
		os.mkdir("WhatsappLOG")
		print 'The directory was created correctly'
	except:
		print 'Verify that the WhatsappLOG directory is created'

def create_dir_db():
	try:
		os.mkdir("WhatsappDB")
		print 'The directory was created correctly'
	except:
		print 'Verify that the WhatsappDB directory is created'

def create_dir_report():
	try:
		os.mkdir("Reports_Whatsapp_Forensic")
		print 'The directory was created correctly'
	except:
		print 'Verify that the Reports directory is created'

def create_dir_media():
	try:
		os.mkdir("Whatsapp_Extracted_Media")
		print 'The directory was created correctly'
	except:
		print 'Verify that the Media directory is created'


def get_hash_root(data, option):
	if option == "origin":
		command = config.adb_comm+" shell su 0 md5 /data/data/com.whatsapp/databases/"+data
		hash_ = os.popen(command).read()
		if "/sh" in hash_:
			md5 = modules.config.adb_comm+" shell su 0 md5sum /data/data/com.whatsapp/databases/"+data
			hash_ = os.popen(md5).read()
	elif option == "clone":
		for directory in config.directory:
			command = config.adb_comm+" shell md5 "+directory+data
			hash_ = os.popen(command).read()
			md5 = config.adb_comm+" shell md5sum "+directory+data
			hash_2 = os.popen(md5).read()
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

def get_hash(data, option):
	if option == "origin":
		for directory in config.directory:
			command = config.adb_comm+" shell md5 "+directory+"WhatsApp/Databases/"+data
			md5 = modules.config.adb_comm+" shell md5sum "+directory+"WhatsApp/Databases/"+data
			hash_ = os.popen(command).read()
			hash_2 = os.popen(md5).read()
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
		for directory in config.directory:
			command = config.adb_comm+" shell md5 "+directory+data
			hash_ = os.popen(command).read()
			md5 = modules.config.adb_comm+" shell md5sum "+directory+data
			hash_2 = os.popen(md5).read()
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

def create_report(t, list_dbs, info_root, whatsapp_log):
	text_final="Date of system: "+ str(t)+"\n"
	command = config.adb_comm+" shell date"
	time_device = os.popen(command).read()
	text_final+="Date of device: "+ str(time_device)+"\n\n"
	command = config.adb_comm+" shell getprop ro.build.versio.release"
	android_v = os.popen(command).read()
	text_final+="-----Device Information-----\n\n"
	text_final+="Android version: "+android_v
	#command = "adb shell "
	#TO/DO extract whatsapp version
	#whatsapp_v = os.popen(command).read()
	#text_final+="WhatsApp version: "+whatsapp_v
	for dbs in list_dbs:
		db_v = dbs["name"].split(".")
		db_v = db_v[len(db_v)-1]
		text_final += "DataBase version: "+db_v+"\n"
		text_final += "Database hashs--> Origin hash: "+dbs["hash_origen"]+ ", Clone hash: "+dbs["hash_clonado"]
	for i in range(len(info_root)):
		if i == 0:
			text_final+= "Root: "+info_root[i]+"\n"
		else:
			text_final+= "Root files: "+info_root[i]["file"]+", "+"Directory: "+info_root[i]["directory"]+", App used to root: "+info_root[i]["App"]+"\n"
	if whatsapp_log!=None:
		for log in whatsapp_log:
			msg_deleted=log["deleted_msg"]
			for msg in msg_deleted:
				text_final+=msg+"\n"
			text_final+="Log hash--> Origin hash: "+log["hash_origen"]+ ", Clone hash: "+log["hash_clonado"]
	t = t.split(",")[1].replace(" ","_")
	f = open (t+'_report_whatsapp_forensic.txt','w')
	f.write(text_final)
	f.close()
	print text_final

def banner():
	print config.banner
	print "------------------------------------------------------------------------------"
	print "[AUTHORS]: Jorge Coronado (aka @JorgeWebsec) | Ramon Bajona"
	print "[Email]: info@quantika14.com | [Twitter]: @QuantiKa14"
	print "[Version]: 1.0 | [Date]: 10-10-2017"
	print "------------------------------------------------------------------------------"
	print ""
