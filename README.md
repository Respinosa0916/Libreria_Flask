# Comandos para el uso de Flask

## Creación del entorno virtual
Para crear un entorno virtual en Python, ejecuta el siguiente comando:
```bash
python -m venv venv
```

## Entrar al entorno virtual
```bash
.\env\Script\activate
```

## Instalacion de las librerias de flask ya estando en el entorno virtual
```bash
pip install -r requirements.txt
```
> **Nota:** Las librerias de flask se deben de instalar dentro del entorno virtual, por ende debes de entrar primero al entorno virtual

## Si no tienes la base de datos en el arhcivo .env esta el nombre de la base de datos "library_db" y se inicializa con el siguiente codigo
```bash
python init_admin.py
```
> **Nota:** El nombre de la base de datos tiene que se library_db si en tu base de datos le pusiste otro nombre modifica el archivo .env

## Inicial proyecto
```bash
python run.py
```

## Por defecto el usuario de admin ya esta predeterminado en la base de datos
```bash
Correo: admin@biblioteca.com
Password: admin123
```
