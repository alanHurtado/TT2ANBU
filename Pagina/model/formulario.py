from wtforms import Form    # para importar formularios
from wtforms import StringField, SubmitField, IntegerField, DateField # Para usar campos de texto

class ComentForm(Form):
    id_busqueda = IntegerField('ID Busqueda')
    nombre = StringField('Nombre: ') # variable nombre con vista Nombre en html
    nombre_usuario = StringField('Nombre de usuario: ')
    ubicacion = StringField('Ubicación: ')
    fecha = DateField('Fecha: ')
    submit = SubmitField('')
