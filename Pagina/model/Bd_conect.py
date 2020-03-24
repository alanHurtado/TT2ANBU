from flaskext.mysql import MySQL  ## permite el uso de MySQL
from flask import Flask

app = Flask(__name__)

### Coneccion a la base de datos ####
app.config['MYSQL_DATABASE_USER'] = 'ANBU'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ANBUTT2'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

app.secret_key = "mysecretkey" 

def insertar_busqueda(nombre, usuario, ubicacion ):
    conn = mysql.connect()  # conectamos a la BD
    cursor = conn.cursor()     # creamos cursos para manejar la BD
    cursor.execute("INSERT INTO Busqueda (username_buscado, nombre_buscado, ubicacion) VALUES (%s,%s,%s)", (usuario, nombre, ubicacion))
    conn.commit()

def res_bus():
    conn = mysql.connect()  # conectamos a la BD
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Busqueda')
    data = cursor.fetchall()
    cursor.close()
    return data

def res_per():
    conn = mysql.connect()  # conectamos a la BD
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Perfil')
    data = cursor.fetchall()
    cursor.close()
    return data