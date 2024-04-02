from flask_sqlalchemy import SQLAlchemy
import datetime


db=SQLAlchemy()

class Venta(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombreVenta=db.Column(db.String(50))
    direccionVenta=db.Column(db.String(50))
    telefonoVenta=db.Column(db.String(50))
    totalVenta=db.Column(db.Integer)
    create_dateVenta = db.Column(db.DateTime)

class materiaPrima(db.Model):
    idMateriaPrima=db.Column(db.Integer,primary_key=True)
    nombreMateriaPrima=db.Column(db.String(50))
    idProveedor=db.Column(db.Integer,foreign_key=True)
    fecha_entrada=db.Column(db.DateTime)
    fecha_salida=db.Column(db.DateTime)
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
