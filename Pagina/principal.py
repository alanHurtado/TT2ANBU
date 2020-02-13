from flask import Flask
from flask import render_template ## permite renderisar templates
from flask import request, redirect, url_for   ## permite el manejo de los datos del formulario
from flaskext.mysql import MySQL  ## permite el uso de MySQL
from werkzeug import generate_password_hash, check_password_hash

import formulario   # importamos el formulario

app = Flask(__name__)

### Coneccion a la base de datos ####
app.config['MYSQL_DATABASE_USER'] = 'ANBU'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ANBUTT2'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

app.secret_key = "mysecretkey" 

@app.route('/')
def index():
    return render_template('home.html') # se agrega rende_template para usar el template

@app.route('/busqueda', methods=['GET', 'POST']) # indicamos solocitudes get y post en la pagina   
def busqueda(): # accedemos al atributo method POST = enviar GET = mostrar
    coment_form = formulario.ComentForm(request.form)    # generamos la instacia al formulario
    if request.method == 'POST':    #   si se reciben datos
        nombre = coment_form.nombre.data # se guarda con form en la variable declarada segun busqueda.html
        nombre_usuario = coment_form.nombre_usuario.data
        ubicacion = coment_form.ubicacion.data
        conn = mysql.connect()  # conectamos a la BD
        cursor = conn.cursor()     # creamos cursos para manejar la BD
        cursor.execute("INSERT INTO Busqueda (username_buscado, nombre_buscado, ubicacion) VALUES (%s,%s,%s)", (nombre_usuario, nombre, ubicacion))
        conn.commit()

        next = request.args.get('next', 'consulta') ## especificamos la ruta si se enviaron los datos
        if next:    # comprobamos si paso por la url
           return redirect(next) # Se manda a la ruta
        return redirect(url_for('index')) #si no mandamos a la ruta o parametro definido
    return render_template('busqueda.html', form = coment_form) # mandamos el formulario

@app.route('/resultadobusqueda')
def resultado_busqueda():
    return render_template('resultadobusqueda.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html') 

@app.route('/resultadoconsulta')
def resultado_consulta():
    return render_template('resultadoconsulta.html') 

# valifamos que se ejecute el programa principal
if __name__ == '__main__':
    app.run(debug = True, port = 8000) # Actualizar servdor automaticamente y se indica el puerto 

