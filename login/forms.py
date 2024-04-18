from datetime import datetime 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,BooleanField,SubmitField,IntegerField, ValidationError,validators,EmailField
from wtforms.validators import DataRequired, Length, Email,EqualTo
from models import usuario,logslogin,db
from werkzeug.security import generate_password_hash, check_password_hash
class LoginForms(FlaskForm):
    email=StringField("Usuario(email) ",validators=[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=1,max=50,message='Este campo no puede estar vacio ni contener mas de 10 caracteres')])
    
    password=PasswordField('Contraseña ',validators=[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=8,max=50,message='Intenta de nuevo, contraseña invalida')])
    def validate_email(self, email):
        user = usuario.query.filter_by(correo=email.data).first()
        if not user:
            registrar_log(email.data, 'login', 'Intento de inicio de sesión fallido - Correo no registrado')

            raise ValidationError('Este correo electrónicono no se encuentra registrado')
        

        
    def validate_password(self,password):
        user = usuario.query.filter_by(correo=self.email.data).first()
        if user:
            password_bd = user.contrasena
            if not check_password_hash(password_bd, password.data):
                registrar_log(self.email.data, 'login', 'Intento de inicio de sesión fallido con el correo registrado: '+str(self.email.data))
                
                raise ValidationError('Contraseña incorrecta, intente de nuevo')
            else:
                registrar_log(self.email.data, 'login', 'Intento de inicio de sesión exitoso con el correo registrado: '+str(self.email.data))
                
def registrar_log(user_, accion, detalle):
    nuevo_log = logslogin(usuario_id=0, accion=accion, detalle=detalle, fecha=datetime.now())
    user = usuario.query.filter_by(correo=user_).first()
    if user:
        nuevo_log = logslogin(usuario_id=user.idUsuario, accion=accion, detalle=detalle, fecha=datetime.now())
    db.session.add(nuevo_log)
    db.session.commit() 
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[validators.DataRequired(message='el campo es requerido'),])
    password = PasswordField('Password', [validators.DataRequired(message='el campo es requerido'),])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

    
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
        DataRequired(message='El campo es requerido'),
        Length(min=8, max=50, message='Agrega una contraseña')
    ], render_kw={"type": "password"})
    confirmar_password= PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='El campo es requerido'),
        Length(min=8, max=50, message='Agrega una contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    estatus = SelectField('Estatus', choices=[('0', 'Inactivo'), ('1', 'Activo')])
    mostrar_password = BooleanField('Mostrar contraseña')
    
    def validate_email(self, email):
        user = usuario.query.filter_by(correo=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está en uso. Por favor, elige otro.')
    
    def validate_password(self, password):
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