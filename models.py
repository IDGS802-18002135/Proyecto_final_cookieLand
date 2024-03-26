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