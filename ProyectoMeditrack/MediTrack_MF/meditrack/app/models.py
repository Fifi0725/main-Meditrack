"""Modelos de datos de la base de datos de MediTrack."""
from datetime import datetime, timezone

from app import db


class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    laboratorio = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    requiere_receta = db.Column(db.Boolean, nullable=False, default=False)

    fecha_registro = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Medicamento {self.id}: {self.nombre}>"
