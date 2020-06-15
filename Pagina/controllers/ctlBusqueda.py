###---------------- CONTROLADOR DE BÚSQUEDA ----------------###

#:::: Este controlador realiza las solicitudes a la API
# del sítio APIFY.com para buscar y obtener los perfiles públicos
# de Instagram coincidentes con el nombre proporcionado.

from controllers.config import *
from model.Bd_conect import *
import requests
import json

def do_search(srch_name,srch_limit,no_posts):	
	dbSrchId = insertar_busqueda(srch_name)
	data = search_profiles(srch_name,srch_limit,no_posts)
	
	if not data:
		return False
	elif data == '[]':
		return NO_PROFILES_FOUND
	else:
		try:
			data = clean_txt_data(data)
			dataObj = json.loads(data)		
			ownerId = ""
			for obj in dataObj:
				#::::::::::::::: Insert para Perfil ::::::::::::::#
				if ownerId != obj['ownerId']:
					ownerId = obj['ownerId']
					username = obj['#debug']['userUsername']
					name = obj['#debug']['userFullName']
					url_profile="https://www.instagram.com/"+username
					dbProfId = insert_profile(username, name, url_profile)
					#:::: Insert para busqueda_perfil ::::#
					insert_srch_prof(dbSrchId,dbProfId)				
					#:::::::::::::::::::::::::::::::::::::#
				#:::::::::::::::::::::::::::::::::::::::::::::::::#

				#:::::::::::::::: Insert para Publicacion ::::::::::::::::#
				date = obj['timestamp']
				date = date.replace('T',' ')
				date = date.replace('.000Z','')

				url_Post = obj['url']
				url_Image = obj['displayUrl']
				location = obj['locationName']
				try:
					desc = obj['firstComment']
				except Exception as e:
					desc = ""
				insert_post(dbProfId,date,url_Post,desc,location,url_Image)						
				#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
			return dbSrchId
		except Exception as e:
			print("ERROR al ejecutar la funcion do_search() :"+str(e))			
			return False

def search_profiles(data_name,data_limit,data_posts):
	URL = ("https://api.apify.com/v2/actor-tasks/"+taskId+
		"/run-sync?token="+token+
		"&outputRecordKey=OUTPUT&build="+buildVersion)

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
	#rstatus_code = 201
	if r.status_code == 201:
		URL = (
			"https://api.apify.com/v2/actor-tasks/"+
			taskId+"/runs/last/dataset/items?token="+
			token+"&status=SUCCEEDED")
		
		answ = requests.get(url=URL,headers={'Content-Type':'application/json'})

		if answ.status_code == 200:
			return answ.text
	else:		
		return False

def clean_txt_data(inputString):
	inputString = inputString.replace('\n', '')
	inputString = inputString.replace('á', 'a')
	inputString = inputString.replace('é', 'e')
	inputString = inputString.replace('í', 'i')
	inputString = inputString.replace('ó', 'o')
	inputString = inputString.replace('ú', 'u')
	inputString = inputString.replace('ñ', 'n')
	return inputString.encode('ascii', 'ignore').decode('ascii')