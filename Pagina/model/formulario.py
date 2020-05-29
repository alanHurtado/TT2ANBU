import sys, re, time
from wtforms import Form    # para importar formularios
from wtforms import StringField, SubmitField , SelectField# Para usar campos de texto
from wtforms import validators  #realizar validaciones

########### ---------------Validaciones para Formulario de busqueda -----------------##########
def val_nombre(form, field):
    nombre = field.data
    validar = re.match('^@?[a-z\s_áéíóúàèìòùäëïöüñ]+[0-9a-z]*$', nombre, re.I)
    if nombre == "":
    	raise validators.ValidationError('Introduzca un Nombre o Username')
    if not validar :
        raise validators.ValidationError('Nombre no válido')     
##########################################################################################

#############----------------- Validaciones formulario Consulta-------------- ################
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
##########################################################################################


class ComentFormBus(Form):
    in_name = StringField('Nombre o Username: ',
    [
        val_nombre
    ])
    no_profiles = SelectField('Número  máximo de perfiles a buscar:', choices=[
        ('1',1),('2',2),('3',3),('4',4),('5',5),
        ('6',6),('7',7),('8',8),('9',9),('10',10)])
    no_posts = SelectField('Número  máximo de publicaciones por perfil:', choices=[
        ('1',1),('2',2),('3',3),('4',4),('5',5),
        ('6',6),('7',7),('8',8),('9',9),('10',10),
        ('11',11),('12',12),('13',13),('14',14),('15',15)])
    submit = SubmitField('')

class ComentFormCon(Form):
    in_name = StringField('Nombre: ',
    [
        val_nombre
    ]) 
    fecha_in = StringField('Fecha del : ', 
    [
        validators.InputRequired(message ='Fecha requerida')
    ])
    fecha_fin =StringField('al - ', 
    [
        validators.input_required(message='Fecha requerida')
    ])
    submit = SubmitField('')