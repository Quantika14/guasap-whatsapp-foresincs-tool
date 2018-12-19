import os

def check_dependencies():
	try:
		from Tkinter import *
	except:
		print "[MODULES][>] Para instalar Tkinter en Linux"
		print "puedes usar el siguiente comando:"
		print "sudo apt-get install python-tk"
		os.system('sudo apt-get install python-tk')
