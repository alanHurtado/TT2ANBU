###---------------- DEFINICIONES Y VALIDACIONES DE FORMULARIOS ----------------###

#:::: Este componente define los tipos y nombres de los campos utilizados
# en los formularios del sistema, también define las funciones correspondientes
# de cada campo para evaluar y condicionar los datos de entrada. 

import sys, re, time
from wtforms import Form  # Importar instancia de los formularios
from wtforms import StringField, SubmitField , SelectField  # Tipos de campos en formularios
from wtforms import validators  # Realizar validaciones

#::::::::::::::::: VALIDACIONES para el formulario de BUSQUEDA :::::::::::::::::#
def val_nombre(form, field):
    nombre = field.data
    validar = re.match('^@?[a-z\s_áéíóúàèìòùäëïöüñ]+[0-9a-z]*$', nombre, re.I)
    if nombre == "":
    	raise validators.ValidationError('Introduzca un Nombre o Username')
    if not validar :
        raise validators.ValidationError('Nombre no válido')     
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

#::::::::::::::: VALIDACIONES para el formulario de CONSULTA :::::::::::::::#
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
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#


#:::::::::: DEFINICIONES de campos para el formulario de BUSQUEDA ::::::::::#
class ComentFormBus(Form):
    in_name = StringField('Nombre o Username: ',
    [
        val_nombre
    ])
    no_profiles = SelectField('Número  máximo de perfiles a buscar:',
            choices=[
                ('1',1),('2',2),('3',3),('4',4),('5',5),
                ('6',6),('7',7),('8',8),('9',9),('10',10)]
            )
    no_posts = SelectField('Número  máximo de publicaciones por perfil:',
            choices=[
                ('1',1),('2',2),('3',3),('4',4),('5',5),
                ('6',6),('7',7),('8',8),('9',9),('10',10),
                ('11',11),('12',12),('13',13),('14',14),('15',15)]
            )
    submit = SubmitField('')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

#::::: DEFINICIONES de campos para el formulario de CONSULTA :::::#
class ComentFormCon(Form):
    in_name = StringField('Nombre:')
     
    fecha_in = StringField('Fecha del : ', 
    [
        validators.InputRequired(message ='Fecha requerida')
    ])
    fecha_fin =StringField('al - ', 
    [
        validators.input_required(message='Fecha requerida')
    ])
    submit = SubmitField('')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
class ComentFormReport(Form):
    id_con = StringField('id')
    submit = SubmitField('')