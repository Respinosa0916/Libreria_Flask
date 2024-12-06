from app import create_app, db
from app.models import UserType, User
from werkzeug.security import generate_password_hash

def init_database():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if UserType already exists
        if not UserType.query.first():
            # Create user types
            admin_type = UserType(nombre='Administrador')
            user_type = UserType(nombre='Usuario')
            db.session.add(admin_type)
            db.session.add(user_type)
            db.session.commit()
            
            # Create admin user
            admin = User(
                nombre='Administrador',
                correo='admin@biblioteca.com',
                password=generate_password_hash('admin123', method='sha256'),
                tipo_usuario_id=admin_type.id
            )
            db.session.add(admin)
            db.session.commit()
            print('Base de datos inicializada con éxito.')
            print('Credenciales del administrador:')
            print('Email: admin@biblioteca.com')
            print('Contraseña: admin123')
        else:
            print('La base de datos ya está inicializada.')