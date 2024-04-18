from datetime import date, datetime
from flask import Flask, request, render_template,Blueprint,session
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, current_user, login_required, logout_user, login_user, login_required, logout_user

from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, galleta, detallesreceta, ventas, detalleventas
import creacionArch
from sqlalchemy.orm import joinedload

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

puntoDeVenta= Blueprint('puntoDeVenta',__name__,template_folder='./templates',)


@puntoDeVenta.route("/puntoDeVenta", methods=["POST", "GET"])
@cross_origin(origins="http://192.168.228.65:5000")
@login_required
def punto_De_Venta():
    
    manejador = creacionArch.manejadorArchivo('ticket.txt') 
    galletas = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).all()    
    receta = detallesreceta.query.all()
    print("galletas existentes:", galletas)
    print("recetas relacionadas con galletas:", receta)
    ticket = manejador.mostrar_contenido()
    formulario = request.form 
  
    
    if request.method == 'POST':
       
        if formulario.get("_method") == "DELETE":
            eliminacion = manejador.eliminar(int(formulario.get("indice")))
            print("indice"+formulario.get("indice")+"ticket"+eliminacion)
            ticket = manejador.mostrar_contenido()
            return render_template("PV.html", galletas=galletas, recetas=receta, ticket=ticket if ticket else [], mensaje=eliminacion )
        elif  formulario.get("_method") == "DELETE-ALL":
            eliminacion= manejador.eliminar_todo()
            ticket = manejador.mostrar_contenido()
            return render_template("PV.html", galletas=galletas, recetas=receta, ticket=ticket if ticket else [], mensaje=eliminacion )
            
        elif formulario.get("_method") == "SUBMIT":
            total=0.0
            for re in ticket:
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
            
            for rep in ticket:
                dato = rep.split(":")
                nombre = dato[0]
                c7=dato[1]
                c1=dato[2]
                pz=dato[3]
                p=dato[4]
                sub=dato[5]
                gall = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).filter(detallesreceta.nombreReceta == nombre).all()
                if gall:
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
                    gall[0].existencias_caja700 -= int(c7)
                    gall[0].existencias_caja1 -= int(c1)
                    gall[0].existencias_pieza -= int(pz)
                else:
                    # Maneja la situación si la galleta no se encuentra en la base de datos
                    print(f"No se encontró la galleta con nombre {nombre} en la base de datos.")   
            
            
            # Realizar la transacción
            db.session.commit()
            insercion = manejador.eliminar_todo()
            ticket = manejador.mostrar_contenido()
            return render_template("PV.html", galletas=galletas, recetas=receta, ticket=ticket if ticket else [] ,mensaje=insercion  )
        else:  
            nombre = str(formulario.get("nombre"))
            gall = db.session.query(galleta).join(detallesreceta).options(joinedload(galleta.detalles_receta)).filter(detallesreceta.nombreReceta == nombre).all()
            subtotal=0
            caja7 = int(formulario.get("cajas700", "").strip()) if formulario.get("cajas700", "").strip() else 0
            caja1=int(formulario.get("cajas1","").strip()) if formulario.get("cajas1", "").strip() else 0
            piezas=int(formulario.get("piezas","").strip()) if formulario.get("piezas", "").strip() else 0
            pesos=int(formulario.get("pesos","").strip()) if formulario.get("pesos", "").strip() else 0
            for galle in gall:
                precio700 = galle.precio_caja700
                precio1=galle.precio_caja1
                preciopz=galle.precio_unidad
                print(f"ID: {galle.idDetallesReceta}, precio unidad: {galle.precio_unidad}, Precio: {galle.precio_caja1}")
            subtotal=(int(precio700)*int(caja7))+(int(precio1)*int(caja1))+(int(piezas)*int(preciopz))+int(pesos)   
            if subtotal == 0:
                insercion= "Sin valores al agregar"
                ticket = manejador.mostrar_contenido()
            else:    
                insercion = manejador.insertar(str(formulario.get("nombre"))+":"+str(caja7)+":"+str(caja1)+":"+str(piezas)+":"+str(pesos)+":"+str(subtotal))
                ticket = manejador.mostrar_contenido()
              
            
     
            return render_template("PV.html", galletas=galletas, recetas=receta, ticket=ticket if ticket else [], mensaje=insercion )

          
        
       
    return render_template("PV.html", galletas=galletas, recetas=receta, ticket=ticket if ticket else [])
