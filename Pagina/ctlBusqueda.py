####----Controlador de Búsqueda------#####
# ---Este controlador realiza solicitudes a la API del sítio APIFY.com para 
# buscar y obtener perfiles públicos de Instagram. La búsqueda se realiza con
# base en un nombre proporcionado.

from config import *
from model.Bd_conect import *
import requests
import json

def do_search(srch_name,srch_limit,no_posts):	
	dbSrchId = insertar_busqueda(srch_name)
	data = search_profiles(srch_name,srch_limit,no_posts)
	if not data:
		return False
	else:
		try:
			data = clean_txt_data(data)
			dataObj = json.loads(data)		
			ownerId = ""
			for obj in dataObj:
				#--Insert para Perfil--#
				if ownerId != obj['#debug']['userId']:
					ownerId = obj['#debug']['userId']
					username = obj['#debug']['userUsername']
					name = obj['#debug']['userFullName']
					url=obj['#debug']['url']
					dbProfId = insert_profile(username, name, url)
					#---Insert para busqueda_perfil---#
					insert_srch_prof(dbSrchId,dbProfId)				
					###################################
				############################

				#--Insert para Publicacion--#
				date = obj['timestamp']
				date = date.replace('T',' ')
				date = date.replace('.000Z','')

				urlPost = obj['url']
				urlImage = obj['imageUrl']
				location = obj['locationName']
				try:
					desc = obj['firstComment']
				except Exception as e:
					desc = ""
				insert_post(dbProfId,date,urlPost,desc,location,urlImage)						
				############################
			return dbSrchId
		except Exception as e:
			print("ERROR al ejecutar la funcion do_search() :"+str(e))			
			return False

def search_profiles(data_name,data_limit,data_posts):
	URL = "https://api.apify.com/v2/actor-tasks/"+taskId+"/run-sync?token="+token+"&outputRecordKey=OUTPUT/"	
	data = """{
	    "search": """+'"'+data_name+'"'+""",
	    "searchType": "user",
	    "searchLimit": """+data_limit+""",
	    "resultsType": "posts",
	    "resultsLimit": """+data_posts+""",
	    "extendOutputFunction": "($) => { return {} }",
	    "proxy":{
	      "useApifyProxy": true,
	      "apifyProxyGroups": []
	    }
	}"""

	r = requests.post(url=URL,data=data,headers={'Content-Type':'application/json'})
	
	if r.status_code == 201:
		URL = "https://api.apify.com/v2/actor-tasks/"+taskId+"/runs/last/dataset/items?token="+token+"&status=SUCCEEDED"
		answ = requests.get(url=URL,headers={'Content-Type':'application/json'})
		if answ.status_code == 200:
			return answ.text
	else:		
		return False

def result_data_for_view(id_srch):
	try:
		data_prof=select_profiles_by_srch(id_srch)
		data = list()
		for prof in data_prof:
			profiles = list()
			data_post=select_posts(prof[0])
			posts = list(data_post)
			profiles.append(prof)
			profiles.append(posts)
			data.append(profiles)
		return data
	except Exception as e:
		print("ERROR recuperando los datos de la búsqueda result_data_for_view(): "+str(e))
	return False

def clean_txt_data(inputString):
	inputString = inputString.replace('\n', '')
	return inputString.encode('ascii', 'ignore').decode('ascii')
	