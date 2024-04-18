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


class PizzaForm(Form):
            
        nombre=StringField("nombre",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa nombre valido')])
        direccion=StringField("direccion",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa direccion valido')])
        telefono=StringField("telefono",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=10,message='ingresa telefono valido')])
        tamañoPizza=RadioField("tamaño Pizza", 
                                        choices=[('chica','Chica $40'),('mediana','Mediana $80'),('grande','Grange $120')],
                                                validators=[validators.DataRequired(message='El campo es requerido')])
        
        jamon = BooleanField('Jamon $10', default=False)
        piña = BooleanField('Piña $10' , default=False)
        champiñones = BooleanField('Champiñones $10', default=False)
        numeroPizza=IntegerField("Numero de Pizzas",[validators.number_range(min=1, message='valor no valido')])
        fecha = DateField("Fecha", format='%Y-%m-%d', validators=[validators.DataRequired(message='El campo es requerido')])

class MateriaPrima(Form):
      nombreMateriaPrima=SelectField("producto: ",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa nombre valido')])
      proveedor=SelectField("proveedor: ",validators=[validators.DataRequired(message='El campo es requerido'),validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa proveedor valido')])
      fecha_entrada = DateField("Fecha de entrada: ", format='%Y-%m-%d', validators=[validators.DataRequired(message='El campo es requerido')])
      caducidad = DateField("Fecha de caducidad: ", format='%Y-%m-%d', validators=[validators.DataRequired(message='El campo es requerido')])
      cantidadExistente=IntegerField("Unidades ingresadas:",[validators.number_range(min=1, message='valor no valido')])
      tipoUnidad=SelectField("Unidad de medida", 
                                        choices=[('kg','kilogramo (KG)'),('ltr','Litro (ltr)'),('gr','gramos (gr)')],
                                                validators=[validators.DataRequired(message='El campo es requerido')])
    
class Proveedor(Form):
      nombreContacto=StringField("nombre de contacto: ",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa nombre valido')])
      telefonoContacto=StringField("teléfono de contacto: ",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=15,message='ingresa teléfono valido')])
      razon_social=StringField("razón social: ",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=50,message='ingresa razón social valida')])
      direccion=StringField("dirección: ",[validators.DataRequired(message='el campo es requerido'),
                                    validators.length(min=4,max=100,message='ingresa dirección valida')])
      minimo_compra=IntegerField("mínimo de compra",[validators.number_range(min=1, message='valor no valido')])
      maximo_compra=IntegerField("máximo de compra",[validators.number_range(min=1, message='valor no valido')])


class ListaProveedor():
        def __init__(self,nombreContacto,telefonoContacto,razon_social,direccion,minimo_compra,maximo_compra):
                self.nombreContacto=nombreContacto
                self.telefonoContacto=telefonoContacto
                self.razon_social=razon_social
                self.direccion=direccion
                self.minimo_compra=minimo_compra
                self.maximo_compra=maximo_compra