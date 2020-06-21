from jinja2 import Environment, FileSystemLoader
from model.Bd_conect import * 
from matplotlib import pyplot

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

    ###PAra generar Grafico de arma
    
    por_arma = select_armas(id_bus) #valor de porcentaje arma
    for porArma in por_arma:
        if porArma[1] is None:
            porArma[1]=0
        arma = 100-porArma[1]
        variantes = ('Error','Factibilidad')
        valor=(arma, porArma[1])
        color=('#563832','#5A2783')
        valores = (0.1, 0)
        pyplot.rcParams['toolbar'] ='None'
        _, _, texto = pyplot.pie(valor, colors=color, labels=variantes, autopct='%1.2f%%',
                                explode=valores, startangle=90 )
    
        for text in texto:
            text.set_color('white')

        ruta='static/img/graficoA'+str(porArma[0])+'.png'
        pyplot.axis('equal')
        pyplot.savefig(ruta)
        pyplot.close()
       


### Rutas de los graficos generados 
   
    
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
        'val_rostro': valRostro,
    }

    html = template.render(datos)
    f = open('templates/reporte2.html', 'w')
    f.write(html)
    f.close() 
    #print(html)
    