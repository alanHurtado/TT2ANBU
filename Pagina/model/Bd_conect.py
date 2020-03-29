from flaskext.mysql import MySQL  ## permite el uso de MySQL
from flask import Flask

app = Flask(__name__)
app.secret_key = "mysecretkey" 

### Conexión a la base de datos ####
app.config['MYSQL_DATABASE_USER'] = 'ANBU'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ANBUTT2'
app.config['MYSQL_DATABASE_DB'] = 'ANBU_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

conn = mysql.connect()  #conectamos a la BD
cursor = conn.cursor()  #creamos cursos para manejar la BD

def insertar_busqueda(in_name):    
    cursor.execute("INSERT INTO Busqueda (nombre_buscado) VALUES (%s)", (in_name))
    cursor.lastrowid    
    print(conn.commit())

def res_bus():    
    cursor.execute('SELECT * FROM Busqueda')
    data = cursor.fetchall()
    cursor.close()
    return data

def res_per(): 
    cursor.execute('SELECT * FROM Perfil')
    data = cursor.fetchall()
    cursor.close()
    return data