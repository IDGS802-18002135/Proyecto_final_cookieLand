from datetime import date
from datetime import datetime
from flask import Flask, request,render_template,Response
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from models import db
from io import open

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

        



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run()