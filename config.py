import os
from sqlalchemy import create_engine
from encrypt import decrypt
class Config(object):
    SECRET_KEY='CLAVE SECRETA'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG=True
    usuario = decrypt(b'{\xf7\xc9KF\xb7\xf9T\xb0\xbd\xeb\x80\xd8\x0cb\xfb')
    passworld= decrypt(b'\xf4\x91c\xde\xbf\x8d\x82\xba\xd3\x81\xaa&\x8f8\xbea\xd8\xb9\x0e\x95\xb0\xdb\x96@[\n?~\xcd\xa3\x7f;')
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://{usuario}:{passworld}@127.0.0.1/cookieland'
