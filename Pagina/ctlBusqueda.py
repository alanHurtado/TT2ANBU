####----Controlador de Búsqueda------#####
# ---Este controlador realiza solicitudes a la API del sítio APIFY.com para 
# buscar y obtener perfiles públicos de Instagram. La búsqueda se realiza con
# base en un nombre proporcionado.

from config import *
from model.Bd_conect import *
import requests
import json

def do_search(srch_name,srch_limit):	
	dbSrchId = insertar_busqueda(srch_name)
	##########DESCOMENTAR línea en fase de pruebas y muestra#######
	#data = search_profiles(srch_name,srch_limit).replace('\n', '')
	#############################################################
	data = jsonTEST().replace('\n', '')
	
	if not data:
		return False
	else:
		try:
			dataObj = json.loads(data)
			for obj in dataObj:
				#--Insert para Perfil--#
				username = obj['username']
				name = obj['fullName']
				url=obj['#debug']['url']
				dbProfId = insert_profile(username, name, url)
				#----------------------#

				#--Insert para busqueda_perfil-----#
				insert_srch_prof(dbSrchId,dbProfId)				
				#----------------------#

				#--Insert para Publicacion--#
				for post in obj['latestPosts']:
					if not post['type']=='Video':
						date = post['timestamp']
						date = date.replace('T',' ')
						date = date.replace('.000Z','')									
						url = post['displayUrl']
						desc = post['caption']
						location = post['locationName']
						##########DESCOMENTAR línea en fase de pruebas y muestra#######
						#insert_post(dbProfId,date,url,desc,location)					
						################################################################	
						insert_post(dbProfId,date,"https://scontent-mad1.com","Lorem ipsum dolor sit amet",location)						
				#----------------------#
			return dbSrchId
		except Exception as e:
			print("Errore ::"+str(e))
			return False

def search_profiles(data_name,data_limit):
	URL = "https://api.apify.com/v2/actor-tasks/"+actorTaskId+"/run-sync?token="+token+"&outputRecordKey=OUTPUT/"	
	data = """{
	    "search": """+'"'+data_name+'"'+""",
	    "searchType": "user",
	    "searchLimit": """+data_limit+""",
	    "resultsType": "posts",
	    "resultsLimit": 3,
	    "proxy":{
	      "useApifyProxy": true,
	      "apifyProxyGroups": []
	    }
	}"""	
	#r = requests.post(url=URL,data=data,headers={'Content-Type':'application/json'})	
	rstatus_code = 201
	if rstatus_code == 201:
		URL = "https://api.apify.com/v2/actor-tasks/"+actorTaskId+"/runs/last/dataset/items?token="+token+"&status=SUCCEEDED"
		answ = requests.get(url=URL,headers={'Content-Type':'application/json'})
		if answ.status_code == 200:
			return answ.text
	else:
		return False


def jsonTEST():
	jsonTxt = """[{
  "#debug": {
    "url": "https://www.instagram.com/josephinelangford/",
    "loadedUrl": "https://www.instagram.com/josephinelangford/",
    "method": "GET",
    "retryCount": 0,
    "errorMessages": null
  },
  "id": "855729540",
  "username": "josephinelangford",
  "fullName": "Josephine Langford",
  "biography": "",
  "externalUrl": null,
  "externalUrlShimmed": null,
  "followersCount": 2301923,
  "followsCount": 0,
  "hasChannel": false,
  "highlightReelCount": 0,
  "isBusinessAccount": false,
  "joinedRecently": false,
  "businessCategoryName": null,
  "private": false,
  "verified": true,
  "profilePicUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s150x150/67437893_410724122872871_3758488617593339904_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=tWeLsQ3myaUAX_RVbj0&oh=e11045a6f2d8e400ebc5426fff6356c2&oe=5EA866CA",
  "profilePicUrlHD": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s320x320/67437893_410724122872871_3758488617593339904_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=tWeLsQ3myaUAX_RVbj0&oh=6a18ec6b2bc529a4fc736542991d7d16&oe=5EA6D2BA",
  "facebookPage": null,
  "igtvVideoCount": 0,
  "latestIgtvVideos": [],
  "postsCount": 26,
  "latestPosts": [
    {
      "type": "Image",
      "shortCode": "BwL0vfRnd1k",
      "caption": "ContentMode.",
      "commentsCount": 15429,
      "dimensionsHeight": 1080,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/56191689_311853672837178_5702585242739437692_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=rPOY9ukWKjUAX-ad4L_&oh=429b736008dfb4af6213e6b0a0e39eb6&oe=5EA60F0D",
      "likesCount": 712472,
      "timestamp": "2019-04-13T05:55:41.000Z",
      "locationName": null
    },
    {
      "type": "Sidecar",
      "shortCode": "BwLH2xTHuhi",
      "caption": "Refinery29.",
      "commentsCount": 7677,
      "dimensionsHeight": 720,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/54513726_363339687601437_2446177610303881050_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=N1PKOap_qHwAX9EQhjx&oh=b63d4f26be35e97cac98c5e3d3c870e5&oe=5EA6158D",
      "likesCount": 671810,
      "timestamp": "2019-04-12T23:23:27.000Z",
      "locationName": null
    },
    {
      "type": "Sidecar",
      "shortCode": "Bv_1mltBD8V",
      "caption": "Harper’s Bazaar Australia.",
      "commentsCount": 12986,
      "dimensionsHeight": 1350,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/56197345_402088343912486_4064785882761823036_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=102&_nc_ohc=myi1gh38PVoAX_9fiwM&oh=ec3d7d1a60e0f32a882b00ad1a09be7e&oe=5EA6DEDE",
      "likesCount": 774024,
      "timestamp": "2019-04-08T14:12:19.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BuokViDHo84",
      "caption": "",
      "commentsCount": 15575,
      "dimensionsHeight": 1080,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/52670260_325197604799815_8164818005908535459_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=wEPzhJZT1m0AX9q4dAx&oh=b644a3647a3f3d76248e3f49b2387285&oe=5EA7E0C8",
      "likesCount": 746951,
      "timestamp": "2019-03-05T16:47:31.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BugSmLPnFl7",
      "caption": "Mardi Gras.",
      "commentsCount": 1966,
      "dimensionsHeight": 810,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/52461713_2141778719274842_6618536428119995448_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=102&_nc_ohc=qtfcaAkpry4AX9hZ6Kt&oh=a6e1334e515b0cd201073237d5991ea2&oe=5EA6D244",
      "likesCount": 279371,
      "timestamp": "2019-03-02T11:38:34.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BrQbWd7Hkgg",
      "caption": "",
      "commentsCount": 4141,
      "dimensionsHeight": 1350,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/47308276_2145999805638718_5005058227752179156_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=jcDFZaawCF0AX9U-Uwb&oh=959bcce9af96c4ace94d02f9f31ba53d&oe=5EA60341",
      "likesCount": 368686,
      "timestamp": "2018-12-11T18:13:02.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BqAupxynRya",
      "caption": "",
      "commentsCount": 5814,
      "dimensionsHeight": 1080,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/45414929_335820630330870_157047547203612144_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=106&_nc_ohc=cnJT0mpbK1IAX_gy5o4&oh=27cedf95477176ef9bd12af2992e1a60&oe=5EA77342",
      "likesCount": 672198,
      "timestamp": "2018-11-10T19:22:27.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BmKA8WFgj2c",
      "caption": "Tessa & Hardin. #AfterMovie",
      "commentsCount": 13185,
      "dimensionsHeight": 720,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/37804090_1228801870594733_6996563194755940352_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=105&_nc_ohc=gU0mfX3QaW8AX8KFeMC&oh=667a663c59ceccc60810d15424643030&oe=5EA7C211",
      "likesCount": 956576,
      "timestamp": "2018-08-06T23:49:52.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BjlK2rFAtz2",
      "caption": "Rocks.",
      "commentsCount": 133,
      "dimensionsHeight": 1350,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/32931625_372768079876773_4855946821505122304_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=mHtCnwyOY1MAX_8hpLM&oh=0cebd891a519d37832fd879fe1342be8&oe=5EA7BF47",
      "likesCount": 109490,
      "timestamp": "2018-06-03T23:21:47.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BfPWR0OHt67",
      "caption": "Being pensive.",
      "commentsCount": 291,
      "dimensionsHeight": 1255,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/28151578_2016599741929907_8883528802483830784_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=5WEborAQwiwAX_-TfaQ&oh=42c914b58ad439c3b2ac52c4b0cee762&oe=5EA53AAB",
      "likesCount": 151708,
      "timestamp": "2018-02-16T01:52:45.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BefKfL6nGUj",
      "caption": "",
      "commentsCount": 126,
      "dimensionsHeight": 810,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/26263570_2019855681594801_8617030127626223616_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=gKCkolin6T4AX9cOqI2&oh=df168fae188f33a81826aaa41e563783&oe=5EA621CC",
      "likesCount": 99036,
      "timestamp": "2018-01-28T08:46:10.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "BWyRsm6FyVW",
      "caption": "I found Radiator Springs. Have been location scouting for CARS - the live action musical. #2018",
      "commentsCount": 84,
      "dimensionsHeight": 701,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/20067337_465800093786823_2957051697299456000_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=103&_nc_ohc=6TfvZxpMU6cAX8OnX_I&oh=2311e7e557ba87f47e535911dd922486&oe=5EA4EBCC",
      "likesCount": 84956,
      "timestamp": "2017-07-20T22:43:35.000Z",
      "locationName": null
    }]
    },
	{
	  "#debug": {
	    "url": "https://www.instagram.com/josejosetlmd/",
	    "loadedUrl": "https://www.instagram.com/josejosetlmd/",
	    "method": "GET",
	    "retryCount": 0,
	    "errorMessages": null
	  },
	  "id": "5601297367",
	  "username": "josejosetlmd",
	  "fullName": "José José",
	  "biography": "La serie sobre la vida del Príncipe de la Canción 🎼 #JoseJose",
	  "externalUrl": "http://www.Telemundo.com/JoseJose",
	  "externalUrlShimmed": "https://l.instagram.com/?u=http%3A%2F%2Fwww.Telemundo.com%2FJoseJose&e=ATOQ3Ok3ErlBedkdyn5JLG2R0W2864X0oHNlcefR82qaC4msdxXje7HZvCqJBJZH3GCv0E6q&s=1",
	  "followersCount": 30000,
	  "followsCount": 41,
	  "hasChannel": false,
	  "highlightReelCount": 10,
	  "isBusinessAccount": true,
	  "joinedRecently": false,
	  "businessCategoryName": "Content & Apps",
	  "private": false,
	  "verified": true,
	  "profilePicUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-19/s150x150/25006976_1696641333732389_6267348559020949504_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_ohc=PXWgilX9tVUAX_jYJyB&oh=4be827a91c6f0396b416a77a55e63c2b&oe=5EA84AFC",
	  "profilePicUrlHD": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-19/s320x320/25006976_1696641333732389_6267348559020949504_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_ohc=PXWgilX9tVUAX_jYJyB&oh=bdba539dafdfacd474a4655e48a292ae&oe=5EA4BF84",
	  "facebookPage": null,
	  "igtvVideoCount": 0,
	  "latestIgtvVideos": [],
	  "postsCount": 423,
	  "latestPosts": [
	    {
	      "type": "Image",
	      "shortCode": "BhQBWh9A8ld",
	      "caption": "Así cerramos una serie llena de enseñanzas, buena música, lecciones de vida y amor al arte. Felicidades a todo el elenco👏👏👏Despídete de la serie con un mensaje aquí 👇",
	      "commentsCount": 503,
	      "dimensionsHeight": 1080,
	      "dimensionsWidth": 1080,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/29417639_921762604660216_7425763528662843392_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=104&_nc_ohc=7VJhES5fkyoAX9e6MCs&oh=4b4771de970d22efb53d59df70226100&oe=5EA70FAC",
	      "likesCount": 6802,
	      "timestamp": "2018-04-07T01:11:55.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Video",
	      "shortCode": "BhQASvzgt03",
	      "caption": "De esta manera tan emotiva termina la serie #JoséJosé envíale tus mensajes al Príncipe de la Canción.",
	      "commentsCount": 251,
	      "dimensionsHeight": 360,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e15/30084079_443729042723003_4271875047850770432_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=111&_nc_ohc=rxMAvWFgtpsAX9oP_XG&oh=b27c5546e1b8e3abc42f9653779a184b&oe=5E7F2FE1",
	      "likesCount": 3608,
	      "videoViewCount": 31915,
	      "timestamp": "2018-04-07T01:03:33.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Video",
	      "shortCode": "BhP9ylgAkii",
	      "caption": "El Príncipe de la Canción hace una dura reflexión que nos deja un gran aprendizaje. Estas viendo el Gran Final de #JoséJosé por @telemundo",
	      "commentsCount": 81,
	      "dimensionsHeight": 360,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e15/29416439_1933710456942191_5823959929500729344_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=111&_nc_ohc=D5AVQ6bQLLIAX_NJxws&oh=70a02b4138f9fb24d78ef1ae1131cdde&oe=5E7FB360",
	      "likesCount": 1821,
	      "videoViewCount": 22479,
	      "timestamp": "2018-04-07T00:43:02.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Video",
	      "shortCode": "BhP7U-SAJ10",
	      "caption": "Sarita llamó por teléfono al Príncipe de la Canción para contarle que estaba esperando un hijo de él. Estas viendo el Gran Final de #JoseJose @malillanymarin @alexdelamadrid",
	      "commentsCount": 27,
	      "dimensionsHeight": 360,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e15/30084506_190540518402502_3480068913113333760_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=110&_nc_ohc=cMI4veaQZaoAX_JFDUo&oh=bd37df594897a602b21ab50a4a493142&oe=5E7FA001",
	      "likesCount": 1114,
	      "videoViewCount": 15298,
	      "timestamp": "2018-04-07T00:21:39.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhPy8hdgO6J",
	      "caption": "Palabras de @alexdelamadrid: ・・・\nMe quedo con un enorme aprendizaje , con una oportunidad única e irrepetible y con una experiencia que me llevo en el corazón por siempre ! 👑 \n#YoenPrincipe \n#finalJoséJosé \nGRACIAS",
	      "commentsCount": 45,
	      "dimensionsHeight": 1348,
	      "dimensionsWidth": 1080,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/29737751_985240811625019_7883354751742509056_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=107&_nc_ohc=9OFK_VAU0bwAX-D9kpq&oh=c3d2b0ad38d867207d35da84a7742a41&oe=5EA7AA5B",
	      "likesCount": 1574,
	      "timestamp": "2018-04-06T23:06:02.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Video",
	      "shortCode": "BhPknGwgyOd",
	      "caption": "¿Qué hace con su vida un cantante que queda sin voz 😢? Te esperamos esta noche en el Gran Final de #JoséJosé 8/7C.",
	      "commentsCount": 31,
	      "dimensionsHeight": 607,
	      "dimensionsWidth": 1080,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/fr/e15/s1080x1080/29740073_1809264202714107_7962756735561629696_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=103&_nc_ohc=sFrH2jjTMeMAX-SFYBJ&oh=8e97002687ea7cfaeb595bcb8b558721&oe=5E7FB3EF",
	      "likesCount": 956,
	      "videoViewCount": 12507,
	      "timestamp": "2018-04-06T21:04:23.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhPAOkLAoA4",
	      "caption": "La original y la ficción. ¿Se parecen?  Te esperamos esta noche en el Gran Final de José José a las 8/7C por @telemundo",
	      "commentsCount": 108,
	      "dimensionsHeight": 640,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/29417870_599318037072319_8803244297374662656_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=107&_nc_ohc=WOOSEsa2giAAX8zeKb_&oh=4df962e0ef72acf1f5082fde33cd0a5d&oe=5EA5E3E1",
	      "likesCount": 1467,
	      "timestamp": "2018-04-06T15:42:51.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhNfzu-Ay8a",
	      "caption": "Mañana minutos antes del capítulo final de #JoséJosé conéctate con @alexdelamadrid y pregúntale lo que quieras 😱😱😱 te esperamos a partir de la 7:30 pm por aquí 👇",
	      "commentsCount": 14,
	      "dimensionsHeight": 640,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/30084519_455688648182305_8796875449285214208_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=101&_nc_ohc=uzLxtGwG1Q8AX9QVC5B&oh=7a496bea5706b686492dd17a863fcf1c&oe=5EA70379",
	      "likesCount": 670,
	      "timestamp": "2018-04-06T01:40:19.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhNXuskAkG9",
	      "caption": "Junto a un gran hombre. Siempre hay una gran mujer . Sarita la mujer que le aposto al amor . @malillanymarin . @alexdelamadrid  no se pierdan la historia",
	      "commentsCount": 43,
	      "dimensionsHeight": 1080,
	      "dimensionsWidth": 1080,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/29714964_436061696837129_3141450337127235584_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=105&_nc_ohc=1cdp_8yoSxkAX_0tT3Z&oh=16a25e5373f3d9bf355b2346f876acb6&oe=5EA53701",
	      "likesCount": 1611,
	      "timestamp": "2018-04-06T00:29:44.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhNVl_SgkbC",
	      "caption": "No se pierdan hoy @josejosetlmd ! @malillanymarin @alexdelamadrid ! #Tbt",
	      "commentsCount": 17,
	      "dimensionsHeight": 1080,
	      "dimensionsWidth": 1080,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/30086177_336422876878986_3028045818780188672_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=106&_nc_ohc=cXJ6SP3isZEAX-XYrFK&oh=68aeb4143901bd39132591e499feb20b&oe=5EA58D7B",
	      "likesCount": 1220,
	      "timestamp": "2018-04-06T00:11:04.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Image",
	      "shortCode": "BhM531Dg4Ms",
	      "caption": "Miren quién estará con nosotros esta noche antes del capítulo de José José @malillanymarin 👏👏👏Ten listas tus preguntas y no te pierdas el capítulo de hoy.",
	      "commentsCount": 19,
	      "dimensionsHeight": 640,
	      "dimensionsWidth": 640,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/29737014_1661815953886624_7289107685167857664_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=104&_nc_ohc=GbcGc0lMDioAX88pBBq&oh=0ed19810df5b42706bc167c1755da9a2&oe=5EA4F0D5",
	      "likesCount": 535,
	      "timestamp": "2018-04-05T20:08:50.000Z",
	      "locationName": null
	    },
	    {
	      "type": "Video",
	      "shortCode": "BhMhL69geNw",
	      "caption": "¿Quieres saber cuál es la comida favorita del Príncipe de la Canción? No te pierdas esta viernes el final de José José",
	      "commentsCount": 38,
	      "dimensionsHeight": 750,
	      "dimensionsWidth": 750,
	      "displayUrl": "https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e15/30077738_353736058472691_7466735197384343552_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=103&_nc_ohc=OIQ-SJMmCmUAX-uFIer&oh=0ffc45c83c5c26dcff8ae8f6f0f943fb&oe=5E7F8EB8",
	      "likesCount": 777,
	      "videoViewCount": 12358,
	      "timestamp": "2018-04-05T16:33:19.000Z",
	      "locationName": null
	    }
	  ]
	},
	{
	  "#debug": {
	    "url": "https://www.instagram.com/_jose_coronado/",
	    "loadedUrl": "https://www.instagram.com/_jose_coronado/",
	    "method": "GET",
	    "retryCount": 0,
	    "errorMessages": null
	  },
	  "id": "5561060457",
	  "username": "_jose_coronado",
	  "fullName": "Jose Coronado",
	  "biography": "",
	  "externalUrl": "http://majos.es/",
	  "externalUrlShimmed": "https://l.instagram.com/?u=http%3A%2F%2Fmajos.es%2F&e=ATPi2-Dx7tI4I86ByWmtAKfbKXhJ0A6zvED1FST5EHhwjBGmFeA-5dwEkw3UI01Mo7xKlSvh&s=1",
	  "followersCount": 100973,
	  "followsCount": 337,
	  "hasChannel": false,
	  "highlightReelCount": 0,
	  "isBusinessAccount": true,
	  "joinedRecently": false,
	  "businessCategoryName": "Creators & Celebrities",
	  "private": false,
	  "verified": true,
	  "profilePicUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s150x150/47475847_389115641848351_3562524751823896576_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=aT-mmzOOZ8QAX9n_CKx&oh=601b6fc645dc34ff6c51ed81be968ba0&oe=5EA6E4FC",
	  "profilePicUrlHD": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s320x320/47475847_389115641848351_3562524751823896576_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=aT-mmzOOZ8QAX9n_CKx&oh=f13776c1f79e5f3325ce9744563f3127&oe=5EA8080C",
	  "facebookPage": null,
	  "igtvVideoCount": 0,
	  "latestIgtvVideos": [],
	  "postsCount": 75,
	  "latestPosts": [
    {
      "type": "Image",
      "shortCode": "B-KxcxQl2Yx",
      "caption": "Esta noche estaré con @joseramondelamorena en @ondacero #eltransistor \n#yomequedoencasa \n#muchoanimo",
      "commentsCount": 132,
      "dimensionsHeight": 564,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/90486230_2690243957754986_336767002106591910_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=102&_nc_ohc=lPZKNxVNggkAX_jN_VT&oh=02c7ae8c6429f1630d2626c0436a2fd7&oe=5EA71A8A",
      "likesCount": 2700,
      "timestamp": "2020-03-25T19:27:11.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B92BaVxKju9",
      "caption": "#yomequedoencasa \n@landroverspain @landrover @belenlacalle #landroverphotos",
      "commentsCount": 143,
      "dimensionsHeight": 1241,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/90090303_237609374056439_4102371040249465279_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=UvLaBmFxSBwAX-AimTk&oh=1a387f80c69686bed28b524616adaa06&oe=5EA74F35",
      "likesCount": 3701,
      "timestamp": "2020-03-17T18:02:37.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B9zkStnqRu5",
      "caption": "#yomequedoencasa \nEspero que disfrutéis mucho con el final de VIVIR SIN PERMISO!  En estos días tan horribles por los que estamos pasando.\n\nANIMO 😊🙏",
      "commentsCount": 2103,
      "dimensionsHeight": 937,
      "dimensionsWidth": 750,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/89823073_147879660087160_1420089380853418314_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&_nc_ohc=tcgMxQqKyAoAX8Tswjw&oh=910328796a937cc5894380a59c35d812&oe=5EA5A9A4",
      "likesCount": 19438,
      "timestamp": "2020-03-16T19:09:41.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B9rN0a2q9WS",
      "caption": "#yomequedoencasa",
      "commentsCount": 300,
      "dimensionsHeight": 1068,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/89610288_144188070214077_15772284714280098_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=CwPAn98GUHAAX9zOP25&oh=81e6bddcdd6900311bc24dc96a36f0b0&oe=5EA4A608",
      "likesCount": 9071,
      "timestamp": "2020-03-13T13:19:23.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B9pSrOWqnjs",
      "caption": "#yomequedoencasa",
      "commentsCount": 308,
      "dimensionsHeight": 1072,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/89672290_504998483741920_5143325279056946918_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&_nc_ohc=X7jQlfHM-jcAX9CDUsM&oh=90574178c0a398326d882b28b71424db&oe=5EA4DD30",
      "likesCount": 13030,
      "timestamp": "2020-03-12T19:23:20.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B9H3i6TK9sw",
      "caption": "#Repost @nacholopezfotografo with @get_repost\n・・・\nJose Coronado (@_jose_coronado) Gigantes en Movistar+ (@gigantesserie) Majós (@majos.mm) #seriesmovistar #series #GigantesLaSerie #nacholopez #canon #love #fashion #beautiful #followme #instadaily #repost #nature #girl #style #smile #igers #tagsforlikes #life #beauty #amazing #instagram #photography #photo #canon #bestoftheday  #photooftheday © copyright todas las imagenes\n\nMuchas gracias @nacholopezfotografo por esos instantes! 🙏🏼",
      "commentsCount": 976,
      "dimensionsHeight": 1328,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/84336408_2636961616629291_742282269946932819_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=103&_nc_ohc=Xf29YXi7N0cAX98zaqm&oh=a4d3f3b0c5a1634eb8f97a25901cb897&oe=5EA5FE36",
      "likesCount": 15816,
      "timestamp": "2020-02-28T19:51:20.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B9BpjEZIvXk",
      "caption": "Me gusta la aventura.\nMe gusta que me siga. \nMe gusta mojarme.\nMe gusta!\n\n@landroverspain @landrover @belenlacalle #landrover #aventura #invierno #conducir #extremadura #campo",
      "commentsCount": 140,
      "dimensionsHeight": 514,
      "dimensionsWidth": 640,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/84028812_208576653855408_8211019192047350345_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=100&_nc_ohc=_p2BUZNWyMQAX8a4r18&oh=982bbc4602e13d9a4791db8a90793f3c&oe=5EA67E86",
      "likesCount": 5309,
      "timestamp": "2020-02-26T09:53:35.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B8_a-R7IY6n",
      "caption": "Muy Agradecido por la audiencia en Telecinco y Netflix.\nVIVIR SIN PERMISO T2 \n@mediasetcom @alea_media @netflixes @ficcionproducciones Una semana mas!! GRACIAS GRACIAS GRACIAS\n\n#vivirsinpermiso \n#series #seriesespañolas #ficcion",
      "commentsCount": 2772,
      "dimensionsHeight": 1350,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/84455854_2458837911033034_3360337251446456271_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=0kXscY71rWQAX-O5RUc&oh=b256384e177aa162dc803adf3c19b647&oe=5EA55519",
      "likesCount": 22674,
      "timestamp": "2020-02-25T13:07:44.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B8ycyxNIhCZ",
      "caption": "Calentado motores.\nEstreno 23 de noviembre.\n\nWAY DOWN @balaguerojaume \n@telecincocinema \n#cine",
      "commentsCount": 214,
      "dimensionsHeight": 688,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/82871575_522969601690962_2281657932179948754_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=106&_nc_ohc=8FR8aJNBLdQAX-G0EoK&oh=3ecdf5e3485504ef9879103c749138ab&oe=5EA74647",
      "likesCount": 5464,
      "timestamp": "2020-02-20T12:13:31.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B8weEbgIzIT",
      "caption": "Feliz rodando EL INOCENTE de Oriol Paulo. Hoy rodando con Victor García. Pedazo de serie para @netflixes \n#series #seriesnetflix #pedazodeserie #ficcionespañola. @uripaulo",
      "commentsCount": 468,
      "dimensionsHeight": 1349,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/84981504_638879333558086_2752904187143771129_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=gbYqEnCQsZIAX951LPx&oh=85c6fecb063745caa990d59b9cb3083e&oe=5EA6CEA0",
      "likesCount": 8090,
      "timestamp": "2020-02-19T17:46:11.000Z",
      "locationName": null
    },
    {
      "type": "Video",
      "shortCode": "B8pLmSwoTjq",
      "caption": "MAÑANA LUNES un capítulo mas de @vspserie en T5\nVIVIR SIN PERMISO 2T.\n\n@telecincoes @alea_media @ficcionproducciones @mediasetcom \n#ficcionespañola #tvseries",
      "commentsCount": 1202,
      "dimensionsHeight": 600,
      "dimensionsWidth": 480,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/84458323_498069737577955_5322431928519546997_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=jMnhVLX-2AAAX8T_reh&oh=63b33a0c2676e79435abc3117754a497&oe=5E7FA6CE",
      "likesCount": 11491,
      "videoViewCount": 58631,
      "timestamp": "2020-02-16T21:51:30.000Z",
      "locationName": null
    },
    {
      "type": "Image",
      "shortCode": "B8BOZB0Id2N",
      "caption": "Siguiendo las huellas... Maravilla de invierno.\n\n@landroverspain @landrover @belenlacalle #landrover #invierno #conducir #seguridad #disfrutar",
      "commentsCount": 182,
      "dimensionsHeight": 1349,
      "dimensionsWidth": 1080,
      "displayUrl": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/83824996_2603099799744195_4166161042464614609_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=103&_nc_ohc=kkpzP5hgmGQAX8ebZw4&oh=d2e6cd05906e8b1433fb8d7b48c524fd&oe=5EA6E724",
      "likesCount": 4182,
      "timestamp": "2020-02-01T09:24:53.000Z",
      "locationName": null
    }
  	]
	}]"""
	return jsonTxt
