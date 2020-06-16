#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import os.path as osp
import hashlib
import modules.utils
import subprocess
from subprocess import Popen, PIPE

def check_directory():
	for directory in modules.utils.directory:
		direct = modules.utils.adb_comm +" shell ls "+directory+"WhatsApp/Media/"
		b,c = Popen(direct, stdout=PIPE, stderr=PIPE).communicate()
		b=b.decode('utf-8').replace("\r\n","")
		c=c.decode('utf-8').replace("\r\n","")
		if "No such file or directory" in b or "No such file or directory" in c:
			continue
		else:
			return directory

#extrae los archivos multimetidas de WhatsApp
def pull_media(directory):
	pull = subprocess.call(modules.utils.adb_comm + " pull "  + directory + "WhatsApp/Media Whatsapp_Extracted_Media/")

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

def get_subdirectoris(directory):
	ls_recursi = modules.utils.adb_comm+" shell ls -R "+directory+"WhatsApp/Media"
	letras=subprocess.Popen(ls_recursi, stdout=PIPE, stderr=PIPE).communicate()
	a, b = letras
	a=a.decode('utf-8')
	return a

def get_mdinfo(path, i):
	
	name =path+"/"+i
	
	if os.name == 'nt':
		name = name.replace(" ", "\\ ")
	else:
		name = name.replace(" ", "\\\\ ")
	md5 = modules.utils.adb_comm+" shell md5sum "+name 
	hash_ = subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode('latin-1').replace("\r\n","")
	print(hash_)
	if "/sh" not in hash_:
		return name, hash_.split(" ")
	else:
		md5 = modules.utils.adb_comm+" shell md5sum "+name
		hash_ = subprocess.Popen(md5, stdout=PIPE, stderr=PIPE).communicate()[0].decode('latin-1').replace("\r\n","")
		return name, hash_.split(" ")[0]


def extract_mm(root):
	md5_original=list()
	md5_cloned=list()
	files=list()
	on_rute=False
	on_file=False
	subdirectoris=list()
	directory = check_directory()
	pull_media(directory)

	PATH = 'Whatsapp_Extracted_Media/'
	""" Clone media data check """
	for path, dirs, files in os.walk(PATH):
		for fpath in [osp.join(path, f) for f in files]:
			md5 = filehash(fpath)
			name = osp.relpath(fpath, PATH)
			md5_original.append((name,md5))
	root.updateConsole("Finish hash cloned...")
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
	
	print("/////////////////////////////////////////////////////////////////////////")
	for directory in subdirectoris:
		path=directory[len(directory)-1]

		for f in directory:
			fi=f.split(" ")
			
			for fil in fi:
				name, md5 = get_mdinfo(path, fil)
				md5_cloned.append((name,md5))
			
		


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