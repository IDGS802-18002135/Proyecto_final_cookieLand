from datetime import datetime 
from flask import  Flask, flash, redirect, request, render_template,Blueprint,session, url_for
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import HistorialContrasenas, db, usuario
from .forms import RegistroForm
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

usuario_= Blueprint('usuario_',__name__,template_folder='./templates',)

@usuario_.route("/usuarios", methods=["POST", "GET"])
@login_required
def usuarios():
    respuesta_formulario = request.form
    lista_usuarios = usuario.query.all()
    if request.method == "POST":
        method = respuesta_formulario["_method"]
        idusuario = respuesta_formulario["idUsuario"]
        usuario_ = usuario.query.filter(usuario.idUsuario==idusuario).first()
        
    return render_template("usuarios.html",lista=lista_usuarios)    
            
            

@usuario_.route("/desactive_user", methods=["POST", "GET"])
@login_required
def des_user():
    respuesta_formulario = request.form
    if request.method == "POST":
        idusuario = respuesta_formulario["idUsuario"]
        usuario_ = usuario.query.filter(usuario.idUsuario==idusuario).first()
        usuario_.estatus=0
        db.session.commit()
        print("Estatus al desactivar"+str(usuario_.estatus))
        flash("Desactivado con exito","success")
        return redirect(url_for("usuario_.usuarios"))
    flash("Error al eliminar","warning")
    return render_template("usuarios.html")    

@usuario_.route("/active_user", methods=["POST", "GET"])
@login_required
def act_user():
    respuesta_formulario = request.form
    if request.method == "POST":
        idusuario = respuesta_formulario["idUsuario"]
        usuario_ = usuario.query.filter(usuario.idUsuario==idusuario).first()
        usuario_.estatus=1
        db.session.commit()
        print("Estatus al activar"+str(usuario_.estatus))
        
        flash("Activado con exito","success")
        return redirect(url_for("usuario_.usuarios"))
    flash("Error al eliminar","warning")
    return render_template("usuarios.html")    
                                     

@usuario_.route("/editar_usuario", methods=["POST", "GET"])
@login_required
def edit_usu():
    respuesta_formulario = request.form
    formulario = RegistroForm()
    if request.method == "POST":
        idusuario = respuesta_formulario["idUsuario"]
        usuario_ = usuario.query.filter(usuario.idUsuario==idusuario).first()
        if usuario_:
        
            return render_template("usuarios_edit.html", form=formulario, usuario=usuario_)
    
    return redirect(url_for("usuario_.usuarios") )          
@usuario_.route("/actualizar_usuario", methods=["POST", "GET"])
@login_required
def actualizar_usu():
    respuesta_formulario = request.form
    formulario = RegistroForm()
    idusuario = respuesta_formulario["idUsuario"]
    usuario_ = usuario.query.filter(usuario.idUsuario==idusuario).first()
    if formulario.validate() and usuario_:
        # Actualización de los datos del usuario
        usuario_.nombreUsuario = formulario.nombre.data
        usuario_.apellidoPaterno = formulario.app.data
        usuario_.apellidoMaterno = formulario.apm.data
        usuario_.correo = formulario.email.data
        usuario_.estatus = formulario.estatus.data
        
        if formulario.password.data:
            pass_encrypt = encriptar(formulario.password.data)
            usuario_.contrasena = pass_encrypt
        db.session.commit()
        if formulario.password.data:
            # Registro de la contraseña en el historial
            pass_encrypt = encriptar(formulario.password.data)
            
            historial_contraseña = HistorialContrasenas(
                usuario_id=usuario_.idUsuario,
                contrasena=pass_encrypt,
                fecha_creacion=datetime.now()
            )
            db.session.add(historial_contraseña)
            db.session.commit()

        flash('Actualización de usuario exitosa', 'success')
        print("contraseña: "+ formulario.password.data)
        
        return render_template("usuarios_edit.html", form=formulario, usuario=usuario_)
    
    
    return render_template("usuarios_edit.html", form=formulario, usuario=usuario_)


def encriptar(dato):
    pass_encrypt = generate_password_hash(dato)
    return pass_encrypt

  