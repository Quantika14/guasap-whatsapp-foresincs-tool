#!/usr/bin/env python
#-*- coding:utf-8 -*-
analyze_logs=[]

directory=["/storage/external_SD/","/sdcard/", "/storage/sdcard0/", "/storage/self/primary/"]

error_alert = ["No device connected or can not connect to device..."]

dicts_root=[{"app":"kingroot","version":"2.2","marca":"all","observaciones":"Cuenta con versión de PC"},{"app":"kingoroot","version":"1.5","marca":"all","observaciones":"De algunas marcas solo permite rootear determinados teléfonos(https://es.kingoapp.com/dispositivos.htm)"},{"app":"odin","version":"Cualquiera","marca":"Samsung","observaciones":"Realiza un flasheo únicamente a los terminales Samsung y funciona desde el PC, además necesitará arrancar el bootloader en el terminal."},{"app":"framaroot","version":"4.0","marca":"Ver lista en la web","observaciones":"Funciona a base de exploits encontrados en determinados procesadores, por lo cual cubre algunos dispositivos en determinadas versiones. Ver dispositivos compatibles: http://framaroot.net/devices.html"},{"app":"towelroot","version":"Hasta 4.4","marca":"Aquellos terminales lanzados antes del 3 de Junio de 2014","observaciones":"(https://towelroot.com/)"},{"app":"srsroot","version":"1.5","marca":"all","observaciones":"Las versiones exactas de Android que soporta son 1.5, 2.1, 2.2, 2.3, 3.1, 3.2, 4.x, 5.x, 6.x"},{"app":"root master","version":"desconocido","marca":"all","observaciones":"En la página web no viene indicada desde que versión de Android soporta"},{"app":"universal root","version":"1.6","marca":"mirar lista en la pagina web","observaciones":"(http://universalandrootdl.com/)"},{"app":"easy root toolkit","version":"desconocido","marca":"mirar ista en la pagina web","observaciones":"(https://forum.xda-developers.com/showthread.php?t=2327472) Se usa con un ordenador Linux"},{"app":"z4root","version":"4.0","marca":"all","observaciones":"Permite ejecutar la aplicación con un equipo externo o desde el mismo dispositivo (https://www.z4root.info/)"},{"app":"vroot","version":"4.0","marca":"all","observaciones":""},{"app":"root master","version":"4.0","marca":"all","observaciones":""},{"app":"easy rooting toolkit","version":"4.0","marca":"all","observaciones":"Requiere un PC con Windows"},{"app":"baidu root","version":"4.0","marca":"all","observaciones":""},{"app":"wondershare mobilego","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"root genius","version":"4.0","marca":"all","observaciones":""},{"app":"tunesgo root","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"ping pong root","version":"desconocido","marca":"all","observaciones":""},{"app":"howtoroot","version":"desconocida","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"iroot","version":"4.0","marca":"all","observaciones":""},{"app":"dr.fone root","version":"4.0","marca":"all","observaciones":"Requiere de PC con Windows"},{"app":"oneclickroot","version":"desconocida","marca":"all","observaciones":""},{"app":"weaksauce","version":"desconocida","marca":"all","observaciones":""},{"app":"supersu pro root","version":"3.0","marca":"all","observaciones":""},{"app":"superuser x","version":"desconocida","marca":"all","observaciones":""}]
banner = """

     _____                                   
    |  __ \                                 
    | |  \/ _   _   __ _  ___   __ _  _ __  
    | | __ | | | | / _` |/ __| / _` || '_ \ 
    | |_\ \| |_| || (_| |\__ \| (_| || |_) |
     \____/ \__,_| \__,_||___/ \__,_|| .__/ 
                                     | |    
                                     |_|    
   __                                       _                            
  / _|                                     (_)                           
 | |_    ___    _ __    ___   _ __    ___   _    ___       _ __    _   _ 
 |  _|  / _ \  | '__|  / _ \ | '_ \  / __| | |  / __|     | '_ \  | | | |
 | |   | (_) | | |    |  __/ | | | | \__ \ | | | (__   _  | |_) | | |_| |
 |_|    \___/  |_|     \___| |_| |_| |___/ |_|  \___| (_) | .__/   \__, |
                                                          | |       __/ |
                                                          |_|      |___/ 
"""

css="""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Guasap Forensic Report</title>
<style>
body {
	background-color: #F4F4F4;
	font-family: sans-serif;
}
h1 {
	color: black;
	font-family: sans-serif;
	font-size: 300%;
	text-align: center;
	border-bottom: 2px solid black;
}
h2 {
	color: black;
	font-family: sans-serif;
	font-size: 150%;
	text-align: center;
	border-bottom: 2px solid black;
	width:10%;
	margin-left:45%;
}
h3 {
	color: black;
	font-family: sans-serif;
}
p {
	color: black;
	font-size: 100%;
	line-height: 100%;

}

p.cabecera{
border-bottom: 1px solid #000000; /**Línea inferior**/
margin-top:5%;

padding:0 0 2px; 
font-size:160%; /**Tamaño del texto**/
line-height:1.9em; /**Altura del recuadro**/
}
p.cabecera{
color: #000000; /**Color del título**/
text-align: center; /**centrar título**/
}
p.subcabecera{
border-bottom: 1px solid #000000; /**Línea inferior**/
margin-top:5%;
padding:0 0 2px; 
font-size:100%; /**Tamaño del texto**/
line-height:1.9em; /**Altura del recuadro**/
}
p.subcabecera{
color: #000000; /**Color del título**/
text-align: center; /**centrar título**/
}

hr { 
   border: 2px solid #5c3566; 
   border-radius: 200px /8px; 
   height: 0px; 
   text-align: center; 
   margin: 3%
 } 

p.aversion {
	color: black;
}

p.hash {
	color: #555753;
	line-height: 130%;
}

p.messages {
	color: #2e3436;
}
#list{
	display: none;
}
#list_media{
	display: none;
}
#list_dbs{
	display: none;
}
#list_dbs_root{
	display: none;
}
.botonlog{
            text-decoration: none !important;
            padding: 7px;
            font-weight: 600;
            font-size: 15px;
            color: #ffffff !important;
            background-color: #7d70af;
            border-radius: 6px;
            border: 2px solid #746ead;
            margin-bottom: 5%;
}
.botonlog:hover{
	background-color: #8F86B1;
}
#boton_ {
            text-decoration: none !important;
            padding: 7px;
            font-weight: 600;
            font-size: 15px;
            color: #ffffff !important;
            background-color: #7d70af;
            border-radius: 6px;
            border: 2px solid #746ead;
            margin-bottom: 5%;
          }
#boton_:hover{
	background-color: #8F86B1;
}
#boton_media {
            text-decoration: none !important;
            padding: 7px;
            font-weight: 600;
            font-size: 15px;
            color: #ffffff !important;
            background-color: #7d70af;
            border-radius: 6px;
            border: 2px solid #746ead;
            margin-bottom: 5%;
          }
#boton_media:hover{
	background-color: #8F86B1;
}
#boton_dbs {
            text-decoration: none !important;
            padding: 7px;
            font-weight: 600;
            font-size: 15px;
            color: #ffffff !important;
            background-color: #7d70af;
            border-radius: 6px;
            border: 2px solid #746ead;
            margin-bottom: 5%;
          }
#boton_dbs:hover{
	background-color: #8F86B1;
}
#boton_dbs_root {
            text-decoration: none !important;
            padding: 7px;
            font-weight: 600;
            font-size: 15px;
            color: #ffffff !important;
            background-color: #7d70af;
            border-radius: 6px;
            border: 2px solid #746ead;
            margin-bottom: 5%;
          }
#boton_dbs_root:hover{
	background-color: #8F86B1;
}

</style>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js">
</script>
<script>
function listar(){
        if ($("#list").css("display")=="none"){
          $("#list").show();
          $(boton_).text('Show less');
        }
        else{
          $("#list").hide();
          $(boton_).text('Show all');

            }
      };
function listar_media(){
        if ($("#list_media").css("display")=="none"){
          $("#list_media").show();
          $(boton_media).text('Show less');
        }
        else{
          $("#list_media").hide();
          $(boton_media).text('Show all');
            }
      };
function listar_dbs(){
        if ($("#list_dbs").css("display")=="none"){
          $("#list_dbs").show();
          $(boton_dbs).text('Show less');
        }
        else{
          $("#list_dbs").hide();
          $(boton_dbs).text('Show all');
            }
      };
function listar_dbs_root(){
        if ($("#list_dbs_root").css("display")=="none"){
          $("#list_dbs_root").show();
          $(boton_dbs_root).text('Show less');
        }
        else{
          $("#list_dbs_root").hide();
          $(boton_dbs_root).text('Show all');
            }
      };
</script>
</head>

<body>"""

##COMANDOS WINDOWS
adb_w="c:\\adb\\adb"

##COMANDOS LINUX
adb_l="adb"

##GLOBAL
adb_comm=""
