#!/usr/bin/env python
#-*- coding:utf-8 -*-

directory=["/storage/external_SD/","/sdcard/", "/storage/sdcard0/", "/storage/self/primary/"]

error_alert = ["No device connected or can not connect to device..."]

dicts_root=[{"app":"kingroot","version":"2.2","marca":"all","observaciones":"Cuenta con versión de PC"},{"app":"kingoroot","version":"1.5","marca":"all","observaciones":"De algunas marcas solo permite rootear determinados teléfonos(https://es.kingoapp.com/dispositivos.htm)"},{"app":"odin","version":"Cualquiera","marca":"Samsung","observaciones":"Realiza un flasheo únicamente a los terminales Samsung y funciona desde el PC, además necesitará arrancar el bootloader en el terminal."},{"app":"framaroot","version":"4.0","marca":"Ver lista en la web","observaciones":"Funciona a base de exploits encontrados en determinados procesadores, por lo cual cubre algunos dispositivos en determinadas versiones. Ver dispositivos compatibles: http://framaroot.net/devices.html"},{"app":"towelroot","version":"Hasta 4.4","marca":"Aquellos terminales lanzados antes del 3 de Junio de 2014","observaciones":"(https://towelroot.com/)"},{"app":"srsroot","version":"1.5","marca":"all","observaciones":"Las versiones exactas de Android que soporta son 1.5, 2.1, 2.2, 2.3, 3.1, 3.2, 4.x, 5.x, 6.x"},{"app":"root master","version":"desconocido","marca":"all","observaciones":"En la página web no viene indicada desde que versión de Android soporta"},{"app":"universal root","version":"1.6","marca":"mirar lista en la pagina web","observaciones":"(http://universalandrootdl.com/)"},{"app":"easy root toolkit","version":"desconocido","marca":"mirar ista en la pagina web","observaciones":"(https://forum.xda-developers.com/showthread.php?t=2327472) Se usa con un ordenador Linux"},{"app":"z4root","version":"4.0","marca":"all","observaciones":"Permite ejecutar la aplicación con un equipo externo o desde el mismo dispositivo (https://www.z4root.info/)"},{"app":"vroot","version":"4.0","marca":"all","observaciones":""},{"app":"root master","version":"4.0","marca":"all","observaciones":""},{"app":"easy rooting toolkit","version":"4.0","marca":"all","observaciones":"Requiere un PC con Windows"},{"app":"baidu root","version":"4.0","marca":"all","observaciones":""},{"app":"wondershare mobilego","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"root genius","version":"4.0","marca":"all","observaciones":""},{"app":"tunesgo root","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"ping pong root","version":"desconocido","marca":"all","observaciones":""},{"app":"howtoroot","version":"desconocida","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"iroot","version":"4.0","marca":"all","observaciones":""},{"app":"dr.fone root","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"oneclickroot","version":"desconocida","marca":"all","observaciones":""},{"app":"weaksauce","version":"desconocida","marca":"all","observaciones":""},{"app":"supersu pro root","version":"3.0","marca":"all","observaciones":""},{"app":"superuser x","version":"desconocida","marca":"all","observaciones":""}]

analyze_logs=[]

##COMANDOS WINDOWS
adb_w="c:\\adb\\adb"

##COMANDOS LINUX
adb_l="adb"

##GLOBAL
adb_comm=""
