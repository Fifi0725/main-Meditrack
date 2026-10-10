"""Formulario para crear y editar medicamentos."""
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)

from wtforms.validators import DataRequired, InputRequired, Length, NumberRange


class MedicamentoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=100, message="Máximo 100 caracteres."),
        ],
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria.")],
    )
    laboratorio = StringField(
        "Laboratorio",
        validators=[
            DataRequired(message="El laboratorio es obligatorio."),
            Length(max=100, message="Máximo 100 caracteres."),
        ],
    )
    precio = FloatField(
        "Precio",
        validators=[
            InputRequired(message="El precio es obligatorio."),
            NumberRange(min=0, message="El precio no puede ser negativo."),
        ],
    )
    stock = IntegerField(
        "Stock",
        validators=[
            InputRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock no puede ser negativo."),
        ],
    )
    fecha_vencimiento = DateField(
        "Fecha de vencimiento",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de vencimiento es obligatoria.")],
    )
    requiere_receta = BooleanField("Requiere receta")
    submit = SubmitField("Guardar medicamento")
