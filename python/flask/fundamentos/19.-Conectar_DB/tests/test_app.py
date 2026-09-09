import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pymysql

from app import app
from mascota import Mascota
from mysqlconnection import MySQLConnection
from usuario import Usuario


FECHA = datetime(2026, 1, 1, 12, 0)
MASCOTA = {
    "id": 3, "nombre": "Luna", "tipo": "Perro", "color": "Blanco",
    "created_at": FECHA, "updated_at": FECHA,
}
USUARIO = {
    "id": 1, "nombre": "Ana Torres", "email": "ana.torres@example.com",
    "edad": 24, "created_at": FECHA, "updated_at": FECHA,
}


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        self.mascotas = patch("mascota.connectToMySQL").start()
        self.usuarios = patch("usuario.connectToMySQL").start()
        self.addCleanup(patch.stopall)

    def test_listado(self):
        self.mascotas.return_value.query_db.return_value = [MASCOTA]
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Luna", response.data)
        self.assertIn(b"Blanco", response.data)

    def test_listado_vacio(self):
        self.mascotas.return_value.query_db.return_value = []
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No existen mascotas registradas", response.data)

    def test_rutas_invalidas_no_consultan(self):
        for ruta in ("/mascotas/3", "/mascotas/999", "/mascotas/abc",
                     "/mascotas/-1", "/desconocida"):
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code, 404)
        self.mascotas.assert_not_called()
        self.usuarios.assert_not_called()

    def test_usuarios(self):
        self.usuarios.return_value.query_db.return_value = [USUARIO]
        response = self.client.get("/usuarios")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ana Torres", response.data)
        self.assertIn(b"ana.torres@example.com", response.data)
        self.assertIn(b"24", response.data)

    def test_usuarios_vacios(self):
        self.usuarios.return_value.query_db.return_value = []
        response = self.client.get("/usuarios")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No existen usuarios registrados", response.data)

    def test_errores_consulta_y_conexion_son_503(self):
        for ruta, conexion in (("/", self.mascotas),
                               ("/usuarios", self.usuarios)):
            for fallo in ("consulta", "conexion"):
                with self.subTest(ruta=ruta, fallo=fallo):
                    conexion.side_effect = None
                    conexion.return_value.query_db.return_value = False
                    if fallo == "conexion":
                        conexion.side_effect = pymysql.OperationalError(
                            "clave-super-secreta SELECT datos privados"
                        )
                    with self.assertLogs(app.logger, level="ERROR") as logs:
                        response = self.client.get(ruta)
                    self.assertEqual(response.status_code, 503)
                    self.assertEqual(response.mimetype, "text/html")
                    self.assertIn(b"schema.sql", response.data)
                    self.assertIn(b".env", response.data)
                    self.assertNotIn(b"clave-super-secreta", response.data)
                    self.assertNotIn("clave-super-secreta", " ".join(logs.output))
                    self.assertNotIn(b"No existen mascotas", response.data)
                    conexion.side_effect = None

    def test_autoescaping(self):
        ataque = "<script>alert(1)</script>"
        self.mascotas.return_value.query_db.return_value = [
            dict(MASCOTA, nombre=ataque)
        ]
        self.usuarios.return_value.query_db.return_value = [
            dict(USUARIO, nombre=ataque, email=ataque)
        ]
        for ruta in ("/", "/usuarios"):
            with self.subTest(ruta=ruta):
                response = self.client.get(ruta)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(ataque.encode(), response.data)
                self.assertIn(b"&lt;script&gt;", response.data)

class ModeloTests(unittest.TestCase):
    def test_get_all_devuelve_objetos_con_campos_exactos(self):
        for modelo, modulo, fila, tabla in (
            (Mascota, "mascota", MASCOTA, "mascotas"),
            (Usuario, "usuario", USUARIO, "usuarios"),
        ):
            with self.subTest(modelo=modelo.__name__):
                with patch(modulo + ".connectToMySQL") as conexion:
                    consulta = conexion.return_value.query_db
                    consulta.return_value = [fila, dict(fila, id=8)]
                    objetos = modelo.get_all()
                    self.assertEqual(len(objetos), 2)
                    self.assertIsInstance(objetos[0], modelo)
                    self.assertEqual(vars(objetos[0]), fila)
                    self.assertEqual(objetos[1].id, 8)
                    conexion.assert_called_once_with()
                    consulta.assert_called_once_with(
                        "SELECT * FROM " + tabla + " ORDER BY id;"
                    )
                    consulta.return_value = []
                    self.assertEqual(modelo.get_all(), [])
                    consulta.return_value = False
                    with self.assertRaises(pymysql.MySQLError):
                        modelo.get_all()

    def test_modelo_sin_desafio(self):
        self.assertFalse(hasattr(Mascota, "get_by_id"))


class ConexionTests(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    @patch("mysqlconnection.pymysql.connect")
    def test_configuracion_por_defecto(self, connect):
        MySQLConnection()
        connect.assert_called_once_with(
            host="127.0.0.1", port=3306, user="skillnest", password="",
            database="primera_flask", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor, autocommit=True,
            connect_timeout=5,
        )

    @patch.dict("os.environ", {
        "MYSQL_HOST": "db.local", "MYSQL_PORT": "3307",
        "MYSQL_USER": "prueba", "MYSQL_PASSWORD": "solo-ficticia",
        "MYSQL_DATABASE": "otra_base",
    }, clear=True)
    @patch("mysqlconnection.pymysql.connect")
    def test_configuracion_entorno_y_argumento(self, connect):
        MySQLConnection()
        argumentos = connect.call_args.kwargs
        self.assertEqual(argumentos["host"], "db.local")
        self.assertEqual(argumentos["port"], 3307)
        self.assertEqual(argumentos["user"], "prueba")
        self.assertEqual(argumentos["password"], "solo-ficticia")
        self.assertEqual(argumentos["database"], "otra_base")
        MySQLConnection("base_explicita")
        self.assertEqual(connect.call_args.kwargs["database"], "base_explicita")

    @patch.dict("os.environ", {"MYSQL_PORT": "invalido"})
    @patch("mysqlconnection.pymysql.connect")
    def test_puerto_invalido(self, connect):
        with self.assertRaises(pymysql.MySQLError):
            MySQLConnection()
        connect.assert_not_called()

    @patch("mysqlconnection.pymysql.connect")
    def test_resultados_y_orden_de_cierre(self, connect):
        for sql, filas, esperado in (
            (" SELECT * FROM mascotas;", [MASCOTA], [MASCOTA]),
            ("SELECT * FROM mascotas;", (), []),
            ("INSERT INTO mascotas (nombre) VALUES (%(nombre)s);", (), 7),
            ("UPDATE mascotas SET nombre = %(nombre)s;", (), None),
            ("DELETE FROM mascotas WHERE nombre = %(nombre)s;", (), None),
        ):
            with self.subTest(sql=sql):
                connection = MagicMock()
                connect.return_value = connection
                cursor = connection.cursor.return_value.__enter__.return_value
                cursor.fetchall.return_value = filas
                cursor.lastrowid = 7
                orden = []
                connection.cursor.return_value.__exit__.side_effect = (
                    lambda *args: orden.append("cursor")
                )
                connection.close.side_effect = lambda: orden.append("conexion")
                datos = {"nombre": "nombre de prueba"}
                self.assertEqual(MySQLConnection().query_db(sql, datos), esperado)
                cursor.execute.assert_called_once_with(sql, datos)
                connection.close.assert_called_once_with()
                self.assertEqual(orden, ["cursor", "conexion"])

    @patch("mysqlconnection.pymysql.connect")
    def test_error_consulta_generico_y_cierre(self, connect):
        connection = connect.return_value
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.execute.side_effect = pymysql.ProgrammingError("dato-secreto")
        with self.assertLogs("mysqlconnection", level="ERROR") as logs:
            resultado = MySQLConnection().query_db(
                "SELECT dato_privado FROM mascotas WHERE id = %(id)s;", {"id": 3}
            )
        self.assertIs(resultado, False)
        connection.cursor.return_value.__exit__.assert_called_once()
        connection.close.assert_called_once_with()
        self.assertNotIn("dato-secreto", " ".join(logs.output))
        self.assertNotIn("SELECT", " ".join(logs.output))
        self.assertNotIn("dato_privado", " ".join(logs.output))

    @patch("mysqlconnection.pymysql.connect")
    def test_error_al_crear_cursor_cierra_conexion(self, connect):
        connect.return_value.cursor.side_effect = pymysql.OperationalError("privado")
        with self.assertLogs("mysqlconnection", level="ERROR"):
            self.assertIs(MySQLConnection().query_db("SELECT 1;"), False)
        connect.return_value.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
