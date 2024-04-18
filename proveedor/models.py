from flask_sqlalchemy import SQLAlchemy
import datetime
import re


db=SQLAlchemy()

class Venta(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombreVenta=db.Column(db.String(50))
    direccionVenta=db.Column(db.String(50))
    telefonoVenta=db.Column(db.String(50))
    totalVenta=db.Column(db.Integer)
    create_dateVenta = db.Column(db.DateTime)

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
    compra_minimo=db.Column(db.Integer,default=1)
    compra_maxima=db.Column(db.Integer,default=1)

class ProveedorDao:
    def __init__(self, idProveedor, nombreContacto, telefonoContacto, razon_social, direccion, compra_minimo=1, compra_maxima=1):
        self.idProveedor = idProveedor
        self.nombreContacto = nombreContacto
        self.telefonoContacto = telefonoContacto
        self.razon_social = razon_social
        self.direccion = direccion
        self.compra_minimo = compra_minimo
        self.compra_maxima = compra_maxima


