from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField,RadioField,EmailField,IntegerField,SelectMultipleField,BooleanField,DateField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id')
    nombre=StringField("nombre",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=10,message='ingresa nombre valido')])
    
    apaterno=StringField('apaterno',[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=10,message='ingresa apellido valido')])
    
    amaterno=StringField('amaterno',[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=10,message='ingresa apellido valido')])
    
    direccion=StringField('direccion',[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=50,message='ingresa domicilio valido')])

    edad=IntegerField('edad',
                      [validators.number_range(min=1, message='valor no valido')])

    email=EmailField('correo',[
        validators.Email(message='Ingrese un correo valido'
                         )])