from datetime import date
from datetime import datetime
from flask import Flask, request,render_template,Response,redirect,url_for
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
from wtforms import SelectMultipleField,BooleanField
from .forms import materiaPrimaCatalogo
from config import DevelopmentConfig
from models import db
from io import open
from models import Proveedor,Materiaprima,materiaprimacatalogo,proveedor_materia_prima,sanitizar

from wtforms import validators
from flask import Blueprint
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


catalogo_mp= Blueprint('catalogo_mp',__name__,template_folder='./templates',)
sanitizar_object=sanitizar()

@catalogo_mp.route("/catalogo_materia_prima",methods=["GET","POST"])
@login_required
def catalogo_materia_prima():

    listaCatalogo=""
    listaCatalogo=materiaprimacatalogo.query.all()

    mp_catalogo_form=materiaPrimaCatalogo(request.form)
    if request.method=='POST'  and mp_catalogo_form.validate() and "ingresarCatalogo" in request.form:
        nuevo_catalogo=materiaprimacatalogo(
            nombre=sanitizar_object.sanitize_input(mp_catalogo_form.nombre.data),
            compra_minimo=sanitizar_object.sanitize_input(mp_catalogo_form.minimo_compra.data),
            compra_maxima=sanitizar_object.sanitize_input(mp_catalogo_form.maximo_compra.data)

        )
        db.session.add(nuevo_catalogo)
        db.session.commit()
        return redirect (url_for('catalogo_mp.catalogo_materia_prima'))
    return render_template("catalogo_mp.html",form=mp_catalogo_form, listaCatalogo=listaCatalogo)

@catalogo_mp.route("/eliminar", methods=["GET","POST"])
def eliminar():
    mp_catalogo_form=materiaPrimaCatalogo(request.form)

    if request.method=='POST':
        print("HUUH")
        print(mp_catalogo_form.id.data)
        idMateriaPrimaCatalogo=sanitizar_object.sanitize_input(mp_catalogo_form.id.data)
        mp=materiaprimacatalogo.query.get(idMateriaPrimaCatalogo)
        mp.estatus=0
        db.session.commit()

        return redirect(url_for('catalogo_mp.catalogo_materia_prima'))
        
        
    return render_template('catalogo_materia_prima.html',form=mp_catalogo_form)