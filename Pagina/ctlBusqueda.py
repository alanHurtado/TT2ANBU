####----Controlador de Búsqueda------#####
# ---Este controlador realiza solicitudes a la API del sítio APIFY.com para 
# buscar y obtener perfiles públicos de Instagram. La búsqueda se realiza con
# base en un nombre proporcionado.

import requests

actorTaskId = "PE7drWyJCrT9z2wj8"
token = "RR2h79SdNi6nrWecwM5XGAutQ"

def search_profiles(srch_name,srch_limit):
	URL = "https://api.apify.com/v2/actor-tasks/"+actorTaskId+"/run-sync?token="+token+"&outputRecordKey=OUTPUT/"	
	data = """{
	    "search": """+'"'+srch_name+'"'+""",
	    "searchType": "user",
	    "searchLimit": """+srch_limit+""",
	    "resultsType": "posts",
	    "resultsLimit": 3,
	    "proxy":{
	      "useApifyProxy": true,
	      "apifyProxyGroups": []
	    }
	}"""	
	r = requests.post(url=URL,data=data,headers={'Content-Type':'application/json'})	
	if r.status_code == 201:
		URL = "https://api.apify.com/v2/actor-tasks/"+actorTaskId+"/runs/last/dataset/items?token="+token+"&status=SUCCEEDED"
		answ_json = requests.get(url=URL,headers={'Content-Type':'application/json'})
		if answ_json.status_code == 200:
			return answ_json.json()
	else:
		return False

