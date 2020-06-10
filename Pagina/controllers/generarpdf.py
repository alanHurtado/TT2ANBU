from jinja2 import Environment, FileSystemLoader

def generarpdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reporte.html')
    x = 19
    a_perfiles = 5+1 #total perfiles analisados
    a_publicaciones = 3+1 #total de publicaciones por perfil
    datos = {
        'num_busqueda': 10,
        'fecha_busqueda' : '10/08/2020',
        'username': 'Ferrer',
        'no_perfiles' : 8,
        'no_publicaciones' : 6,
        'no_rostros': 10,
        'no_armas': x,
        'perfiles': a_perfiles,
        'perfil': 1,
        'name_perfil':'Roberto Sanchez',
        'usernamw': '@Roberto24',
        'biodrafia': 'Soy provedor de servicios externos en consul..... ',
        'publicacion': 1,
        'publicaciones': a_publicaciones,
        'ruta_imagen':'../static/img/ANBU.jpg',
        'ubi_publi': 'Mexico',
        'fecha_publi': '98/87/12',
        'enlace': 'ruta de enla perfil',
        'pie_img': 'En la playa',
        'no_arma_pub': 2,
        'no_rostro_pub':1,
        'resultado': 'Es posible violento'
    }

    html = template.render(datos)
    #print(html)
    return html