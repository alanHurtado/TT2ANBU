###---------------- VALORES GENERALES DEL SISTEMA ----------------###

#:::: Componente donde se definen los valores estáticos y generales
# de todo el sistema como rutas de carpetas y variables de la API.

#:::::::::::::: APIFY ::::::::::::::#
#--BUILD_VERSION--#
#--> 0.2 (TEST)
#--> 0.1 (beta)
#--> 0.0 (latest)*
buildVersion = "latest"
#(TASKS ->  MY-TASK'Instagram Scrapper' -> Settings -> ID )
taskId = "L5Mh6z6wApo4dKk3B"
#(APIFY ACCOUNT -> INTEGRATIONS -> API TOKEN)
token = "DbBBmyEHGPeqY5bu5Etji5YG7"
#:::::::::::::::::::::::::::::::::::#

#::::::::::::: SISTEMA :::::::::::::#
IMG_POSTS_PATH = "tmp/post_img/"
DETECTIONS_PATH = './detecciones/'   # carpeta destino de los resultados

#::: Codigos de ERROR :::#
NO_PROFILES_FOUND = -2
#:::::::::::::::::::::::::::::::::::#