from datetime import date
from datetime import datetime
from flask import Flask, redirect, request,render_template,Response, url_for
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from models import db
from io import open
from models import Proveedor,usuario

from flask import Blueprint
from proveedor.proveedor import proveedores
from materiaprima.materiaprima import materia_prima
from catalogo_materiaprima.catalogo_materia_prima import catalogo_mp
from login._login import log
from flask_login import LoginManager, login_required, logout_user


app=Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)  # donde 'app' es tu aplicación Flask


@login_manager.user_loader
def load_user(user_id):
    user=usuario.query.get(int(user_id))
    print(user)
    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(log.login)

app.config.from_object(DevelopmentConfig)
app._static_folder="static"
csrf=CSRFProtect()






@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404





app.register_blueprint(proveedores)
app.register_blueprint(materia_prima)
app.register_blueprint(catalogo_mp)
app.register_blueprint(log)

def status_401(error):
    return redirect(url_for('log.login'))



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_error_handler(401, status_401)
 
    
    app.run()