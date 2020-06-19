from jinja2 import Environment, FileSystemLoader
from model.Bd_conect import * 

def generarpdf(id_bus):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reporte.html')
   #### Obtener datos de la BD
    dato = select_fechabus(id_bus)
    fechaBus = dato
    nomBus = dato
    dato = num_perfiles(id_bus)
    numPerfiles = dato
    dato = num_publicaciones(id_bus)
    numPublicaciones = dato
    dato = num_armas(id_bus)
    numArmas = dato
    dato = num_rostros(id_bus)
    numRostros = dato
    dato = select_perfil(id_bus)
    perfiles = select_perfil(id_bus)
    publicaciones = select_publicaciones(id_bus)
    
    valRostro = 2

    datos = {
        'num_busqueda': id_bus,
        'fecha_busqueda' : fechaBus,
        'nombre_buscado': nomBus,
        'no_perfiles' : numPerfiles,
        'no_publicaciones' : numPublicaciones,
        'no_rostros': numRostros,
        'no_armas': numArmas,
        'perfiles': perfiles,
        'publicaciones': publicaciones,
        'resultado': 'Es posible violento',
        'val_rostro': valRostro

    }

    html = template.render(datos)
    f = open('templates/reporte2.html', 'w')
    f.write(html)
    f.close() 
    #print(html)
    