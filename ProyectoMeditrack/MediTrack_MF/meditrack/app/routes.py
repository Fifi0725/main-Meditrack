"""Rutas principales: panel de control, listado/búsqueda, detalle y errores."""
from datetime import date, timedelta
from flask import Blueprint, render_template, request
from app import db
from app.models import Medicamento

main = Blueprint("main", __name__)

# Umbrales para las alertas del panel y de las tablas.
# unidades o menos = "stock bajo"
STOCK_BAJO = 10  
# vence dentro de este número de días = "por vencer"
DIAS_POR_VENCER = 30  

@main.route("/")
def dashboard():
    hoy = date.today()
    limite = hoy + timedelta(days=DIAS_POR_VENCER)

    def contar(*condiciones):
        return db.session.scalar(
            db.select(db.func.count(Medicamento.id)).where(*condiciones)
        )

    resumen = {
        "total": contar(),
        "stock_bajo": contar(Medicamento.stock <= STOCK_BAJO),
        "por_vencer": contar(
            Medicamento.fecha_vencimiento >= hoy,
            Medicamento.fecha_vencimiento <= limite,
        ),
        "vencidos": contar(Medicamento.fecha_vencimiento < hoy),
    }
    recientes = db.session.scalars(
        db.select(Medicamento).order_by(Medicamento.fecha_registro.desc()).limit(5)
    ).all()

    return render_template(
        "dashboard.html",
        resumen=resumen,
        recientes=recientes,
        stock_bajo=STOCK_BAJO,
        dias=DIAS_POR_VENCER,
    )

@main.route("/listarMedicamentos")
def listarMeds():
    # Búsqueda opcional por nombre o laboratorio: /listarMedicamentos?q=para
    q = request.args.get("q", "").strip()
    consulta = db.select(Medicamento).order_by(Medicamento.nombre)
    if q:
        patron = f"%{q}%"
        consulta = consulta.where(
            db.or_(
                Medicamento.nombre.ilike(patron),
                Medicamento.laboratorio.ilike(patron),
            )
        )
    medicamentos = db.session.scalars(consulta).all()

    return render_template(
        "medicamentos/consultas/buscarMeds.html",
        medicamentos=medicamentos,
        q=q,
        hoy=date.today(),
        stock_bajo=STOCK_BAJO,
        dias=DIAS_POR_VENCER,
    )

@main.route("/detallesMedicamentos/<int:medicamento_id>")
def detallesMeds(medicamento_id):
    medicamento = db.get_or_404(Medicamento, medicamento_id)
    return render_template(
        "medicamentos/consultas/detailsMeds.html",
        medicamento=medicamento,
        hoy=date.today(),
        stock_bajo=STOCK_BAJO,
        dias=DIAS_POR_VENCER,
    )


@main.app_errorhandler(404)
def not_found(error):
    return render_template("errores/404.html"), 404

@main.app_errorhandler(500)
def internal_error(error):
    # Si falló la base de datos, la sesión queda dañada: se limpia antes de
    # volver a pintar la página.
    db.session.rollback()
    return render_template("errores/500.html"), 500
