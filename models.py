from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re


db=SQLAlchemy()



class Materiaprima(db.Model):
    idMateriaPrima=db.Column(db.Integer,primary_key=True)
    nombreMateriaPrima=db.Column(db.String(50))
    idProveedor=db.Column(db.Integer)
    fecha_entrada=db.Column(db.DateTime)
    
    caducidad=db.Column(db.DateTime)
    cantidadExistente=db.Column(db.Integer)
    tipoUnidad=db.Column(db.String(10))




class Proveedor(db.Model):
    idProveedor=db.Column(db.Integer,primary_key=True)
    nombreContacto=db.Column(db.String(50))
    telefonoContacto=db.Column(db.String(15))
    razon_social=db.Column(db.String(100))
    direccion=db.Column(db.String(100))
    

class ProveedorDao:
    def __init__(self, idProveedor, nombreContacto, telefonoContacto, razon_social, direccion, compra_minimo=1, compra_maxima=1):
        self.idProveedor = idProveedor
        self.nombreContacto = nombreContacto
        self.telefonoContacto = telefonoContacto
        self.razon_social = razon_social
        self.direccion = direccion
        self.compra_minimo = compra_minimo
        self.compra_maxima = compra_maxima

class materiaprimacatalogo(db.Model):
    idMateriaPrimaCatalogo=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    compra_minimo=db.Column(db.Integer)
    compra_maxima=db.Column(db.Integer)
    estatus=db.Column(db.Integer)

class proveedor_materia_prima(db.Model):
    idProveedor_materia_prima=db.Column(db.Integer,primary_key=True)
    idProveedor=db.Column(db.Integer)
    idMateriaPrimaCatalogo=db.Column(db.Integer)


class usuario(db.Model,UserMixin):
    idUsuario=db.Column(db.Integer,primary_key=True)
    nombreUsuario=db.Column(db.String(20))
    apellidoPaterno=db.Column(db.String(20))
    apellidoMaterno=db.Column(db.String(20))
    correo =db.Column(db.String(50))
    contrasena =db.Column(db.String(50))
    idRol =db.Column(db.Integer,default=1)
    estatus=db.Column(db.String(5))
    
    #def set_password(self, password):
     #   self.password = generate_password_hash(password)
    
    def get_id(self):
        return str(self.idUsuario)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.correo)


    
      # Nuevo campo para indicar si el usuario está activo

    


      

class sanitizar:
    def sanitize_input(self,input_string):
        # Define una expresión regular para encontrar solo caracteres alfanuméricos y espacios
        regex_pattern = re.compile(r'[^.@a-zA-Z0-9\s]')

        # Aplica la expresión regular para eliminar caracteres no deseados
        sanitized_string = re.sub(regex_pattern, '', input_string)
        return sanitized_string
    

class administrador:
    def administrador(self, rol):
        if rol==1:
            return True
        else:
            return False

class produccion:
    def produccion(self, rol):
        if rol==2:
            return True
        else:
            return False

class ventas:
    def ventas(self, rol):
        if rol==3:
            return True
        else:
            return False