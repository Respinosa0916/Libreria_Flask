from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .models import Libro, Autor, Categoria
from . import db
from datetime import datetime
import os

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo_usuario_id != 1:  # Asumiendo que 1 es el ID para administradores
        flash('Acceso no autorizado')
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

# CRUD Libros
@admin.route('/libros')
@login_required
def libros():
    libros = Libro.query.all()
    return render_template('admin/libros/index.html', libros=libros)

@admin.route('/libros/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_libro():
    if request.method == 'POST':
        libro = Libro(
            isbn=request.form.get('isbn'),
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            fecha_publicacion=datetime.strptime(request.form.get('fecha_publicacion'), '%Y-%m-%d'),
            precio=request.form.get('precio'),
            autor_id=request.form.get('autor_id'),
            categoria_id=request.form.get('categoria_id')
        )
        
        # Manejar la subida de la portada
        if 'portada' in request.files:
            file = request.files['portada']
            if file.filename:
                # Ruta al directorio de uploads
                uploads_dir = os.path.join(current_app.root_path, 'static/uploads')
                # Crear el directorio si no existe
                os.makedirs(uploads_dir, exist_ok=True)
                # Nombre del archivo
                filename = f"{libro.isbn}_{file.filename}"
                # Guardar el archivo
                file.save(os.path.join(uploads_dir, filename))
                # Guardar el nombre en la base de datos
                libro.portada = filename

        db.session.add(libro)
        db.session.commit()
        flash('Libro creado exitosamente')
        return redirect(url_for('admin.libros'))
    
    autores = Autor.query.all()
    categorias = Categoria.query.all()
    return render_template('admin/libros/nuevo.html', autores=autores, categorias=categorias)

@admin.route('/libros/editar/<isbn>', methods=['GET', 'POST'])
@login_required
def editar_libro(isbn):
    libro = Libro.query.get_or_404(isbn)
    if request.method == 'POST':
        libro.titulo = request.form.get('titulo')
        libro.descripcion = request.form.get('descripcion')
        libro.fecha_publicacion = datetime.strptime(request.form.get('fecha_publicacion'), '%Y-%m-%d')
        libro.precio = request.form.get('precio')
        libro.autor_id = request.form.get('autor_id')
        libro.categoria_id = request.form.get('categoria_id')
        
        # Manejar la subida de una nueva portada
        if 'portada' in request.files:
            file = request.files['portada']
            if file.filename:
                # Ruta al directorio de uploads
                uploads_dir = os.path.join(current_app.root_path, 'static/uploads')
                # Crear el directorio si no existe
                os.makedirs(uploads_dir, exist_ok=True)
                
                # Generar el nombre del archivo
                filename = f"{libro.isbn}_{file.filename}"
                file_path = os.path.join(uploads_dir, filename)
                
                # Eliminar la portada anterior si existe
                if libro.portada:
                    old_file_path = os.path.join(uploads_dir, libro.portada)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Guardar el nuevo archivo
                file.save(file_path)
                libro.portada = filename

        db.session.commit()
        flash('Libro actualizado exitosamente')
        return redirect(url_for('admin.libros'))
    
    autores = Autor.query.all()
    categorias = Categoria.query.all()
    return render_template('admin/libros/editar.html', libro=libro, autores=autores, categorias=categorias)

@admin.route('/libros/eliminar/<isbn>', methods=['POST'])
@login_required
def eliminar_libro(isbn):
    libro = Libro.query.get_or_404(isbn)
    
    # Eliminar el archivo de portada si existe
    if libro.portada:
        uploads_dir = os.path.join(current_app.root_path, 'static/uploads')
        portada_path = os.path.join(uploads_dir, libro.portada)
        if os.path.exists(portada_path):
            os.remove(portada_path)
    
    # Eliminar el libro de la base de datos
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado exitosamente')
    return redirect(url_for('admin.libros'))

# CRUD Autores
@admin.route('/autores')
@login_required
def autores():
    autores = Autor.query.all()
    return render_template('admin/autores/index.html', autores=autores)

@admin.route('/autores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_autor():
    if request.method == 'POST':
        autor = Autor(
            nombre=request.form.get('nombre'),
            apellido=request.form.get('apellido'),
            fecha_nacimiento=datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d')
        )
        db.session.add(autor)
        db.session.commit()
        flash('Autor creado exitosamente')
        return redirect(url_for('admin.autores'))
    return render_template('admin/autores/nuevo.html')

@admin.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_autor(id):
    autor = Autor.query.get_or_404(id)
    if request.method == 'POST':
        autor.nombre = request.form.get('nombre')
        autor.apellido = request.form.get('apellido')
        autor.fecha_nacimiento = datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d')
        db.session.commit()
        flash('Autor actualizado exitosamente')
        return redirect(url_for('admin.autores'))
    return render_template('admin/autores/editar.html', autor=autor)

@admin.route('/autores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_autor(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    flash('Autor eliminado exitosamente')
    return redirect(url_for('admin.autores'))


# CRUD Categorías
@admin.route('/categorias')
@login_required
def categorias():
    categorias = Categoria.query.all()
    return render_template('admin/categorias/index.html', categorias=categorias)

@admin.route('/categorias/nueva', methods=['GET', 'POST'])
@login_required
def nueva_categoria():
    if request.method == 'POST':
        categoria = Categoria(nombre=request.form.get('nombre'))
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada exitosamente')
        return redirect(url_for('admin.categorias'))
    return render_template('admin/categorias/nuevo.html')

@admin.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form.get('nombre')
        db.session.commit()
        flash('Categoría actualizada exitosamente')
        return redirect(url_for('admin.categorias'))
    return render_template('admin/categorias/editar.html', categoria=categoria)

@admin.route('/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada exitosamente')
    return redirect(url_for('admin.categorias'))