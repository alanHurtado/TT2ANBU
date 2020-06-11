###---------------- CONTROLADOR PRINCIPAL DEL SISTEMA ----------------###

#:::: Este controlador procesa todas las peticiones que
# recibe la página del sistema, se encarga de redirigir al
# usuario a las secciones correspondientes y también de ejecutar
# el código para la lógica del negocio.
from datetime import *
from controllers.ctlBusqueda import *
from controllers.ctlAnalisis import *
from controllers import formulario
from controllers.generarpdf import *
import pdfkit
from flask import Flask
from flask import render_template  # Permite renderizar templates (Archivos HTML)
from flask import Flask, Response, jsonify, send_from_directory, abort, request, redirect, url_for, flash  # Permite manejo de los datos del formulario
from flask import render_template, make_response  # Permite renderizar templates (Archivos HTML)
from flask import request, redirect, url_for, flash  # Permite manejo de los datos del formulario
from model.Bd_conect import *  # Funciones del modelo para uso de la base de datos
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
weights_path = './weights/yolov3.tf'
tiny = False                    # dejar en False dado que no se usa tiny yolo
size = 416                      # tamaño de las imagenes resultantes
output_path = './detecciones/'   # carpeta destino de los resultados
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


app = Flask(__name__)
app.secret_key = 'anotherSecretKey'

@app.route('/')
def index():
    return render_template('home.html') # se agrega rende_template para usar el template

@app.route('/busqueda', methods = ['GET', 'POST']) # indicamos solocitudes get y post en la pagina   
def busqueda(): # accedemos al atributo method POST = enviar GET = mostrar
    coment_form = formulario.ComentFormBus(request.form)    # generamos la instacia al formulario
    if request.method == 'POST' and coment_form.validate():    #   si se reciben datos
        error = None
        in_name = coment_form.in_name.data
        no_profiles = coment_form.no_profiles.data
        no_posts = coment_form.no_posts.data           
        id_srch = do_search(in_name,no_profiles,no_posts)
        
        if id_srch == NO_PROFILES_FOUND:
            error = ("No se encontraron perfiles de Instagram con el username o nombre: "+in_name)
            return render_template('busqueda.html',error=error,form = coment_form)
        if not id_srch:
            error = 'ERROR: El servicio de búsqueda falló, por favor intente de nuevo.'
            return render_template('busqueda.html',error=error,form = coment_form)
        else:                        
            next = request.args.get('next', 'resultado_busqueda') # especificamos la ruta si se enviaron los datos            
            if next:    # comprobamos si paso por la url
               return redirect(url_for('resultado_busqueda', id_srch=id_srch)) # Se manda a la ruta
            return redirect(url_for('index')) #si no mandamos a la ruta o parametro definido
    return render_template('busqueda.html', form = coment_form) # mandamos el formulario

@app.route('/resultado_busqueda/<int:id_srch>', methods=['GET','POST'])
def resultado_busqueda(id_srch):
    if request.method == 'GET':
        data_srch=select_srch(id_srch)
        data = result_data_for_view(id_srch)
        if data:                        
            return render_template('resultadobusqueda.html', Busqueda = data_srch, Perfiles = data, noResults = len(data))
        else:
            error = 'ERROR al mostrar los resultados, por favor intente de nuevo.'
            return render_template('busqueda.html',error=error)
    else:
        chekList = request.form.getlist('analisis')
        #if getImages(chekList,id_srch):
        getImages(chekList,id_srch)
        creaCarpeta(id_srch)
        analisisArma(id_srch)
        mypath = output_path + str(id_srch) #carpeta de imagenes analizadas
        pics = [f for f in listdir(mypath) if isfile(join(mypath, f))] #lista de esas imagenes

        for imagen in pics:
            fromDirectory = mypath
            toDirectory = "./static/detecciones/" + str(id_srch)
            copy_tree(fromDirectory, toDirectory)
        return render_template("resultado_analisis.html", pics=pics, id=id_srch)
        #else:
            #error = 'ERROR al comenzar el análisis, por favor intente de nuevo.'
            #return render_template('show.html', message=error)

@app.route('/consulta', methods = ['GET', 'POST'])
def consulta():
    coment_form = formulario.ComentFormCon(request.form)
    if request.method == 'POST' and coment_form.validate():    #   se agrega coment_form para validar el formulario 
        #id_busqueda = coment_form.id_busqueda.data
        in_name = coment_form.in_name.data # se guarda con form en la variable declarada segun busqueda.html
        fecha_in = coment_form.fecha_in.data
        fecha_fin = coment_form.fecha_fin.data       
        ## Creamos una lista con los valores de la consulta
        consulta=[in_name, fecha_in, fecha_fin]
        
        next = request.args.get('next', 'resultado_consulta') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(url_for('resultado_consulta', consulta=consulta)) # Se manda a la ruta
        return redirect(url_for('index'))
    return render_template('consulta.html', form=coment_form) 

@app.route('/resultado_consulta/<consulta>', methods=['GET','POST'])
def resultado_consulta(consulta):
    print(consulta)
    print(":::::::::::::::::::::::hoolalksdf")
    if request.method == 'GET':
        print(consulta)
        data_con=consulta_busqueda()    
    return render_template('resultadoconsulta.html', Consulta = data_con, consulta=consulta )

@app.route('/reportes')
def reportes():
    lis_reportes = os.listdir('static/pdf')
    return render_template('reportes.html', Reportes=lis_reportes)

@app.route('/conocenos')
def conocenos():
    return render_template('conocenos.html')


# la api que regresa las detecciones
@app.route('/detections/<int:id_srch>', methods=['GET','POST'])
def detections(id_srch):
    raw_images = []
    images = request.files.getlist("images")
    image_names = []
    for image in images:
        image_name = image.filename
        image_names.append(image_name)
        image.save(os.path.join(os.getcwd(), image_name))
        img_raw = tf.image.decode_image(
            open(image_name, 'rb').read(), channels=3)
        raw_images.append(img_raw)
        
    num = 0
    
    # se crea lista en caso de ser mas de una
    response = []

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
        nombre = randomString()
        final_path = output_path + str(id_srch) + "/" + image_names[0] + "-" + nombre + '.jpg'
        cv2.imwrite(final_path, img)

    #remove temporary images
    for name in image_names:
        os.remove(name)
    try:
        return jsonify(responses), 200
    except FileNotFoundError:
        abort(404)

@app.route('/generar_reportes')
def generar_reportes():
    x = datetime.now()
    date =str(x.year)+str(x.month)+str(x.day)+str(x.minute)
    
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None
    }
    css = 'static/css/reporte.css'
    
    #config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    generarpdf()
    pdfkit.from_file('templates/reporte2.html', 'static/pdf/reporte'+date+'.pdf', options=options, css=css)
    #pdfkit.from_string(generarpdf(), 'static/pdf/reporte'+date+'.pdf')
    pdf =  pdfkit.from_file('templates/reporte2.html', False)   #configuration=config
    os.remove('templates/reporte2.html')
   
    response = make_response(pdf)
    response.headers['Content-type'] = 'static/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename = reporte'+date+'.pdf'
    return response 

@app.route('/reporte')
def reporte():
    return render_template('reporte.html')



# valifamos que se ejecute el programa principal
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000) # Actualizar servdor automaticamente y se indica el puerto 
