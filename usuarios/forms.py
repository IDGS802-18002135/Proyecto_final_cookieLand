from datetime import datetime 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,BooleanField,SubmitField,IntegerField, ValidationError,validators,EmailField
from wtforms.validators import DataRequired, Length, Email,EqualTo
from models import HistorialContrasenas, usuario,logslogin,db
from werkzeug.security import generate_password_hash, check_password_hash
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El campo es requerido'),
        Length(min=3, max=20, message='Este campo nombre no puede estar vacío ni contener más de 20 caracteres')
    ])
    app = StringField('Apellido Paterno', validators=[
        DataRequired(message='El campo es requerido'),
        Length(min=3, max=50, message='Este campo "Apellido Paterno" no puede estar vacío ni contener más de 50 caracteres')
    ])
    apm = StringField('Apellido Materno', validators=[
        DataRequired(message='El campo es requerido'),
        Length(min=3, max=50, message='Este campo "Apellido Materno" no puede estar vacío ni contener más de 50 caracteres')
    ])
    email = EmailField('Correo Electrónico', validators=[
        DataRequired(message='El campo es requerido'),
        Email(message='Dirección de correo electrónico no válida'),
        Length(min=8, max=50, message='Este correo no puede estar vacío ni contener más de 50 caracteres')
    ])
    password = PasswordField('Contraseña', validators=[
        
        Length(min=0, max=50, message='Agrega una contraseña')
    ])
    confirmar_password= PasswordField('Confirmar Contraseña', validators=[
        
        Length(min=0, max=50, message='Agrega una contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    
    estatus = SelectField('Estatus', choices=[('0', 'Inactivo'), ('1', 'Activo')])
    
    def validate_password(self, password):
        if password.data :
            # Verifica si la contraseña contiene al menos una mayúscula, una minúscula, un número y un carácter especial
            caracteres_especiales = "!@#$%^&*()-_+=<>?/,.|{}[]"
            tiene_mayuscula = False
            tiene_minuscula = False
            tiene_numero = False
            tiene_caracter_especial = False

            for caracter in password.data:
                if caracter.isupper():
                    tiene_mayuscula = True
                elif caracter.islower():
                    tiene_minuscula = True
                elif caracter.isdigit():
                    tiene_numero = True
                elif caracter in caracteres_especiales:
                    tiene_caracter_especial = True

            if not (tiene_mayuscula and tiene_minuscula and tiene_numero and tiene_caracter_especial):
                raise ValidationError('La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.')

            # Verifica si la contraseña está en la lista de contraseñas comunes
            contrasenas_comunes = {
                '123456', 'contraseña', 'qwerty', '123456789', '12345678', '1234567',
                'Contraseña1!', 'C@mbio123', 'Bienvenido123!', 'admin123', 'Admin@123',
                'dejadmeentrar1', 'dejadmeentrar!', 'cambiadme1', 'cambiadme!', '1234567890',
                'abcdefg1', 'ABCDEFG1', '!@#$%^&*()', 'contraseña123', 'adminadmin',
                'usuario', 'root', 'qazwsx', '123456aA!', '1234abcd!', 'qwerty123!',
                'contraseña1!', 'contraseña!', 'prueba123!', 'bienvenido1!', '123456789aA!',
                '1234567890!', '123456789a!', 'abc123!', '123abc!', 'Abc123!', 'Abcdefg1!',
                'Contraseña123!', 'Pass123!', 'Passw0rd!', 'Contraseña!', 'C@mbiar123!',
                'C@mbio!123', 'C@mbio123!', 'Qwerty!123', 'Qwerty!@#', 'Qwerty!1234',
                'Qwerty123!', 'Qwerty@123', 'qwerty!123', 'qwerty!@#', 'qwerty!1234',
                'qwerty123!', 'qwerty@123', 'password123', 'Password1!', 'P@ssw0rd',
                'Welcome123!', 'letmein1', 'letmein!', 'changeme1', 'changeme!',
                'test123!', 'welcome1!', '123456789aA!', '1234567890!', '123456789a!',
                'password1!', 'password!', 'admin123!', 'abc123!', '123abc!', 'Abc123!',
                'Abcdefg1!', 'Password123!', 'Passw0rd!', 'P@ssword!', 'P@ssw0rd!',
                'Password!23', 'Password!@#', 'Password!123', 'P@ssw0rd!123',
                'P@ssword!123'
            }


            
            if password.data in contrasenas_comunes:
                raise ValidationError('La contraseña es demasiado común. Por favor, elige una contraseña más segura.')
            
            historial_contraseñas = HistorialContrasenas.query.filter_by(contrasena=password.data).first()
            if historial_contraseñas:
                raise ValidationError('La contraseña ha sido utilizada anteriormente. Por favor, elige una nueva contraseña.')
            
            user = usuario.query.filter_by(correo=self.email.data).first()
            if user:
                password_bd = user.contrasena
                if check_password_hash(password_bd, password.data):
                    
                    raise ValidationError('Si va a actuaalizar su contraseña no puede ser igual a la actual')
                
                