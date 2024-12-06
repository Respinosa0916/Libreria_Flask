from . import db
from flask_login import UserMixin
from datetime import datetime

class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='tipo_user', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    libros = db.relationship('Libro', backref='autor', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    libros = db.relationship('Libro', backref='categoria', lazy=True)

class Libro(db.Model):
    isbn = db.Column(db.String(13), primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    portada = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    fecha_publicacion = db.Column(db.Date)
    precio = db.Column(db.Numeric(10, 2))
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)