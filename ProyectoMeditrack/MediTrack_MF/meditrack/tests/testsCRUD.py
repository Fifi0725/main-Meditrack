import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from flask import template_rendered
from config import TestConfig
from app.models import Medicamento
from datetime import date, timedelta

class CsrfConfig(TestConfig):
    WTF_CSRF_ENABLED = True  # habilita CSRF para probarlo

DATOS = {
    "nombre": "Paracetamol",
    "descripcion": "Analgésico y antipirético",
    "laboratorio": "Mk",
    "precio": 5.0,
    "stock": 20,
    "fecha_vencimiento": date(2025, 12, 31),
    "requiere_receta": "y",
}

class BaseTest(unittest.TestCase):
    config = TestConfig
    def setUp(self):
        self.app = create_app(self.config)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.ctx.pop()

    def crear(self, **cambios):
        valores = {
            "nombre": "ibuprofeno",
            "descripcion": "Antiinflamatorio",
            "laboratorio": "Bayer",
            "precio": 50.0,
            "stock": 100,
            "fecha_vencimiento": date(2025, 12, 31),
            "requiere_receta": False,
        }
        valores.update(cambios)
        medicamento = Medicamento(**valores)
        db.session.add(medicamento)
        db.session.commit()
        return medicamento

class TestModelo(BaseTest):
    def test_fecha_registro_se_llena_sola(self):
        medicamento = self.crear()
        self.assertIsInstance(medicamento.fecha_registro, date)

    def test_se_guardan_todos_los_campos(self):
        medicamento = self.crear()
        self.assertEqual(medicamento.nombre, "ibuprofeno")
        self.assertEqual(medicamento.descripcion, "Antiinflamatorio")
        self.assertEqual(medicamento.laboratorio, "Bayer")
        self.assertEqual(medicamento.precio, 50.0)
        self.assertEqual(medicamento.stock, 100)
        self.assertEqual(str(medicamento.fecha_vencimiento), "2025-12-31")
        self.assertFalse(medicamento.requiere_receta)

if __name__ == "__main__":
    unittest.main()