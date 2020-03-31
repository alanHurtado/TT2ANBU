from flaskext.mysql import MySQL  ## permite el uso de MySQL
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey" 

### Conexión a la base de datos ####
app.config['MYSQL_DATABASE_USER'] = 'ANBU'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ANBUTT2'
app.config['MYSQL_DATABASE_DB'] = 'anbuDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

conn = mysql.connect()  #conectamos a la BD

#----Funciones INSERT INTO --------#
def insertar_busqueda(in_name):
    cursor = conn.cursor()
    x = datetime.now()
    formatted_date = x.strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("INSERT INTO Busqueda (nombre_buscado,fecha) VALUES (%s,%s)", (in_name, formatted_date))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insertar_busqueda: "+str(e))
        return False    

def insert_profile(username, name, url):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Perfil (username,nombre,urlPerfil) VALUES (%s,%s,%s)",(username,name,url))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insert_profile: "+str(e))
        return False        

def insert_srch_prof(idSearch,idProfile):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO busqueda_perfil (idBusqueda,idPerfil) VALUES (%s,%s)",(idSearch,idProfile))
        conn.commit()
        return True
    except Exception as e:
        print("ERROR al realizar insert_srch_prof: "+str(e))
        return False

def insert_post(idProfile,date,url,desc,location):
    cursor = conn.cursor()
    try:
        date = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')          
        cursor.execute("INSERT INTO Publicacion (idPerfil,fecha,url,descripcion,ubicacion) VALUES (%s,%s,%s,%s,%s)",(idProfile,date,url,desc,location))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insert_post: "+str(e))
        return False
    pass
#------------------------------------------------------------------#

#------Funciones SELECT ------------#
def select_srch(idBusqueda):
    cursor = conn.cursor()    
    try:
        cursor.execute('SELECT * from Busqueda where idBusqueda ='+str(idBusqueda))
        data = cursor.fetchall()
        cursor.close()       
        return data
    except Exception as e:
        print("ERROR al realizar select_srch(): "+str(e))
        return False        

def select_profiles(idBusqueda):
    cursor = conn.cursor()
    try:
        query = """select p.*
        from Busqueda b, Perfil p, busqueda_perfil x
        where b.idBusqueda = """+str(idBusqueda)+"""
        and x.idBusqueda = b.idBusqueda
        and x.idPerfil = p.idPerfil;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_profiles(): "+str(e))
        return False

def select_posts(idPerfil):
    cursor = conn.cursor()
    try:
        query="""select x.*
        from Publicacion x, Perfil y
        where y.idPerfil = """+str(idPerfil)+"""
        and x.idPerfil=y.idPerfil;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_posts(): "+str(e))
        return False


#------------------------------------------------------------------#