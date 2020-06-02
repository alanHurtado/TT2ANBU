###---------------- CONTROLADOR DE ANÁLISIS ----------------###

#:::: Este controlador se encarga de los procesos y código
# que están relacionados con el análisis de la publicaciones
# tanto para el análisis de arma con el análisis de rostro.

from controllers.config import *
from model.Bd_conect import *
import urllib.request as req

def getImages(idsProfiles):
	try:
		for idProf in idsProfiles:
			posts = select_posts(idProf)
			for p in posts:
				imgurl =p[9]
				name = str(idProf)+"-"+str(p[0])+".jpg"
				path = IMG_PROFILES_DIR+name
				req.urlretrieve(imgurl, path)
				upd_img_path(p[0],path)
		return True
	except Exception as e:
		print("ERROR al ejecutar la funcion getImages() :"+str(e))
		return False