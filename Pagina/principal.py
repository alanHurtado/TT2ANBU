from ctlBusqueda import *
from flask import Flask
from flask import render_template ## permite renderisar templates
from flask import request, redirect, url_for, flash   ## permite el manejo de los datos del formulario
from model.Bd_conect import insertar_busqueda, res_bus, res_per  # importamos los registros a la BD
from model import formulario    #importamos el formulario

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
        
        #------TEST-------#
        if not do_search(in_name,no_profiles):
            error = 'El servicio de búsqueda no está disponible, intente de nuevo.'
            return render_template('busqueda.html',error=error,form = coment_form)
        else:            
            return render_template('resultadobusqueda.html', json = [{"foo","var"}])
        #---------------------------#
        
        # next = request.args.get('next', 'resultado_busqueda') ## especificamos la ruta si se enviaron los datos
        # if next:    # comprobamos si paso por la url
        #    return redirect(next) # Se manda a la ruta
        # return redirect(url_for('index')) #si no mandamos a la ruta o parametro definido
    return render_template('busqueda.html', form = coment_form) # mandamos el formulario

@app.route('/resultado_busqueda')
def resultado_busqueda():
    data_bus=res_bus()
    data_per=res_per()
    return render_template('resultadobusqueda.html', Busqueda = data_bus, Perfil = data_per)

@app.route('/consulta', methods = ['GET', 'POST'])
def consulta():
    coment_form = formulario.ComentFormCon(request.form)
    if request.method == 'POST' and coment_form.validate():    #   se agrega coment_form para validar el formulario 
        id_busqueda = coment_form.id_busqueda.data
        nombre = coment_form.nombre.data # se guarda con form en la variable declarada segun busqueda.html
        nombre_usuario = coment_form.nombre_usuario.data
        ubicacion = coment_form.ubicacion.data
        fecha_in = coment_form.fecha_in.data
        fecha_fin = coment_form.fecha_fin.data
    
        next = request.args.get('next', 'resultado_consulta') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(next) # Se manda a la ruta
        return redirect(url_for('index'))
    return render_template('consulta.html', form=coment_form) 

@app.route('/resultado_consulta')
def resultado_consulta():
    
    return render_template('resultadoconsulta.html') 

# valifamos que se ejecute el programa principal
if __name__ == '__main__':
    app.run(debug = True, port = 8000) # Actualizar servdor automaticamente y se indica el puerto 

