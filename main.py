from datetime import date, datetime
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, galleta, detallesreceta, ventas, detalleventas
import creacionArch
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
app._static_folder='static'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/", methods=["POST", "GET"])
def main():
    manejador = creacionArch.manejadorArchivo('ticket.txt') 
    galletas = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).all()    
    receta = detallesreceta.query.all()
    print("galletas existentes:", galletas)
    print("recetas relacionadas con galletas:", receta)
    respuesta = manejador.mostrar_contenido()
    respuestaform = request.form 
    if request.method == 'POST':
        if respuestaform.get("_method") == "DELETE":
            eliminacion = manejador.eliminar(int(respuestaform.get("indice")))
            print("indice"+respuestaform.get("indice")+"respuesta"+eliminacion)
            respuesta = manejador.mostrar_contenido()
            return render_template("PV.html", galletas=galletas, recetas=receta, respuesta=respuesta if respuesta else [], mensaje=eliminacion )
        elif respuestaform.get("_method") == "SUBMIT":
            total=0.0
            for re in respuesta:
                dato = re.split(":")
                sub = dato[5]
                total=total+float(sub)
                print(sub)
                print("total"+str(total))
                
            venta = ventas(
                idUsuario=1,
                totalVenta=total  # Asigna el total de la venta
            )
            db.session.add(venta)
            db.session.commit()
            db.session.flush()
            
            for rep in respuesta:
                dato = rep.split(":")
                nombre = dato[0]
                c7=dato[1]
                c1=dato[2]
                pz=dato[3]
                p=dato[4]
                sub=dato[5]
                gall = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).filter(detallesreceta.nombreReceta == nombre).all()
                
             # Crear una instancia de la clase DetalleVentas
                detalle_venta = detalleventas(
                    idVenta=venta.idVenta,
                    fecha_venta=datetime.now(),
                    c_1=c1,
                    c_7=c7,
                    c_pz=pz,
                    c_pesos=p,
                    id_galleta=gall[0].id_galleta,  # Asigna el id de la galleta
                    subtotal=sub,  # Asigna el subtotal
                    razon_retiro="Nada"  # Asigna la razón de retiro si corresponde, en este caso lo dejamos como None
                )
                db.session.add(detalle_venta)
            
            
            # Realizar la transacción
            db.session.commit()
            insercion = manejador.eliminar_todo()
            respuesta = manejador.mostrar_contenido()
            return render_template("PV.html", galletas=galletas, recetas=receta, respuesta=respuesta if respuesta else [] ,mensaje=insercion  )
        else:  
            nombre = str(respuestaform.get("nombre"))
            gall = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).filter(detallesreceta.nombreReceta == nombre).all()
            subtotal=0
            caja7 = int(respuestaform.get("cajas700", "").strip()) if respuestaform.get("cajas700", "").strip() else 0
            caja1=int(respuestaform.get("cajas1","").strip()) if respuestaform.get("cajas1", "").strip() else 0
            piezas=int(respuestaform.get("piezas","").strip()) if respuestaform.get("piezas", "").strip() else 0
            pesos=int(respuestaform.get("pesos","").strip()) if respuestaform.get("pesos", "").strip() else 0
            for galle in gall:
                precio700 = galle.precio_caja700
                precio1=galle.precio_caja1
                preciopz=galle.precio_unidad
                print(f"ID: {galle.idDetallesReceta}, precio unidad: {galle.precio_unidad}, Precio: {galle.precio_caja1}")
            subtotal=(int(precio700)*int(caja7))+(int(precio1)*int(caja1))+(int(piezas)*int(preciopz))+int(pesos)   
            if subtotal == 0:
                insercion= "Sin valores al agregar"
                respuesta = manejador.mostrar_contenido()
            else:    
                insercion = manejador.insertar(str(respuestaform.get("nombre"))+":"+str(caja7)+":"+str(caja1)+":"+str(piezas)+":"+str(pesos)+":"+str(subtotal))
                respuesta = manejador.mostrar_contenido()
              
                 
            return render_template("PV.html", galletas=galletas, recetas=receta, respuesta=respuesta if respuesta else [], mensaje=insercion )

          
        
       
    return render_template("PV.html", galletas=galletas, recetas=receta, respuesta=respuesta if respuesta else [])

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()
