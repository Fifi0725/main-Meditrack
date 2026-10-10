"""Rutas para crear, editar y eliminar medicamentos (CRUD)."""
from flask import Blueprint, flash, redirect, render_template, url_for

from app import db
from app.gestion.forms import MedicamentoForm
from app.models import Medicamento

gestion_bp = Blueprint("gestion", __name__, url_prefix="/medicamentos")


def _datos_del_formulario(form):
    """Devuelve solo los campos que pertenecen al modelo.

    ERROR 8 (corregido): crear y editar repetían siete asignaciones iguales.
    Aquí queda un único lugar para mantenerlas.

    No se incluye fecha_registro a propósito: la base de datos la llena sola
    (ver models.py), así que no hace falta en la ruta de crear ni en la de
    editar (la fecha de registro no debe cambiar al editar).
    """
    return {
        "nombre": form.nombre.data.strip(),
        "descripcion": form.descripcion.data.strip(),
        "laboratorio": form.laboratorio.data.strip(),
        "precio": form.precio.data,
        "stock": form.stock.data,
        "fecha_vencimiento": form.fecha_vencimiento.data,
        "requiere_receta": form.requiere_receta.data,
    }


@gestion_bp.route("/nuevo", methods=["GET", "POST"])
def crear_medicamento():
    form = MedicamentoForm()

    if form.validate_on_submit():
        medicamento = Medicamento(**_datos_del_formulario(form))
        db.session.add(medicamento)
        db.session.commit()

        flash("Medicamento creado correctamente.", "success")
        return redirect(url_for("main.listarMeds"))

    return render_template("formulario.html", form=form, titulo="Nuevo medicamento")


@gestion_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar_medicamento(id):
    medicamento = db.get_or_404(Medicamento, id)
    form = MedicamentoForm(obj=medicamento)

    if form.validate_on_submit():
        for campo, valor in _datos_del_formulario(form).items():
            setattr(medicamento, campo, valor)
        db.session.commit()

        flash("Medicamento actualizado correctamente.", "success")
        return redirect(url_for("main.detallesMeds", medicamento_id=medicamento.id))

    return render_template("formulario.html", form=form, titulo="Editar medicamento")


@gestion_bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar_medicamento(id):
    medicamento = db.get_or_404(Medicamento, id)
    db.session.delete(medicamento)
    db.session.commit()

    flash("Medicamento eliminado correctamente.", "success")
    return redirect(url_for("main.listarMeds"))
