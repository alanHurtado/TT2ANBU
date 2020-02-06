from flask import Flask
from flask import render_template ## permite renderisar templates

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html') # se agrega rende_template para usar el template

@app.route('/busqueda')
def busqueda():
    return render_template('busqueda.html') # se agrega rende_template para usar el template

@app.route('/resultadobusqueda')
def resultado_busqueda():
    return render_template('resultadobusqueda.html') # se agrega rende_template para usar el template

@app.route('/consulta')
def consulta():
    return render_template('consulta.html') # se agrega rende_template para usar el template

@app.route('/resultadoconsulta')
def resultado_consulta():
    return render_template('resultadoconsulta.html') # se agrega rende_template para usar el template

if __name__ == '__main__':
    app.run(debug = True, port = 8000) #se indica el puerto 

