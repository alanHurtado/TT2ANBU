###---------------- CONTROLADOR DE ANÁLISIS ----------------###

#:::: Este controlador se encarga de los procesos y código
# que están relacionados con el análisis de la publicaciones
# tanto para el análisis de arma con el análisis de rostro.

from controllers.config import *
from model.Bd_conect import *
import urllib.request as req
import os
import requests
import time
import random
import string
import json
from os import listdir
from os.path import isfile, join

def getImages(idsProfiles,idSrch):
	try:
		dir_path = IMG_PROFILES_DIR+str(idSrch)+"/"
		if not os.path.exists(dir_path):
			os.mkdir(dir_path)

		for idProf in idsProfiles:
			posts = select_posts(idProf)
			for p in posts:
				imgurl =p[9]
				name = str(idProf)+"-"+str(p[0])+".jpg"
				img_path = dir_path+name
				req.urlretrieve(imgurl, img_path)
				upd_img_path(p[0],img_path)
		return True
	except Exception as e:
		print("ERROR al ejecutar la funcion getImages() :"+str(e))
		return False

def creaCarpeta(id_srch):
	dir_det = "./detecciones/" + str(id_srch) #path que guarda las detecciones
	dir_st = "./static/detecciones/" + str(id_srch)#copia del path pasado a mostrar en la pagina de resultados
	if not os.path.exists(dir_det):
		os.mkdir(dir_det)
	if not os.path.exists(dir_st):
		os.mkdir(dir_st)

def analisisArma(id_srch):
	mypath = "./tmp/post_img/" + str(id_srch) #carpeta de imagenes descargadas por busqueda
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] #lista de esas imagenes
	API_URL = "http://0.0.0.0:8000/detections/" + str(id_srch)
	# carga imagen por imagen y la manda a analizar
	for img in onlyfiles:
		s = str(img).replace('.jpg', '')
		datos = s.split("-")
		idPerfil = str(datos[0])
		idPublicacion = str(datos[1])
		IMAGE_PATH = mypath + "/" + img
		image = open(IMAGE_PATH, "rb").read()
		payload = {"images": image}
		data = requests.post(API_URL, files=payload).json()
		print(data)
		if not data:
			print("no data")
		else:
			try:
				new_data = str(data).replace("\'", "\"")
				dataObj = json.loads(new_data)		
				for obj in dataObj:
					if obj["arma"] == "SI":
						res = 1
						insert_arma(idPublicacion,obj["porcentaje"],res)
			except Exception as e:
				print("ERROR al ejecutar la funcion do_search() :"+str(e))			
				return False		
	return True
		

def randomString(stringLength=5): #para nombres de imagenes, de otro modo se reemplazan y desaparecen
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

