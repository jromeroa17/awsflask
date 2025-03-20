from sqlalchemy import ForeignKey
from . import db
from flask_login import UserMixin


class Instancia(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    name = db.Column(db.String(150))
    opsys = db.Column(db.String(50))
    keypairs = db.Column(db.String(50))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    Instance = db.Relationship('Instancia')