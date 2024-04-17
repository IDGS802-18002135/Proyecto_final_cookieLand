from datetime import date
from datetime import datetime
from flask import Flask, flash, request,render_template,Response,redirect,url_for
from flask_cors import cross_origin
from flask_wtf.csrf import CSRFProtect
from wtforms import SelectMultipleField,BooleanField
from .forms import ProveedorForms,materiaPrimaCatalogo
from config import DevelopmentConfig

from flask_login import LoginManager, current_user, login_required, logout_user, login_user, login_required, logout_user

from models import db
from io import open
from models import Proveedor,Materiaprima,materiaprimacatalogo,proveedor_materia_prima,sanitizar,usuario
from models import administrador,ventas,produccion

from wtforms import validators
from flask import Blueprint
app=Flask(__name__)





app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


proveedores= Blueprint('proveedores',__name__,template_folder='./templates',)




@proveedores.route("/proveedor",methods=["GET","POST"])

@login_required
def proveedor():
    try:
        if administrador().administrador(current_user.idRol):
            
            # username=current_user.nombreUsuario
            #rol=current_user.rol
        
            


            
            sanitizar_object=sanitizar()
            listaIngredientes=""
            listaIngredientes=materiaprimacatalogo.query.all()

            #test=materiaprimacatalogo.query.all()
            #print("AAAAAAAAAAAAAA")
            #print(test)
            
            
            for i in listaIngredientes:
                # print(i.idMateriaPrima)
                # print(i.nombreMateriaPrima)
                a=str(i.idMateriaPrimaCatalogo)
                b=str(i.nombre)
                setattr(ProveedorForms, "i"+a , BooleanField(b))
                
                

            


            listaProveedor=""
            
            
            proveedor_form=ProveedorForms(request.form)

            mp_catalogo_form=materiaPrimaCatalogo(request.form)
            
            
            #  print(i)
                #proveedor_form.ingredientes.choices += [(i.idMateriaPrima, i.nombreMateriaPrima)]

            if "agregarCatalogo" in request.form:
                
                
        
                


                
                mpCatalogo=materiaprimacatalogo(
                    nombre=sanitizar_object.sanitize_input(mp_catalogo_form.nombre.data),
                    compra_minimo=sanitizar_object.sanitize_input(str(mp_catalogo_form.minimo_compra.data)),
                    compra_maxima=sanitizar_object.sanitize_input(str(mp_catalogo_form.maximo_compra.data))

                )
                db.session.add(mpCatalogo)
                db.session.commit()

                return redirect (url_for('proveedores.proveedor'))
            
            

            if request.method=='POST'  and proveedor_form.validate() and "ingresar" in request.form:
                print("?????????????????")
                proveedor=Proveedor(
                                    
                                    nombreContacto=sanitizar_object.sanitize_input(proveedor_form.nombreContacto.data),
                                    telefonoContacto=sanitizar_object.sanitize_input(proveedor_form.telefonoContacto.data),
                                    razon_social=sanitizar_object.sanitize_input(proveedor_form.razon_social.data),
                                    direccion=sanitizar_object.sanitize_input(proveedor_form.direccion.data)
                                    
                                    )
                #compra_minimo=proveedor_form.minimo_compra.data,
                                    #compra_maxima=proveedor_form.maximo_compra.data
                db.session.add(proveedor)
                db.session.commit()
                db.session.flush()
                print("id??: ")
                print(proveedor.idProveedor)

                print("AQUIIIIIIIIIIIIIIIIIIII")
                atributos = vars(proveedor_form)

                # Iterar sobre los atributos y sus valores
                for nombre_atributo, valor_atributo in atributos.items():
                    # Verificar si el nombre del atributo comienza con 'i' seguido de un número
                    if nombre_atributo.startswith('i') and nombre_atributo[1:].isdigit():
                        # Obtener el valor del atributo
                        valor = getattr(proveedor_form, nombre_atributo).data
                        print(f"El valor de {nombre_atributo} es: {valor}")
                        if valor==True:
                            #inserta en la base
                            numero=nombre_atributo.split("i") 
                            proveedorXcatalogomp=proveedor_materia_prima(
                                idProveedor=proveedor.idProveedor,
                                idMateriaPrimaCatalogo=numero[1]
                            )
                            db.session.add(proveedorXcatalogomp)
                            db.session.commit()

                return redirect (url_for('proveedores.proveedor'))
            
            listaProveedor=Proveedor.query.all()
            print(listaProveedor)

            
            return render_template("proveedor.html",form2=mp_catalogo_form,form=proveedor_form,listaProveedor=listaProveedor,listaIngredientes=listaIngredientes)#username=username,rol=rol)
    


        else:
            return render_template("forbidden.html")
    except Exception as e:
                print("Error:", e)
                flash('Sucedió algo inesperado contacte con el administrador','error')




