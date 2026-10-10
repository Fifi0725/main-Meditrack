import os
import sys
import unittest
import tempfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app import crear_web
from app.database import db_conexion

class BibliotecaTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.temp_db = tempfile.mkstemp()
        self.app = crear_web({
            "TESTING": True,
            "DATABASE_PATH": self.temp_db,
            "WTF_CSRF_ENABLED": False
        })
        self.client = self.app.test_client()

    def setUp(self):
        self.db_fd, self.temp_db = tempfile.mkstemp()
        self.app = crear_web({
            "TESTING": True,
            "DATABASE_PATH": self.temp_db,
            "WTF_CSRF_ENABLED": False
        })
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.temp_db)

    def test_index_status(self):
        """La ruta principal debe devolver 200"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_crear_libro(self):
        """Se debe poder crear un libro"""
        response = self.client.post("/crear", data={
            "titulo": "El Quijote",
            "autor": "Cervantes",
            "fecha": "1605-01-16",
            "editorial": "Francisco de Robles",
            "genero": "Historia",
            "portada": "https://example.com/img.jpg"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            conexion = db_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()
            self.assertEqual(len(libros), 1)

    def test_editar_libro(self):
        """Se debe poder editar un libro"""

        with self.app.app_context():
            conexion = db_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO libros (titulo, autor, fecha, editorial, genero, portada)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("Libro", "Autor", "2020-01-01", "Edit", "Fantasia", ""))
            conexion.commit()

        response = self.client.post("/editar/1", data={
            "titulo": "Libro Editado",
            "autor": "Autor Nuevo",
            "fecha": "2021-02-02",
            "editorial": "Nueva Editorial",
            "genero": "Historia",
            "portada": "https://example.com/edit.jpg"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_eliminar_libro(self):
        """Se debe poder eliminar un libro"""

        with self.app.app_context():
            conexion = db_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO libros (titulo, autor, fecha, editorial, genero, portada)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("Test", "Yo", "2000-01-01", "X", "Terror", ""))
            conexion.commit()

        response = self.client.post("/eliminar/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            conexion = db_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()
            self.assertEqual(len(libros), 0)


if __name__ == "__main__":
    unittest.main()