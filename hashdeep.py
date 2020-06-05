#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, time
import os.path as osp
import hashlib
import modules.config, modules.functions
#importamos subprocess para cambiarlo por el os
import subprocess
from subprocess import Popen, PIPE
# poner como un try y except
# from Tkinter import *
from tkinter import *


def write(text):
    """ helper for writing output, as a single point for replacement """
    print(text)

# --- helpers ---
def filehash(filepath):
	blocksize = 64*1024
	md5 = hashlib.md5()
	with open(filepath, 'rb') as fp:
		while True:
			data = fp.read(blocksize)
			if not data:
				break
			md5.update(data)
	return md5.hexdigest()

#comprobar que las variables se corresponden de forma correcta
#comprobar whatsapp esta instalado
def check_directory():
	for directory in modules.config.directory:
		direct = modules.config.adb_comm+" shell ls "+directory+"WhatsApp/Media/"
		variables=Popen(direct, stdout=PIPE, stderr=PIPE).communicate()
		b,c = Popen(direct, stdout=PIPE, stderr=PIPE).communicate()
		b=b.decode('utf-8').split("\r\n")[0]
		c=c.decode('utf-8').split("\r\n")[0]
		if "No such file or directory" in b or "No such file or directory" in c:
			print("no se ha encontrado el directorio de Whatsapp en esta ubicacion")
			continue
		else:
			print("se ha encontrado el directorio")
			return directory

#comprobar que la funcion es correcta
def pull_media(directory):
	pull = modules.config.adb_comm+" pull "+directory+"WhatsApp/Media Whatsapp_Extracted_Media/"
	a = Popen(modules.config.adb_comm + " shell ls data", stdout=PIPE, stderr=PIPE)
	a = process.communicate()[0]
	print (pull)
	#a = os.popen(pull)
	#print (a.read())

def get_subdirectoris(directory):
	ls_recursi = modules.config.adb_comm+" shell ls -R "+directory+"WhatsApp/Media"
	a, b, c = os.popen3(ls_recursi)
	b = b.read()
	return b

def get_mdinfo(path, i):
	name =path+"/"+i
	if os.name == 'nt':
		name = name.replace(" ", "\\ ")
	else:
		name = name.replace(" ", "\\\\ ")
	md5 = modules.config.adb_comm+" shell md5 "+name
	hash_ = os.popen(md5).read()
	if "/sh" not in hash_:
		return name, hash_.split(" ")[0]
	else:
		md5 = modules.config.adb_comm+" shell md5sum "+name
		hash_ = os.popen(md5).read()
		return name, hash_.split(" ")[0]

def extract_mm(root):
	md5_original=list()
	md5_cloned=list()
	files=list()
	on_rute=False
	on_file=False
	subdirectoris=list()
	modules.functions.create_dir_media()
	directory = check_directory()

	#TODO ordenar este codigo
	if directory is not None:
		# --- /helpers ---

	#	write("""\
	#	%%%% HASH_CHECK
	#	%%%% size,sha256,filename
	#	##
	#	## Clone media hash check
	#	##""")
		pull_media(directory)
		mensaje_deb = "Creando hash y comparando... \n Este proceso varia su duracion en base a los archivos multimedia"
		root.updateConsole(mensaje_deb)
		PATH = 'Whatsapp_Extracted_Media/'
		""" Clone media data check """
		for path, dirs, files in os.walk(PATH):
			for fpath in [osp.join(path, f) for f in files]:
				md5 = filehash(fpath)
				name = osp.relpath(fpath, PATH)
	#			print ("---------------------")
	#			print ("MD5 [>] "+str(md5))
	#			print ("Path [>] "+str(name)) 
				md5_original.append((name,md5))
		print ("Finish hash cloned...")

	#	print ('\n')
	#	write("""\
	#	%%%% HASH_CHECK
	#	%%%% size,sha256,filename
	#	##
	#	## Original media hash check
	#	##""")

		ls=get_subdirectoris(directory)
		ls=ls.replace("\r", "").split("\n")

		for l in ls:
			if "/" in l and on_rute:
				if on_file:
					files.append(path.replace(":",""))
					subdirectoris.append(files)
					on_rute=False
					on_file=False
					files=[]
				else:
					on_rute=False
					on_file=False
					files=[]
				path=""
			if "/" in l:
				path = l
				on_rute=True
			elif "." in l and on_rute:
				file_l = l
				on_file=True
				files.append(file_l)
			else:
				continue

		for directory in subdirectoris:
			path=directory[len(directory)-1]
			for i in range(len(directory)-1):
				name, md5 = get_mdinfo(path, directory[i])
				md5_cloned.append((name,md5))
	#			print ("---------------------")
	#			print ("MD5 [>] "+str(md5))
	#			print ("Path [>] "+str(name))
		print ("Finish hash origin...")
		print ("Comparing...")
		for i in range(len(md5_cloned)):
			for has in md5_original:
				if has[1] == md5_cloned[i][1]:
					print ("-----------------------")
					print ("-------  Cloned  ------")
					print ("MD5 [>] "+str(md5_cloned[i][1]))
					print ("Path [>] "+str(md5_cloned[i][0]))
					print ("--------Original-------")
					print ("MD5 [>] "+str(has[1]))
					print ("Path [>] "+str(has[0]))
	#				time.sleep(1)
		return md5_cloned, md5_original
	
	else:
		print("No se ha encontrado el WhatsApp instalado")