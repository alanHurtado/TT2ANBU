###---------------- CONTROLADOR DE ANÁLISIS ----------------###

#:::: Este controlador se encarga de los procesos y código
# que están relacionados con el análisis de la publicaciones
# tanto para el análisis de arma con el análisis de rostro.


#:::::::::::::::::::: Configuración para el análisis de arma ::::::::::::::::::::#
from absl import app, logging
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
from distutils.dir_util import copy_tree
import time
import cv2
import numpy as np
import tensorflow as tf 
import os

# customize your API through the following parameters
classes_path = './data/labels/coco.names'
weights_path = '../../weights/yolov3.tf'
tiny = False                    # dejar en False dado que no se usa tiny yolo
size = 416                      # tamaño de las imagenes resultantes
num_classes = 1                # numero de clases del modelo

# load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

if tiny:
    yolo = YoloV3Tiny(classes=num_classes)
else:
    yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path).expect_partial()
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

from controllers.config import *
from model.Bd_conect import *
import urllib.request as req
import os
import requests
import time
import json
from os import listdir
from os.path import isfile, join

def getImages(idsProfiles,idSrch):
	try:
		dir_path = IMG_POSTS_PATH+str(idSrch)+"/"
		if not os.path.exists(dir_path):#Si la carpeta ya existe no la crea de nuevo
			os.mkdir(dir_path)

		for idProf in idsProfiles:
			posts = select_posts(idProf)
			for p in posts:
				imgurl =p[9]
				name = str(idProf)+"-"+str(p[0])+".jpg"
				img_path = dir_path+name
				req.urlretrieve(imgurl, img_path)#Se descarga la imagen, se guarda en img_path
				upd_img_path(p[0],img_path)#Se actualiza en la BD la ruta local de la foto
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
	# carga imagen por imagen y la manda a analizar
	for img in onlyfiles:
		s = str(img).replace('.jpg', '')
		datos = s.split("-")
		idPerfil = str(datos[0])
		idPublicacion = str(datos[1])
		IMAGE_PATH = mypath + "/" + img
		image = open(IMAGE_PATH, "rb").read()
		
		#################---BLOQUE AÑDIDO PARA TEST ("detecciones/")-----#################
		raw_images = []
		img_raw = tf.image.decode_image(image,channels=3)
		raw_images.append(img_raw)

		num = 0
		for j in range(len(raw_images)):
			# se arma el resultado
			responses = []
			raw_img = raw_images[j]
			num+=1
			img = tf.expand_dims(raw_img, 0)
			img = transform_images(img, size)

			t1 = time.time()
			boxes, scores, classes, nums = yolo(img)
			t2 = time.time()

			for i in range(nums[0]):
				responses.append({
					"arma": "SI",
					"porcentaje": float("{0:.2f}".format(np.array(scores[0][i])*100))
				})
			img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2BGR)
			img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
			final_path = DETECTIONS_PATH + str(id_srch) + "/"+idPerfil+"-" + idPublicacion + '.jpg'
			cv2.imwrite(final_path, img)
		#################:::::::::::::::::::::::::::#################

		data = responses
		#print(data)
		if not data:
			#print("no data")
			continue
		else:
			try:			
				new_data = str(data).replace("\'", "\"")
				dataObj = json.loads(new_data)		
				for obj in dataObj:
					if obj["arma"] == "SI":
						res = 1
						insert_arma(idPublicacion,obj["porcentaje"],res)
						upd_val_arma(idPublicacion,"1")
			except Exception as e:
				print("ERROR al ejecutar la funcion insert_arma() :"+str(e))			
				return False		
	return True

def insertaRostro(data):
	data_r = str(data)
	datos = data_r.split(",")
	cejas_arco = str(datos[0])
	labios_grandes = str(datos[1])
	nariz_grande = str(datos[2])
	cejas_pobladas = str(datos[3])
	barbilla_partida = str(datos[4])
	pomulos = str(datos[5])
	rostro_oval = str(datos[6])
	nariz_puntiaguda = str(datos[7])
	entradas = str(datos[8])
	idPublicacion = "213"#deberia ser datos[9] que viene desde el cliente, se pone dato ahora así para pruebas
	evaluacion_rostro = "1"
	try:
		tr = insert_rostro(cejas_arco,labios_grandes,nariz_grande,cejas_pobladas,
			barbilla_partida,pomulos,rostro_oval,nariz_puntiaguda,entradas,idPublicacion,
			evaluacion_rostro)
		#up = upd_val_arma(idPublicacion,"1")
		return True
	except Exception as e:
		print("ERROR al intentar insertar rostro: "+str(e))
		return False
		