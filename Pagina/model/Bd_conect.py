###---------------- MODELO PARA OPERACIONES EN LA BASE DE DATOS ----------------###

#:::: Este componente se encarga de realizar las operaciones sobre
# la base de datos. Establece la conexión con la base y define las
# funciones para operaciones INSERT, SELECT y UPDATE.

from flaskext.mysql import MySQL
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey" 

#::::::::::: Conexión a la base de datos :::::::::::#
app.config['MYSQL_DATABASE_USER'] = 'ANBU'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ANBUTT2'
app.config['MYSQL_DATABASE_DB'] = 'anbuDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)
conn = mysql.connect()
#:::::::::::::::::::::::::::::::::::::::::::::::::::#

#:::::::::::::::::::::::: Funciones INSERT INTO ::::::::::::::::::::::::#
def insertar_busqueda(in_name):
    cursor = conn.cursor()
    x = datetime.now()
    formatted_date = x.strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = (
            "INSERT INTO Busqueda (nombre_buscado,fecha)"
            " VALUES (%s,%s)"
        )
        data = (in_name,formatted_date)
        cursor.execute(query,data)
        conn.commit()        
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insertar_busqueda: "+str(e))
        return False    

def insert_profile(username, name, url):
    cursor = conn.cursor()
    try:
        query = (
            "INSERT INTO Perfil (username,nombre,urlPerfil)" 
            " VALUES (%s,%s,%s)"
        )
        data = (username,name,url)
        cursor.execute(query,data)
        conn.commit()        
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insert_profile: "+str(e))
        return False        

def insert_srch_prof(idSearch,idProfile):
    cursor = conn.cursor()
    try:
        query = (
            "INSERT INTO busqueda_perfil (idBusqueda,idPerfil)"
            " VALUES (%s,%s)"
        )
        data = (idSearch,idProfile)
        cursor.execute(query,data)
        conn.commit()        
        return True
    except Exception as e:
        print("ERROR al realizar insert_srch_prof: "+str(e))
        return False

def insert_post(idProfile,date,urlPost,desc,location,urlImage):
    cursor = conn.cursor()
    try:
        query = (
            "INSERT INTO Publicacion"
            "(idPerfil,fecha,urlPublicacion,descripcion,ubicacion,urlImagen) "
            "VALUES (%s,%s,%s,%s,%s,%s)"
        )
        date = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        data = (idProfile,date,urlPost,desc,location,urlImage)      
        cursor.execute(query,data)
        conn.commit()        
        return cursor.lastrowid
    except Exception as e:
        print("ERROR al realizar insert_post: "+str(e))
        print(desc)       
        return False    

def insert_arma(idPublicacion,porcentaje,evaluacion):
    cursor = conn.cursor()
    try:
        query = (
            "INSERT INTO Arma (idPublicacion,porcentaje,evaluacion_arma)"
            " VALUES (%s,%s,%s)"
        )
        data = (idPublicacion,porcentaje,evaluacion)
        cursor.execute(query,data)
        conn.commit()        
        return True
    except Exception as e:
        print("ERROR al realizar insert_arma: "+str(e))
        return False

def insert_rostro(cejas_arco,labios_grandes,nariz_grande,cejas_pobladas,
        barbilla_partida,pomulos,rostro_oval,nariz_puntiaguda,entradas,idPublicacion,
        evaluacion_rostro):
    cursor = conn.cursor()
    try:
        query = (
            "INSERT INTO Rostro (cejas_arco,labios_grandes,nariz_grande,cejas_pobladas,barbilla_partida,pomulos,rostro_oval,nariz_puntiaguda,entradas,idPublicacion,evaluacion_rostro)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        data = (cejas_arco,labios_grandes,nariz_grande,cejas_pobladas,
        barbilla_partida,pomulos,rostro_oval,nariz_puntiaguda,entradas,idPublicacion,
        evaluacion_rostro)
        cursor.execute(query,data)
        conn.commit()        
        return True
    except Exception as e:
        print("ERROR al realizar insert_rostro: "+str(e))
        return False
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

#:::::::::::::::::::::: Funciones SELECT ::::::::::::::::::::::#
def consulta_busqueda():
    cursor = conn.cursor()
    try:  
        cursor.execute("SELECT * FROM Busqueda")
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("Error al realizar la consulta"+str(e))
        return False

def select_srch(idBusqueda):
    cursor = conn.cursor()    
    try:
        query = (
            "SELECT * FROM Busqueda "
            "WHERE idBusqueda = "+str(idBusqueda)
        )       
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()       
        return data
    except Exception as e:
        print("ERROR al realizar select_srch(): "+str(e))
        return False

def select_last_id():
    cursor = conn.cursor()
    try:  
        cursor.execute("SELECT idBusqueda from Busqueda ORDER BY fecha DESC LIMIT 1")
        data = cursor.fetchone()
        cursor.close()
        return str(data[0])
    except Exception as e:
        print("Error al realizar la consulta"+str(e))
        return False        

def select_profiles_by_srch(idBusqueda):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT p.* "
            "FROM Busqueda b, Perfil p, busqueda_perfil x "
            "WHERE b.idBusqueda = "+str(idBusqueda)+" "
            "AND x.idBusqueda = b.idBusqueda "
            "AND x.idPerfil = p.idPerfil;"
        )
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
        query=(
            "SELECT x.* "
            "FROM Publicacion x, Perfil y "
            "WHERE y.idPerfil = "+str(idPerfil)+" "
            "AND x.idPerfil=y.idPerfil;"
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_posts(): "+str(e))
        return False

def result_data_for_view(id_srch):
    try:
        data_prof=select_profiles_by_srch(id_srch)
        data = list()
        for prof in data_prof:
            profiles = list()
            data_post=select_posts(prof[0])
            posts = list(data_post)
            profiles.append(prof)
            profiles.append(posts)
            data.append(profiles)
        return data
    except Exception as e:
        print("ERROR recuperando los datos de la búsqueda result_data_for_view(): "+str(e))
    return False

def get_url_post(ids_profiles):
    cursor = conn.cursor()
    try:
        data = list()
        for idProf in ids_profiles:
            aux = list()
            aux.append(idProf)
            query = (
                "SELECT idPublicacion, urlImagen "
                "FROM Publicacion "
                "WHERE idPerfil = "+str(idProf)
            )
            cursor.execute(query)
            url_list = list(cursor.fetchall())
            aux.append(url_list)
            data.append(aux)
        cursor.close()
        return data
    except Exception as e:
        print("ERROR recuperando los datos de la búsqueda get_url_post(): "+str(e))
    return False

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

# :::::::::::::::::::::Para proceso de consultas

def select_consulta(fechain, fechafin):
    cursor = conn.cursor()    
    try:
        query = (
            "SELECT * "
            "FROM Busqueda "
            "WHERE fecha BETWEEN "+ str(fechain)+ "AND" + str(fechafin)
        )     
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()       
        return data
    except Exception as e:
        print("ERROR al realizar select_consulta(): "+str(e))
        return False

def select_fechabus(id_bus):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT nombre_buscado, fecha "
            "From Busqueda "
            "WHERE idBusqueda =" + id_bus
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_fechabus(): "+str(e))
        return False
    
def num_perfiles(id_bus):
    cursor = conn.cursor()
    try:
        query = (
            
            "SELECT COUNT(*) FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar num_perfiles(): "+str(e))
        return False

    
def num_publicaciones(id_bus):
    cursor = conn.cursor()
    try: 
        query = (

            "SELECT COUNT(*) FROM Publicacion WHERE idPerfil IN ("
            "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar num_publicaciones(): "+str(e))
        return False

def num_armas(id_bus):
    cursor = conn.cursor()
    try: 
        query = (
            
            "SELECT COUNT(*) FROM Arma WHERE idPublicacion IN ( "
             "SELECT idPublicacion FROM Publicacion WHERE val_arma = 1 AND idPerfil IN ("
                "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                    "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                        "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar num_armas(): "+str(e))
        return False

def num_rostros(id_bus):
    cursor = conn.cursor()
    try: 
        query = (
            
            "SELECT COUNT(*) FROM Rostro WHERE idPublicacion IN ( "
             "SELECT idPublicacion FROM Publicacion WHERE val_rostro=1 AND idPerfil IN ("
                "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                    "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                        "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_num_rostros(): "+str(e))
        return False

def select_perfil (id_bus):
    cursor = conn.cursor()
    try:
        query = (
            
            "SELECT * FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_perfil(): "+str(e))
        return False

    
def select_publicaciones(id_bus):
    cursor = conn.cursor()
    try: 
        query = (

            "SELECT * FROM Publicacion WHERE idPerfil IN ("
            "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_publicaciones(): "+str(e))
        return False

def select_armas(id_bus):
    cursor = conn.cursor()
    try: 
        query = (

            "SELECT idPublicacion, porcentaje FROM Arma WHERE idPublicacion IN ("
            "SELECT idPublicacion FROM Publicacion WHERE idPerfil IN ("
            "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_armas(): "+str(e))
        return False

def select_rostros(id_bus):
    cursor = conn.cursor()
    try: 
        query = (
            
            "SELECT idPublicacion, rostro_oval, entradas, cejas_pobladas, cejas_arco, pomulos, nariz_grande, nariz_puntiaguda, labios_grandes, barbilla_partida, evaluacion_rostro FROM Rostro WHERE idPublicacion IN ("
            "SELECT idPublicacion FROM Publicacion WHERE idPerfil IN ("
            "SELECT idPerfil FROM Perfil WHERE idPerfil IN ( "
                "SELECT  idPerfil FROM busqueda_perfil WHERE idBusqueda IN ("
                    "SELECT idBusqueda FROM Busqueda WHERE idBusqueda = "+ id_bus + ") ) ) )" 
        )
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print("ERROR al realizar select_rostros(): "+str(e))
        return False

#:::::::::::::::::::: Funciones UPDATE ::::::::::::::::::::#
def upd_img_path(idPost,path):
    cursor = conn.cursor()
    try:
        query = (
            "UPDATE Publicacion "
            "SET ruta_imagen = %s "
            "WHERE idPublicacion = %s"
        )
        data = (path,idPost)
        cursor.execute(query,data)
        conn.commit();
        cursor.close()
        return True
    except Exception as e:
        print("ERROR al realizar upd_img_path(): "+str(e))
        return False 

def upd_val_arma(idPublicacion,val):
    cursor = conn.cursor()
    try:
        query = (
            "UPDATE Publicacion "
            "SET val_arma = %s "
            "WHERE idPublicacion = %s"
        )
        data = (val,idPublicacion)
        cursor.execute(query,data)
        conn.commit();
        cursor.close()
        return True
    except Exception as e:
        print("ERROR al realizar upd_val_arma(): "+str(e))
        return False  

def upd_val_rostro(idPublicacion,val):
    cursor = conn.cursor()
    try:
        query = (
            "UPDATE Publicacion "
            "SET val_rostro = %s "
            "WHERE idPublicacion = %s"
        )
        data = (val,idPublicacion)
        cursor.execute(query,data)
        conn.commit();
        cursor.close()
        return True
    except Exception as e:
        print("ERROR al realizar upd_val_rostro(): "+str(e))
        return False  
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#