from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
import flask_login
import flask
from flask import Flask
from forms import LoginForm
from flask_login import LoginManager
from models import usuario,sanitizar,usuario,db,administrador,ventas,produccion
from .forms import RegistroForm
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig


from flask import Flask
from flask_login import LoginManager,login_user,login_required


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)




log= Blueprint('log',__name__,template_folder='./templates',)

@log.route("/signup", methods=["GET", "POST"])
@login_required
def signup():
    formulario = RegistroForm()
    if request.method == 'POST' and formulario.validate():
        
        pass_sanitizada = sanitizar().sanitize_input(formulario.password.data)
        if pass_sanitizada == formulario.password.data:
            pass_encrypt = encriptar(pass_sanitizada)
            user = usuario(
                nombreUsuario=formulario.nombre.data,
                apellidoPaterno=formulario.app.data,
                apellidoMaterno=formulario.apm.data,
                correo=formulario.email.data,
                contrasena=pass_encrypt,
                estatus=formulario.estatus.data
            )
            db.session.add(user)
            db.session.commit()  # Confirmar los cambios en la base de datos
            print()
            flash('Registro exitoso', 'success')  # Mostrar mensaje de éxito
            return redirect(url_for('puntoDeVenta.punto_De_Venta'))  # Redirigir a una ruta después del registro
    return render_template("signup.html", form=formulario)

def encriptar(dato):
    pass_encrypt = generate_password_hash(dato)
    return pass_encrypt





@log.route("/login",methods=["GET","POST"])

def login():
    try:
        user=""
        password=""
        sanitizar_object=sanitizar()
        
    
        if request.method=="POST":
        
            user=sanitizar_object.sanitize_input(request.form["nombreUsuario"])
        
            #print(sanitizar_object.sanitize_input("---user"))
            password=sanitizar_object.sanitize_input(request.form["contrasena"])
        
            #print(sanitizar_object.sanitize_input("---password"))
            lista_usuario=usuario.query.filter(usuario.correo==user,usuario.contrasena == password)
            
            
            user=""
            passwordConsultado=""
            idUsuario=0
            for item in lista_usuario:
                
                user=item.correo
                passwordConsultado=item.contrasena
                idUsuario=item.idUsuario
            
            

            if user==None or passwordConsultado==None:
                print("Usuario no existe")
                return render_template("login.html")
            if user==user and passwordConsultado==password:
        

                user=usuario.query.get(int(idUsuario))
                print(user.idUsuario)
                try:
                    login_user(user)
                    
                    print("Sesión iniciada")
                    flash('Sesión iniciada', 'success')
                except Exception as e:
                    print("Error al iniciar sesión:", e)

            
                #username=current_user.nombreUsuario
                #print(current_user.nombreUsuario)
                #rol=current_user.rol
                #ultima=current.ultimaConexxion

                if ventas().ventas(current_user.idRol):
                    return redirect(url_for("url para punto de venta"))
                if produccion().produccion(current_user.idRol):
                    return redirect(url_for("proveedores.proveedor"))
                if administrador().administrador(current_user.idRol):
                    return redirect(url_for("proveedores.proveedor"))
                else:
                    return render_template("<h1>No cuenta con un permiso asignado</h1>")
            else:
                print("Usuario no existe o es invalido",)
                flash("Usuario no existe o es invalido","error")
                return render_template("login.html")
            
            
        return render_template("login.html")
    except Exception as e:
                print("Error:", e)
                flash('Sucedió algo inesperado contacte con el administrador','error')







@log.route("/forbiden",methods=["GET","POST"])

def forbiden():
    try:
        return render_template("forbidden.html")
    except Exception as e:
                print("Error:", e)
                flash('Sucedió algo inesperado contacte con el administrador','error')
