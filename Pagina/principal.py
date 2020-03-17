from flask import Flask
from flask import render_template ## permite renderisar templates
from flask import request, redirect, url_for   ## permite el manejo de los datos del formulario
from model.Bd_conect import insertar_busqueda, res_bus   # importamos los registros a la BD
from model import formulario    #importamos el formulario

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html') # se agrega rende_template para usar el template

@app.route('/busqueda', methods = ['GET', 'POST']) # indicamos solocitudes get y post en la pagina   
def busqueda(): # accedemos al atributo method POST = enviar GET = mostrar
    coment_form = formulario.ComentForm(request.form)    # generamos la instacia al formulario
    if request.method == 'POST':    #   si se reciben datos
        nombre = coment_form.nombre.data # se guarda con form en la variable declarada segun busqueda.html
        nombre_usuario = coment_form.nombre_usuario.data
        ubicacion = coment_form.ubicacion.data
        insertar_busqueda(nombre, nombre_usuario, ubicacion)    #mandamos los datos para ser insetardos en la BD
        next = request.args.get('next', 'resultado_busqueda') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(next) # Se manda a la ruta
        return redirect(url_for('index')) #si no mandamos a la ruta o parametro definido
    return render_template('busqueda.html', form = coment_form) # mandamos el formulario

@app.route('/resultado_busqueda')
def resultado_busqueda():
    data=res_bus()
    return render_template('resultadobusqueda.html', Busqueda = data)

@app.route('/consulta', methods = ['GET', 'POST'])
def consulta():
    coment_form = formulario.ComentForm(request.form)
    if request.method == 'POST':    #   si se reciben datos
        id_busqueda = coment_form.id_busqueda.data
        nombre = coment_form.nombre.data # se guarda con form en la variable declarada segun busqueda.html
        nombre_usuario = coment_form.nombre_usuario.data
        ubicacion = coment_form.ubicacion.data
        fecha = coment_form.fecha.data
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

