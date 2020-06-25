#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sqlite3, datetime

# FUNCTIONS #
# Analyze and extract all information from messages
def analyze_db():
	conn = sqlite3.connect('WhatsappDB/msgstore.db')	
	cursor = conn.cursor()
	rows=list()

	for row in cursor.execute('SELECT * FROM messages where edit_version=7 and key_from_me = 1 ORDER BY _id'):
		row_date=str(row[7])
		if len(row_date)>10:
			row_date = row_date[:len(row_date)-3]
		row_date=datetime.datetime.fromtimestamp(int(row_date)).strftime('%Y-%m-%d %H:%M:%S')
		text = "Numero de telefono de whatsapp borrado [>] "+ str(str(row[1]).split("@")[0]) + "\nTimestamp [>] "+row_date
		print (text)
		rows.append(text)

	cursor.close()
	conn.close()
	return rows

# Analyze and extract all information from messages of database file
def analyze_db_file(file):
	conn = sqlite3.connect(file)	
	cursor = conn.cursor()
	rows=list()

	for row in cursor.execute('SELECT * FROM messages where edit_version=7 and key_from_me = 1 ORDER BY _id'):
		row_date=str(row[7])
		if len(row_date)>10:
			row_date = row_date[:len(row_date)-3]
		row_date=datetime.datetime.fromtimestamp(int(row_date)).strftime('%Y-%m-%d %H:%M:%S')
		text = "Numero de telefono de whatsapp borrado [>] "+ str(str(row[1]).split("@")[0]) + "\nTimestamp [>] "+row_date
		print (text)
		rows.append(text)

	cursor.close()
	conn.close()
	return rows
