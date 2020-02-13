from wtforms import Form    # para importar formularios
from wtforms import StringField, SubmitField # Para usar campos de texto

class ComentForm(Form):
    nombre = StringField('Nombre: ') # variable nombre con vista Nombre en html
    nombre_usuario = StringField('Nombre de usuario: ')
    ubicacion = StringField('Ubicación: ')
    submit = SubmitField('Enviar')
