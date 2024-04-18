from datetime import datetime 
import re
from flask import Flask, flash, render_template, request, redirect, url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
import flask_login
import flask
from flask import Flask
from flask_login import LoginManager
from models import usuario,sanitizar,db,HistorialContrasenas
from puntoDeVenta.puntodeventa import puntoDeVenta
from flask_wtf.csrf import CSRFProtect
from .forms import RegistroForm,LoginForms
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
            
            historial_contraseña = HistorialContrasenas(
                usuario_id=user.idUsuario,
                contrasena=pass_encrypt,
                fecha_creacion=datetime.now()
            )
            db.session.add(historial_contraseña)
            db.session.commit()
            flash('Registro exitoso', 'success')  # Mostrar mensaje de éxito
            return redirect(url_for("log.login")) # Redirigir a una ruta después del registro
    return render_template("signup.html", form=formulario)


@log.route("/login", methods=["GET", "POST"])

def login():
    formulario_login = LoginForms()
    if request.method == "POST" and formulario_login.validate():
       
        user = sanitizar().sanitize_input(formulario_login.email.data)
       
        lista_usuario = usuario.query.filter(usuario.correo == user).first()
        idUsuario = lista_usuario.idUsuario
        user = usuario.query.get(idUsuario)
        login_user(user)
        return redirect(url_for("puntoDeVenta.punto_De_Venta"))
            
                
    return render_template("login.html",form=formulario_login)


def encriptar(dato):
    pass_encrypt = generate_password_hash(dato)
    return pass_encrypt

