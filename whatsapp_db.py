#!/usr/bin/env python
#-*- coding:utf-8 -*-
import modules.config, modules.functions, parser_db

def extract_db():
	count=1
	#List with dicts with DBS and their hash
	dbs_list=list()
	#Create directory to db
	modules.functions.create_dir_db()
	#Extract dbs names
	dbs = modules.functions.count_dbs()
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

def extract_db_root():
	count=1
	#List with dicts with DBS and their hash
	dbs_list=list()
	#Create directory to db
	modules.functions.create_dir_db()
	#Extract dbs names
	dbs = modules.functions.count_dbs_root()
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
