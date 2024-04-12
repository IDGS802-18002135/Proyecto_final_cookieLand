from datetime import date, datetime
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, galleta, detallesreceta, ventas, detalleventas
import creacionArch
from sqlalchemy.orm import joinedload
from proveedor.proveedor import proveedores
from materiaprima.materiaprima import materia_prima
from catalogo_materiaprima.catalogo_materia_prima import catalogo_mp
from puntoDeVenta.puntodeventa import puntoDeVenta

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
app._static_folder='static'

app.register_blueprint(proveedores)
app.register_blueprint(materia_prima)
app.register_blueprint(catalogo_mp)
app.register_blueprint(puntoDeVenta)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()
