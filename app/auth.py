from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, UserType
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        user = User.query.filter_by(correo=correo).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            
            # Redirigir según el tipo de usuario
            tipo_usuario = UserType.query.get(user.tipo_usuario_id)
            if tipo_usuario.nombre == "Usuario":
                return redirect(url_for("usuario.listar_libros"))
            else:
                return redirect(url_for("admin.dashboard"))
        else:
            flash("Por favor verifica tus credenciales e intenta nuevamente.")

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("password")

        # Verifica si el correo ya está registrado
        if User.query.filter_by(correo=correo).first():
            flash("El correo ya está registrado. Intenta iniciar sesión.")
            return redirect(url_for("auth.register"))

        # Obtiene el tipo de usuario "Usuario"
        tipo_usuario = UserType.query.filter_by(nombre="Usuario").first()
        if not tipo_usuario:
            # Crea el tipo "Usuario" si no existe
            tipo_usuario = UserType(nombre="Usuario")
            db.session.add(tipo_usuario)
            db.session.commit()

        # Crea el nuevo usuario
        nuevo_usuario = User(
            nombre=nombre,
            correo=correo,
            password=generate_password_hash(password, method="sha256"),
            tipo_usuario_id=tipo_usuario.id
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


