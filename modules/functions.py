#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.utils as utils, modules.functions, os, GuasApp_Forensic,gzip
import subprocess
from subprocess import Popen, PIPE, STDOUT
import getpass
import sqlite3

#FORENSIC FUNCTIONS

def extract_deleted_messages():
	try:
		log_list=list()
		for log in utils.analyze_logs:
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
								if text not in texts:
									texts.append(text)
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
								if text not in texts:
									texts.append(text)
						else:
							if line not in texts:
								texts.append(line)

				if "msgstore/backupdb\n" in line:
					time_backup = line.split(" ")
					time_backup = time_backup[0]+" "+time_backup[1]
					print ("Backup DBs on time [>] "+time_backup)
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
					print ("Group [>] "+subject+"\nNum creator [>] "+num_creator+" | Date creation [>] "+str(date_creation)+"\n Subject [>] "+subject+"| Subject owner num [>] "+subject_owner+" Subject time [>] "+str(subject_time)+"\n Users [>] "+str(users))
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

					print ("Time of change network [>] "+time_con)
					print ("Tipo: "+type_pri+", Estado: "+state_pri+", Nombre: "+extra_pri)
					print ("Tipo: "+type_sec+", Estado: "+state_sec+", Nombre: "+extra_sec) 
					con_dict={"time":time_con,"first_change":{"state":state_pri, "name":extra_pri},"second_change":{"state":state_sec, "name":extra_sec}}
					if con_dict not in con_list:
						con_list.append(con_dict)
				count += 1

			if int(c_messages)>=0 or len(times)>0 or len(con_list)>0 or len(list_groups)>0:
				if log[len(log)-4:]==".txt":
					log=log[:len(log)-4]
				for directory in utils.directory:
					hash_origen_c=utils.adb_comm+" shell su 0 md5 /data/data/com.whatsapp/files/Logs/"+log
					hash_clonado_c=utils.adb_comm+" shell su 0 md5 "+directory+log
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
		print (utils.error_alert[0])


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
	try:
		#no puede utilizar la aplicacion en windows por error de permiso
		if modules.utils.adb_comm == "c:\\adb\\adb":
			a = modules.utils.adb_comm+" shell cd data/data/adb && dir"
			b = modules.utils.adb_comm+" shell cd data/adb && dir"
		else:
			a = modules.utils.adb_comm+" shell cd data/data/adb && ls"
			b = modules.utils.adb_comm+" shell cd data/adb && ls"
		a = subprocess.Popen(a, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('latin-1')
		b = subprocess.Popen(b, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('latin-1')
		
		if "magisk" in a or "magisk" in b:
			return {"directory":"data/adb","App":"Magisk","file":"magisk_debug.log"}
		else:
			return False
	except:
		return False

#Aquí comprobamos a través de un comando si el dispositivo dispone de permisos de root.
def check_su():
	global root_posibility
	try:
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
	except IOError:
		root_posibility=False
		return "No adb installed"

def get_whatsappDB(db):
	try:
		for directory in utils.directory:
			a = utils.adb_comm+" shell dd if='"+directory+"WhatsApp/Databases/"+db+"' of='"+directory+db+"' bs=1000"
			extract = utils.adb_comm+" pull "+directory+db+" WhatsappDB/"+db
			#command = os.popen(a)
			command=subprocess.Popen(a, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			command=command.replace("\r","").replace("\n","")
			if "file or directory" != command[len(command)-17:len(command)] and "unknown operand" not in command:
	#			os.system(a)
				print ('USB debbuging active...')
				os.system(extract)
				print ('extract whatsapp db...')
				return db 
			print ('Change directory...')
	except :
		return utils.error_alert[0]


def get_whatsappDB_root(db):
	
	try:
		copy=utils.adb_comm+" shell su 0 cp '/data/data/com.whatsapp/databases/"+db+"' '/sdcard/"+db+"'"
		#a = utils.adb_comm+" shell su 0 dd if='/data/data/com.whatsapp/databases/"+db+"' of='"+directory+db+"' bs=1000"
		extract = utils.adb_comm+" pull /sdcard/"+db+" WhatsappDB/"+db
		subprocess.call(copy)
		subprocess.call(extract)	
		return db 
	except :
		print (utils.error_alert[0]) 


def create_dir_media():
	try:
		os.mkdir("Whatsapp_extracted_Media")
		print ('The directory was created correctly')
	except:
		print ('Verify that the Media directory is created')

def create_dir_db():
	try:
		os.mkdir("WhatsappDB")
		print ('The directory was created correctly')
	except:
		print ('Verify that the WhatsappDB directory is created')

def create_dir_report():
	try:
		os.mkdir("Reports_Guasap_Forensic")
		print ('The directory was created correctly')
	except:
		print ('Verify that the Reports directory is created')
	
def create_dir_log():
	try:
		os.mkdir("WhatsappLOG")
		print ('The directory was created correctly')
	except:
		print ('Verify that the WhatsappLOG directory is created')



def decompress(filename):
	comprimido=gzip.open(filename, "r")
	descomprimido=comprimido.read().decode("utf-8")
	txt = open(filename+".txt", "w")
	txt.write(descomprimido)
	txt.close()

def get_whatsappLog(log):
	try:
		for directory in utils.directory:
			a = utils.adb_comm+" shell su 0 dd if='/data/data/com.whatsapp/files/Logs/"+log+"' of='"+directory+log+"' bs=1000"
			extract = utils.adb_comm+" pull "+directory+log+" WhatsappLOG/"+log
			command=subprocess.Popen(a, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			if "directory" not in command:
				print ('USB debbuging active...')
				subprocess.call(extract)
				print('extract whatsapp log...')
				return log
			print ('Change directory...')
	except :
		print (utils.error_alert[0])


def set_permission_log(filenames):
	username=getpass.getuser()
	if utils.adb_comm=="c:\\adb\\adb":
		command = "Icacls WhatsappLOG/"+ filenames+" /grant "+ username +":f"
	else:
		command = "chmod 777 WhatsappLOG/"+filenames
	subprocess.call(command)

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

def count_logs():
	command = utils.adb_comm+" shell su 0 ls /data/data/com.whatsapp/files/Logs/"
	logs=subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
	logs = logs.replace("\r","").split("\n")
	
	return logs

# To know the members that belong to a group, this function receives the identified "gjid" of the group
def get_members(group):
	conn = sqlite3.connect('WhatsappDB/msgstore.db')
	group_members_raw = [member[0] for member in conn.execute('SELECT jid FROM group_participants WHERE gjid=?', (group[0],))]
	conn.close()
	# Once retrieved all group members in raw format "34697XXXXXX@s.whatsapp.net" each one must be cleaned
	group_members = [clean_user(member) for member in group_members_raw]
	return group_members

# A simple function for remove preffix and suffix added by Whatsapp to the user "jid"
def clean_user(peer):
	user = str(peer[2:]).replace("@s.whatsapp.net","")
	return user

# Parsing important data from msgstore.db structure header (first 100 bytes of *.db file) to try restore deleted messages
def db_head_parser(db,root):
	# In the SQLite official site the are stored the specifications doc 
	# with the offset in the header of sqlite file about the data stored and lenght (offset - n bytes)
	db_info = []
	db_dump = open(db, "rb")
	db_dump.seek(16)
	page_size_raw = db_dump.read(2)
	db_dump.seek(28)
	number_pages_raw = db_dump.read(4)
	db_dump.seek(32)
	first_trunk_page_raw = db_dump.read(4)
	db_dump.seek(96)
	db_ver_raw = db_dump.read(4)
	# Converting hex to decimal
	first_trunk_page=first_trunk_page_raw.hex()
	#first_trunk_page = int(first_trunk_page_raw.encode("hex"), 16)
	db_ver = db_ver_raw.hex()
	#db_ver = int(db_ver_raw.encode("hex"), 16)
	#page_size = page_size_raw.encode("hex"), 16)
	page_size = page_size_raw.hex()
	number_pages = number_pages_raw.hex()

	#number_pages = int(number_pages_raw.encode("hex"), 16)
	db_info.extend((page_size, number_pages, first_trunk_page, db_ver))

	


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

def get_hash_root(data, option):
	if option == "origin":
		command = utils.adb_comm+" shell su 0 md5 /data/data/com.whatsapp/databases/"+ data
		hash_ = subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
		if "not found" in hash_:
			md5 = modules.utils.adb_comm+" shell su 0 md5sum /data/data/com.whatsapp/databases/"+ data
			hash_= subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")

	elif option == "clone":
		for directory in utils.directory:
			command = utils.adb_comm+" shell md5 "+ directory + data
			hash_ = subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
			md5 = utils.adb_comm+" shell md5sum "+directory + data
			hash_2 = subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
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

def count_dbs_root():
	command = utils.adb_comm+" shell su 0 ls /data/data/com.whatsapp/databases"
	dbs=subprocess.Popen(command, stdout=PIPE, stderr=PIPE).communicate()[0].decode("latin-1")
	dbs = dbs.replace("\r","").split("\n")
	return dbs