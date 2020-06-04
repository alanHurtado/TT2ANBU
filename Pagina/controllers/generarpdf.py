from jinja2 import Environment, FileSystemLoader

def generarpdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reporte.html')
    datos = {
        'name': 'Alan',
        'course': 10,
        'img_per' : 'static/img/ANBU.jpg'
    }

    html = template.render(datos)
    return html