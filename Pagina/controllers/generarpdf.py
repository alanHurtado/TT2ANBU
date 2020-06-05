from jinja2 import Environment, FileSystemLoader

def generarpdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reporte.html')
    datos = {
        'num_busqueda': 10,
        'fecha_busqueda' : '10/08/2020',
        'username': 'Ferrer',
        'no_perfiles' : 8,
        'no_publicaciones' : 6


    }

    html = template.render(datos)
    #print(html)
    return html