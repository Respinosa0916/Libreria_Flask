from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Libro
from . import db

usuario = Blueprint("usuario", __name__)

@usuario.route("/libros")
@login_required
def listar_libros():
    # Consulta todos los libros desde la base de datos
    libros = Libro.query.all()
    return render_template("usuario/libros.html", libros=libros)


@usuario.route("/libros/<isbn>")
def detalle_libro(isbn):
    libro = Libro.query.filter_by(isbn=isbn).first_or_404()
    return render_template("usuario/detalle_libro.html", libro=libro)

@usuario.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verificar la contraseña actual
        if not check_password_hash(current_user.password, current_password):
            flash('La contraseña actual no es correcta.', 'error')
            return redirect(url_for('usuario.perfil'))

        # Verificar que las nuevas contraseñas coincidan
        if new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden.', 'error')
            return redirect(url_for('usuario.perfil'))

        # Actualizar la contraseña
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Contraseña actualizada con éxito.', 'success')
        return redirect(url_for('usuario.perfil'))

    return render_template('usuario/perfil.html')
