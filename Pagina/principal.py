###---------------- CONTROLADOR PRINCIPAL DEL SISTEMA ----------------###

#:::: Este controlador procesa todas las peticiones que
# recibe la página del sistema, se encarga de redirigir al
# usuario a las secciones correspondientes y también de ejecutar
# el código para la lógica del negocio.
from datetime import *
from controllers.ctlBusqueda import *
from controllers.ctlAnalisis import *
from controllers.generarpdf import *
from controllers import formulario
import pdfkit
from flask import Flask
from flask import render_template  # Permite renderizar templates (Archivos HTML)
from flask import Flask, Response, jsonify, send_from_directory, abort, request, redirect, url_for, flash  # Permite manejo de los datos del formulario
from flask import render_template, make_response  # Permite renderizar templates (Archivos HTML)
from flask import request, redirect, url_for, flash  # Permite manejo de los datos del formulario
from model.Bd_conect import *  # Funciones del modelo para uso de la base de datos

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
        try:
            data_url=get_url_post(chekList)
            getImages(chekList,id_srch)
            creaCarpeta(id_srch)
            analisisArma(id_srch)
            mypath = DETECTIONS_PATH + str(id_srch) #carpeta de imagenes analizadas
            pics = [f for f in listdir(mypath) if isfile(join(mypath, f))] #lista de esas imagenes

            for imagen in pics:
                fromDirectory = mypath
                toDirectory = "./static/detecciones/" + str(id_srch)
                copy_tree(fromDirectory, toDirectory)

            return render_template("resultado_analisis.html", pics=pics, id=id_srch, url_img_posts = data_url)
        except Exception as e:
            print("--ERROR-- en getImages, creaCarpeta, analisisArma. Exception: "+str(e))
            error = 'ERROR al comenzar el análisis, por favor intente de nuevo.'
            return render_template('/resultado_busqueda/', message=error, id_srch = id_srch)

@app.route('/consulta', methods = ['GET', 'POST'])
def consulta():
    coment_form = formulario.ComentFormCon(request.form)
    if request.method == 'POST' and coment_form.validate():    #   se agrega coment_form para validar el formulario 
        in_name = coment_form.in_name.data # se guarda con form en la variable declarada segun busqueda.html
        fecha_in = coment_form.fecha_in.data
        fecha_fin = coment_form.fecha_fin.data       
        datos=[in_name, fecha_in, fecha_fin]
        ## Creamos una lista con los valores de la consulta
        next = request.args.get('next', 'resultado_consulta') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(url_for('resultado_consulta', datos=datos)) # Se manda a la ruta
        return redirect(url_for('index'))
    return render_template('consulta.html', form=coment_form) 

@app.route('/resultado_consulta/<string:datos>', methods=['GET','POST'])
def resultado_consulta(datos):
    coment_form = formulario.ComentFormReport(request.form)
    if request.method == 'POST' and coment_form.validate():    #   se agrega coment_form para validar el formulario 
        id_con = coment_form.id_con.data# se guarda con form en la variable declarada segun busqueda.html
        ## Creamos una lista con los valores de la consulta
        next = request.args.get('next', 'generar_reportes') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(url_for('generar_reportes', id_con=id_con)) # Se manda a la ruta
        return redirect(url_for('index'))
    else :
        datos=datos[1:len(datos)-1]
        datos2=datos.split()
        name=datos2[0]
        fecha1=datos2[1]
        fecha2=datos2[2]
        name=name[1:len(name)-2]

        fecha1=fecha1[0:len(fecha1)-1]
    
        consultas=select_consulta(fecha1,fecha2)
    
        fecha1=fecha1[1:len(fecha1)-1]
        fecha2=fecha2[1:len(fecha2)-1]
 
    return render_template('resultadoconsulta.html', name=name, form=coment_form, fecha1=fecha1, fecha2=fecha2, consultas=consultas)

@app.route('/reportes')
def reportes():
    lis_reportes = os.listdir('static/pdf')
    return render_template('reportes.html', Reportes=lis_reportes)

@app.route('/conocenos')
def conocenos():
    return render_template('conocenos.html')

@app.route('/generar_reportes/<string:id_con>', methods=['GET','POST'])
def generar_reportes(id_con):
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
    generarpdf(id_con)
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

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)