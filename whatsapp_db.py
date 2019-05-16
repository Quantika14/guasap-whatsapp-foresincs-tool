#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.config, modules.functions, parser_db, sqlite3
from Tkinter import *

def extract_db(pop_wait):
	count=1
	#List with dicts with DBS and their hash
	dbs_list=list()
	#Create directory to db
	modules.functions.create_dir_db()
	#Extract dbs names
	dbs = modules.functions.count_dbs()
	mensaje_deb = Label(pop_wait, text="Encontradas bases de datos, extrayendo...")
	mensaje_deb.place(x=20,y=80)
	pop_wait.update()
	for db in dbs:
		print "-------*-------"
		if db=="":
			pass
		else:
			#Extract db
			hash_origen = modules.functions.get_hash(db, "origin")
			db = modules.functions.get_whatsappDB(db)
			hash_clonado = modules.functions.get_hash(db, "clone")
			#Save data in dict
			name_d="dict_"+str(count)
			name_d={"name":db,"hash_o":hash_origen,"hash_d":hash_clonado}
			dbs_list.append(name_d)
			print "DB extract sucesfully [>] "+str(db)
			print "Original hash file[>] "+str(hash_origen)
			print "Cloned file hash [>] "+str(hash_clonado)
			count+=1
	return dbs_list

def extract_db_root(pop_wait):
	count=1
	#List with dicts with DBS and their hash
	dbs_list=list()
	#Create directory to db
	modules.functions.create_dir_db()
	#Extract dbs names
	dbs = modules.functions.count_dbs_root()
	mensaje_deb = Label(pop_wait, text="Encontradas bases de datos, extrayendo...")
	mensaje_deb.place(x=20,y=80)
	pop_wait.update()
	for db in dbs:
		print "-------*-------"
		if db=="":
			pass
		else:
			#Extract db
			hash_origen = modules.functions.get_hash_root(db, "origin")
			db = modules.functions.get_whatsappDB_root(db)
			hash_clonado = modules.functions.get_hash_root(db, "clone")
			#Save data in dict
			name_d="dict_"+str(count)
			name_d={"name":db,"hash_o":hash_origen,"hash_d":hash_clonado}
			dbs_list.append(name_d)
			print "DB extract sucesfully [>] "+str(db)
			print "Original hash file[>] "+str(hash_origen)
			print "Cloned file hash [>] "+str(hash_clonado)
			count+=1
	rows=parser_db.analyze_db()
	return dbs_list, rows

def count_messages(pop_wait):
	mensaje_num = Label(pop_wait, text="Calculando...")
	mensaje_num.place(x=20,y=120)
	pop_wait.update()
	conn = sqlite3.connect('WhatsappDB/msgstore.db')	
	total_msg = 0
	byConversation_messages={}
	for jid_msg in conn.execute('SELECT key_remote_jid FROM messages'):
		total_msg += 1
		peer = str(jid_msg[0]).replace("@s.whatsapp.net","")
		# Dict with number of messages with peers removing unnecessary chars 
		# i.e: ['phone_number' : 3 , 'phone_number': 50, 'phone_number': 24]
		if peer in byConversation_messages:
			byConversation_messages[peer] += 1
		else:
			byConversation_messages[peer] = 1
	conn.close()
	print "\nNúmero de mensajes totales: \n\t" ,total_msg
	print "\nNúmero de mensajes por conversacion: \n\t"
	print('\n'.join("{}: {}".format(conversation, num_msg) for conversation, num_msg in byConversation_messages.items()))
	return total_msg, byConversation_messages

def detect_breakID(total_msg):
	conn = sqlite3.connect('WhatsappDB/msgstore.db')
	cursor = conn.cursor()
	# Retrieved the first id in whatsapp db, build a list filled with contiguous IDs for later compare between them.
	# i.e:
	# 	first_id = 14
	# 	adjacents_id_list will be: [ 14, 15, 16, 17, ...]
	adjacents_id_list = []
	first_id = cursor.execute('SELECT _id FROM messages').fetchone()[0]
	adjacents_id_list.append(first_id)
	last_added = first_id
	removed_id = []
	for id in range(total_msg):
		last_added += 1
		adjacents_id_list.append(last_added)
	# msg_id_list is a list with the message _id stored in whatsapp db
	msg_id_list = [id[0] for id in cursor.execute('SELECT _id FROM messages')]
	conn.close()
	# a list with the removed _id message in whatsapp database
	removed_id = [id for id in adjacents_id_list if id not in msg_id_list]

	print "\nID eliminados: \n\t", removed_id
	return adjacents_id_list, msg_id_list, removed_id
