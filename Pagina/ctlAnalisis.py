####----Controlador de Analisis------#####
# ---

from config import *
from model.Bd_conect import *
import urllib.request as req

def getImages(idsProfiles):
	for idProf in idsProfiles:
		posts = select_posts(idProf)
		for p in posts:
			imgurl =p[4]			
			name = str(idProf)+"-"+str(p[0])+".jpg"
			path = IMG_PROFILES_DIR+name
			req.urlretrieve(imgurl, path)
			upd_img_path(p[0],path)