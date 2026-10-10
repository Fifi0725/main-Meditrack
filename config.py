"""Configuración de MediTrack: base de datos (SQLAlchemy), claves y modo de pruebas."""
import os

# Carpeta donde vive este archivo (meditrack/). Se usa para construir la ruta
# de la base de datos.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # AVISO: cambia esta clave (variable de entorno SECRET_KEY) antes de
    # entregar o desplegar el proyecto.
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-me")

    # ERROR 4 (corregido): "sqlite:///meditrack.db" es una ruta RELATIVA, y
    # Flask 3.x crea ese archivo dentro de "instance/". Eso causó que existiera
    # un meditrack.db vacío (sin tablas) y la app no encontrara "medicamento".
    # Con una ruta ABSOLUTA, "flask db upgrade" y "flask run" siempre usan
    # el mismo archivo: meditrack/meditrack.db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "meditrack.db")
    )

    # ERROR 6 (eliminado): SQLALCHEMY_TRACK_MODIFICATIONS = False ya no hace
    # nada en Flask-SQLAlchemy 3.x (esa opción fue retirada), así que sobraba.

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # Base de datos en memoria: se crea y se destruye en cada prueba.
    SQLALCHEMY_DATABASE_URI = "sqlite://"
