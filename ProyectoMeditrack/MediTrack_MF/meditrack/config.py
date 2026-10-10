"""Configuración de MediTrack: base de datos (SQLAlchemy), claves y modo de pruebas."""
import os

#Se usa para construir la ruta de la base de datos.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # AVISO: cambia esta clave (variable de entorno SECRET_KEY) antes de
    # entregar o desplegar el proyecto.
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-me")

 
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "meditrack.db")
    )

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # Base de datos en memoria: se crea y se destruye en cada prueba.
    SQLALCHEMY_DATABASE_URI = "sqlite://"
