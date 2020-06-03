###---------------- CONTROLADOR DE ANÁLISIS ----------------###

#:::: Este controlador se encarga de los procesos y código
# que están relacionados con el análisis de la publicaciones
# tanto para el análisis de arma con el análisis de rostro.

from controllers.config import *
from model.Bd_conect import *
import urllib.request as req
import os

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