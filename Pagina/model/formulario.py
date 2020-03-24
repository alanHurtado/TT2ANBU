import sys, re, time
from wtforms import Form    # para importar formularios
from wtforms import StringField, SubmitField # Para usar campos de texto
from wtforms import validators  #realizar validaciones

## Validaciones para Formulario de busqueda ###
def val_nombre(form, field):
    nombre = field.data
    validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+[0-9a-z]*$', nombre, re.I)
    if nombre == "" :
        raise validators.ValidationError('Es necesario ingresar un nombre')
    elif not validar :
        raise validators.ValidationError('Nombre incorrecto')
  
def val_username(form, field):
    nombre = field.data
    validar = re.match('^@?[a-z0-9\._-sáéíóúàèìòùäëïöüñ]*$', nombre, re.I)
    if not validar :
        raise validators.ValidationError('Username  incorrecto')

##########################################################################3

##### Validaciones formulario Consulta ################
def val_id (form, field):
    nombre = field.data
    validar = re.match('^[0-9]*$', nombre, re.I)
    if nombre == "":
        nombre == "x"
    else :
        if nombre[0] == "0" :
            raise validators.ValidationError('ID no valido')
        elif not validar :
            raise validators.ValidationError('ID no valido')

def val_nombrec(form, field):
    nombre = field.data
    validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]*[0-9a-z]*$', nombre, re.I)
    if not validar :
        raise validators.ValidationError('Nombre incorrecto')



class ComentFormBus(Form):
    nombre = StringField('Nombre: ',
    [
        val_nombre
    ]) 
    nombre_usuario = StringField('Nombre de usuario: ', 
    [   
        val_username
    ])
    ubicacion = StringField('Ubicación: ')
    submit = SubmitField('')

class ComentFormCon(Form):
    id_busqueda = StringField('Id Búsqueda: ', 
    [
        val_id
    ])
    nombre = StringField('Nombre: ',
    [
        val_nombrec
    ]) 
    nombre_usuario = StringField('Nombre de usuario: ', 
    [   
        val_username
    ])
    ubicacion = StringField('Ubicación: ')
    fecha_in = StringField('Fecha del : ', 
    [
        validators.InputRequired(message ='Fecha requerida')
    ])
    fecha_fin =StringField('al - ', 
    [
        validators.input_required(message='Fecha requerida')
    ])
    submit = SubmitField('')

