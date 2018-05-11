#!/usr/bin/env python
#-*- coding:utf-8 -*-
analyze_logs=[]

directory=["/storage/external_SD/","/sdcard/", "/storage/sdcard0/", "/storage/self/primary/"]

error_alert = ["No device connected or can not connect to device..."]

dicts_root=[{"app":"kingroot","version":"2.2","marca":"all","observaciones":"Cuenta con versión de PC"},{"app":"kingoroot","version":"1.5","marca":"all","observaciones":"De algunas marcas solo permite rootear determinados teléfonos(https://es.kingoapp.com/dispositivos.htm)"},{"app":"odin","version":"all","marca":"samsumg", "observaciones":"Realiza un flasheo únicamente a los terminales Samsung y funciona desde el PC, además de necesitar arrancar el bootloader en el terminal."}]

dicts_root=[{"app":"kingroot","version":"2.2","marca":"all","observaciones":"Cuenta con versión de PC"},{"app":"kingoroot","version":"1.5","marca":"all","observaciones":"De algunas marcas solo permite rootear determinados teléfonos(https://es.kingoapp.com/dispositivos.htm)"},{"app":"odin","version":"Cualquiera","marca":"Samsung","observaciones":"Realiza un flasheo únicamente a los terminales Samsung y funciona desde el PC, además necesitará arrancar el bootloader en el terminal."},{"app":"framaroot","version":"4.0","marca":"Ver lista en la web","observaciones":"Funciona a base de exploits encontrados en determinados procesadores, por lo cual cubre algunos dispositivos en determinadas versiones. Ver dispositivos compatibles: http://framaroot.net/devices.html"},{"app":"towelroot","version":"Hasta 4.4","marca":"Aquellos terminales lanzados antes del 3 de Junio de 2014","observaciones":"(https://towelroot.com/)"},{"app":"srsroot","version":"1.5","marca":"all","observaciones":"Las versiones exactas de Android que soporta son 1.5, 2.1, 2.2, 2.3, 3.1, 3.2, 4.x, 5.x, 6.x"},{"app":"root master","version":"desconocido","marca":"all","observaciones":"En la página web no viene indicada desde que versión de Android soporta"}, {"app":"","version":"","marca":"","observaciones":""},{"app":"universal root","version":"1.6","marca":"mirar lista en la pagina web","observaciones":"(http://universalandrootdl.com/)"},{"app":"easy root toolkit","version":"desconocido","marca":"mirar ista en la pagina web","observaciones":"(https://forum.xda-developers.com/showthread.php?t=2327472) Se usa con un ordenador Linux"},{"app":"z4root","version":"4.0","marca":"all","observaciones":"Permite ejecutar la aplicación con un equipo externo o desde el mismo dispositivo (https://www.z4root.info/)"}]

banner = """

 __          __  _               _                                       
 \ \        / / | |             | |                                      
  \ \  /\  / /  | |__     __ _  | |_   ___    __ _   _ __    _ __        
   \ \/  \/ /   | '_ \   / _` | | __| / __|  / _` | | '_ \  | '_ \       
    \  /\  /    | | | | | (_| | | |_  \__ \ | (_| | | |_) | | |_) |      
     \/  \/     |_| |_|  \__,_|  \__| |___/  \__,_| | .__/  | .__/       
                                                    | |     | |          
                                                    |_|     |_|          
   __                                       _                            
  / _|                                     (_)                           
 | |_    ___    _ __    ___   _ __    ___   _    ___       _ __    _   _ 
 |  _|  / _ \  | '__|  / _ \ | '_ \  / __| | |  / __|     | '_ \  | | | |
 | |   | (_) | | |    |  __/ | | | | \__ \ | | | (__   _  | |_) | | |_| |
 |_|    \___/  |_|     \___| |_| |_| |___/ |_|  \___| (_) | .__/   \__, |
                                                          | |       __/ |
                                                          |_|      |___/ 
"""

##COMANDOS WINDOWS
adb_w="c:\\adb\\adb"

##COMANDOS LINUX
adb_l="adb"

##GLOBAL
adb_comm=""

