from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField,RadioField,EmailField,IntegerField,SelectMultipleField,BooleanField,DateField
from wtforms import EmailField
from wtforms import validators

class galletasform(Form):
    
    caja1=IntegerField('cajas1',[validators.number_range(min=1,max= 2, message="ingrese alguna cantidad ")])
    caja700=IntegerField('cajas700',[validators.number_range(min=1,max= 2, message="ingrese alguna cantidad entre")])
    piezas=IntegerField('piezas',[validators.number_range(min=1,max= 2, message="ingrese alguna cantidad entre")])
    pesos=IntegerField('pesos',[validators.number_range(min=1,max= 2, message="ingrese alguna cantidad entre")])