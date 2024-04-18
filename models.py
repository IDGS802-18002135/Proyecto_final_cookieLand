import re
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime


db=SQLAlchemy()

class ventas(db.Model):
    __tablename__ = 'ventas'
    idVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    totalVenta = db.Column(db.Float)
    idUsuario= db.Column(db.Integer)
    detalle_venta = db.relationship("detalleventas", back_populates="venta")
   
class detalleventas(db.Model):
    __tablename__ = 'detalleventas'
    idDetalleVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('ventas.idVenta'), nullable=False)
    fecha_venta = db.Column(db.Date)
    id_galleta = db.Column(db.Integer)
    c_1 = db.Column(db.Integer)
    c_7 = db.Column(db.Integer)
    c_pz = db.Column(db.Integer)
    c_pesos = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    razon_retiro = db.Column(db.String(250))
    venta = db.relationship("ventas", backref="detalleventas")


class galleta(db.Model):
    __tablename__ = 'galleta'
    id_galleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idDetallesReceta = db.Column(db.Integer, db.ForeignKey('detallesreceta.idDetallesReceta'), nullable=False)
    precio_unidad = db.Column(db.Float)
    precio_caja700 = db.Column(db.Float)
    precio_caja1 = db.Column(db.Float)
    minimo_stock_caja700 = db.Column(db.Integer)
    minimo_stock_caja1 = db.Column(db.Integer)
    minimo_stock_pieza = db.Column(db.Integer)
    existencias_caja700 = db.Column(db.Integer)
    existencias_caja1= db.Column(db.Integer)
    existencias_pieza = db.Column(db.Integer)

    detalles_receta = db.relationship('detallesreceta', backref='galleta')
    def __repr__(self):
        return f'<Galleta {self.id_galleta}>'
    
class detallesreceta(db.Model):
    __tablename__ = 'detallesreceta'
    idDetallesReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreReceta = db.Column(db.String(50))
    minimo_produccion = db.Column(db.Integer, nullable=False)
    maximo_produccion = db.Column(db.Integer, nullable=False)
    pesoFinal = db.Column(db.Integer, nullable=False)
    cantidad_a_producir = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(300))
    img_galleta = db.Column(db.String(255))
    costo_receta = db.Column(db.Float)
    def __repr__(self):
        return f'<DetallesReceta {self.idDetallesReceta}>'
    
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
    def _init_(self, idProveedor, nombreContacto, telefonoContacto, razon_social, direccion, compra_minimo=1, compra_maxima=1):
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
    __tablename__ = 'usuario'
    idUsuario=db.Column(db.Integer,primary_key=True)
    nombreUsuario=db.Column(db.String(20))
    apellidoPaterno=db.Column(db.String(20))
    apellidoMaterno=db.Column(db.String(20))
    correo =db.Column(db.String(50))
    contrasena =db.Column(db.String(250))
    idRol =db.Column(db.Integer,default=1)
    estatus=db.Column(db.String(5))
    logs = db.relationship('logslogin', backref='usuario')
    def get_id(self):
        return self.idUsuario
    
class logslogin(db.Model):
    idLog = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    accion = db.Column(db.String(250))
    detalle = db.Column(db.String(250))
    fecha = db.Column(db.Date)    
class HistorialContrasenas(db.Model):
    __tablename__ = 'historial_contrasenas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    contrasena = db.Column(db.String(250), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
 


      

class sanitizar:
    def sanitize_input(self,input_string):
        # Define una expresión regular para encontrar solo caracteres alfanuméricos y espacios
        regex_pattern = re.compile(r'[^.@a-zA-Z0-9\s]')

        # Aplica la expresión regular para eliminar caracteres no deseados
        sanitized_string = re.sub(regex_pattern, '', input_string)
        return sanitized_string