from datetime import date
from datetime import datetime
from flask import Flask, flash, request,render_template,Response,redirect,url_for
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect
from .forms import MateriaPrima
from config import DevelopmentConfig
from models import administrador, db
from io import open
from models import Proveedor,materiaprimacatalogo
from models import Materiaprima,sanitizar
from flask import Blueprint

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

materia_prima= Blueprint('materia_prima',__name__,template_folder='./templates',)
sanitizar_object=sanitizar()
@materia_prima.route("/materiaprima",methods=["GET","POST"])
@login_required
def materiaprima():
    try:
        if administrador().administrador(current_user.idRol):
            materiaprima_form=MateriaPrima(request.form)
            #
            lista_proveedores = Proveedor.query.all()
            opciones_proveedores = [(proveedor.idProveedor, proveedor.razon_social) for proveedor in lista_proveedores]
            materiaprima_form.proveedor.choices = opciones_proveedores
            #

            #
            lista_catalogomp=materiaprimacatalogo.query.all() 
            opciones_materia_prima=[(catalogomp.idMateriaPrimaCatalogo, catalogomp.nombre) for catalogomp in lista_catalogomp]
            materiaprima_form.nombreMateriaPrima.choices = opciones_materia_prima
            #

            
            listaMateriaPrima=Materiaprima.query.all()
            lista_nombre_proveedor=[]
            for item in listaMateriaPrima:
                lista_proveedor_id=Proveedor.query.filter(Proveedor.idProveedor==item.idProveedor)
                for item in lista_proveedor_id:
                    lista_nombre_proveedor.append(item.razon_social)


            for item in lista_nombre_proveedor:
                print(item)
        
            
                


            if request.method=='POST'  and materiaprima_form.validate:
                
                mp=Materiaprima(
                    nombreMateriaPrima=sanitizar_object.sanitize_input(materiaprima_form.nombreMateriaPrima.data),
                    idProveedor=sanitizar_object.sanitize_input(materiaprima_form.proveedor.data),
                    fecha_entrada=sanitizar_object.sanitize_input(materiaprima_form.fecha_entrada.data),
                    
                    caducidad=sanitizar_object.sanitize_input(materiaprima_form.caducidad.data),
                    cantidadExistente=sanitizar_object.sanitize_input(materiaprima_form.cantidadExistente.data),
                    tipoUnidad=sanitizar_object.sanitize_input(materiaprima_form.tipoUnidad.data)
                )
                db.session.add(mp)
                db.session.commit()
                db.session.flush()
                print(materia_prima)
                return redirect (url_for('materia_prima.materiaprima'))
            
                

                
            return render_template("materiaPrima.html",form=materiaprima_form,listaMateriaPrima=listaMateriaPrima,lista_nombre_proveedor=lista_nombre_proveedor)
        else:
            return render_template("forbidden.html")
    except Exception as e:
                print("Error:", e)
                flash('Sucedió algo inesperado contacte con el administrador','error')

    

    