"""Fábrica de la aplicación MediTrack.

ERROR 1 (corregido): el docstring original decía "Rutas y formularios para la
gestión de medicamentos", pero este archivo NO tiene rutas ni formularios:
solo crea y configura la aplicación Flask.
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # ERROR 2 (corregido): los modelos no se importaban de forma explícita.
    # Si Alembic no "ve" la clase Medicamento antes de migrar, no sabe que
    # existe la tabla y la migración sale vacía.
    # ERROR 5 (corregido): una versión anterior importaba
    # "from app.gestion import models", pero ese archivo no existe; el modelo
    # está en app/models.py.
    from app import models  # noqa: F401

    from app.routes import main
    from app.gestion.routes import gestion_bp

    app.register_blueprint(main)
    app.register_blueprint(gestion_bp)

    # ERROR 3 (la causa real de "no such table: medicamento"): en ningún
    # momento se creaban las tablas. Flask-Migrate NO las crea al arrancar.
    # Solución automática: create_all() crea las tablas que falten cada vez
    # que arranca la app (si ya existen, no las toca ni borra datos).
    # Limitación: si luego cambias las columnas de models.py, create_all NO
    # modifica una tabla ya creada; en ese caso borra meditrack/meditrack.db
    # y vuelve a arrancar (o usa "flask db migrate" + "flask db upgrade").
    with app.app_context():
        db.create_all()

    return app