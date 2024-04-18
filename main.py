from datetime import date, datetime
from flask import Flask, redirect, request, render_template, send_from_directory, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, galleta, detallesreceta, ventas, detalleventas,usuario
import creacionArch
from sqlalchemy.orm import joinedload
from proveedor.proveedor import proveedores
from materiaprima.materiaprima import materia_prima
from catalogo_materiaprima.catalogo_materia_prima import catalogo_mp
from puntoDeVenta.puntodeventa import puntoDeVenta
from usuarios.usuarios import usuario_
import logging
from flask_cors import CORS
from login._login import log

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)  # donde 'app' es tu aplicación Flask

ips = {
    "http://192.168.228.65:5000"
}
CORS(puntoDeVenta,origins=ips)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
app._static_folder='static'
logging.getLogger('flask_cors').level = logging.DEBUG
logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(proveedores)
app.register_blueprint(materia_prima)
app.register_blueprint(catalogo_mp)
app.register_blueprint(puntoDeVenta)
app.register_blueprint(log)
app.register_blueprint(usuario_)


@login_manager.user_loader
def load_user(user_id):
    user=usuario.query.get(int(user_id))
    print(user)
    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("log.login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    app.logger.debug('Esto es un mensaje de depuración')
    return "Intento de conexión"

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run(host='0.0.0.0', debug=True)
