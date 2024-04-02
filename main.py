from datetime import date
from datetime import datetime
from flask import Flask, request,render_template,Response
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from models import db
from io import open
from models import Proveedor

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

        
@app.route("/materiaprima",methods=["GET","POST"])
def materiaprima():
    materiaprima_form=forms.MateriaPrima(request.form)
    if request.method=='POST'  and materiaprima_form.validate:
        nombreMateriaPrima=materiaprima_form.nombreMateriaPrima.data
        proveedor=materiaprima_form.proveedor.data
        fecha_entrada=materiaprima_form.fecha_entrada.data
        caducidad=materiaprima_form.caducidad.data
        cantidadExistente=materiaprima_form.cantidadExistente.data
        tipoUnidad=materiaprima_form.tipoUnidad.data

        
    return render_template("materiaPrima.html",form=materiaprima_form)

@app.route("/proveedor",methods=["GET","POST"])
def proveedor():
    listaProveedor=""
    proveedor_form=forms.Proveedor(request.form)
    if request.method=='POST'  and proveedor_form.validate:

        proveedor=Proveedor(
                            
                            nombreContacto=proveedor_form.nombreContacto.data,
                            telefonoContacto=proveedor_form.telefonoContacto.data,
                            razon_social=proveedor_form.razon_social.data,
                            direccion=proveedor_form.direccion.data,
                            compra_minimo=proveedor_form.minimo_compra.data,
                            compra_maxima=proveedor_form.maximo_compra.data)
        db.session.add(proveedor)
        db.session.commit()
    
    listaProveedor=Proveedor.query.all()
    print(listaProveedor)
    
    return render_template("proveedor.html",form=proveedor_form,listaProveedor=listaProveedor)

if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run()