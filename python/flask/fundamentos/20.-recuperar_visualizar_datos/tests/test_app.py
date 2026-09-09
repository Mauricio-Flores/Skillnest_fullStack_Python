import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pymysql

from app import app
from mascota import Mascota
from mysqlconnection import MySQLConnection


def fila(**cambios):
    data = {
        "id": 42,
        "nombre": "Firulais",
        "tipo": "Perro",
        "color": "Caf\u00e9",
        "created_at": datetime(2026, 9, 7, 10, 20, 30),
        "updated_at": datetime(2026, 9, 8, 11, 22, 33),
    }
    data.update(cambios)
    return data


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.patcher = patch("mascota.connectToMySQL")
        self.connect = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.query = self.connect.return_value.query_db

    def test_list_id_dates(self):
        self.query.return_value = [fila(), fila(id=43, nombre="Michi", tipo="Gato")]
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for text in ("Firulais", "Michi", "Caf\u00e9", "<dd>42</dd>",
                     "2026-09-07 10:20:30", "2026-09-08 11:22:33",
                     'datetime="2026-09-07T10:20:30"'):
            self.assertIn(text, html)

    def test_empty_views(self):
        self.query.return_value = []
        for route, message in (("/", "No existen mascotas registradas."),):
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertIn(message, response.get_data(as_text=True))

    def test_ruta_eliminada_no_consulta(self):
        self.assertEqual(self.client.get("/mascotas/perros").status_code, 404)
        self.connect.assert_not_called()

    def test_modelo_sin_desafio(self):
        self.assertFalse(hasattr(Mascota, "get_by_tipo"))

    def test_autoescaping_and_null_dates(self):
        self.query.return_value = [fila(nombre="<script>alert(1)</script>",
                                       created_at=None, updated_at=None)]
        html = self.client.get("/").get_data(as_text=True)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertEqual(html.count("Sin fecha"), 2)

    def test_query_failure_is_503_not_empty(self):
        self.query.return_value = False
        for route in ("/",):
            with self.subTest(route=route), self.assertLogs(app.logger, level="ERROR"):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.mimetype, "text/html")
                html = response.get_data(as_text=True)
                self.assertIn("schema.sql", html)
                self.assertIn(".env", html)
                self.assertNotIn("No existen", html)

    def test_connection_failure_does_not_expose_secret(self):
        self.connect.side_effect = pymysql.MySQLError("password=super-secreto SELECT *")
        for route in ("/",):
            with self.subTest(route=route), self.assertLogs(app.logger, level="ERROR") as logs:
                response = self.client.get(route)
            self.assertEqual(response.status_code, 503)
            self.assertNotIn("super-secreto", response.get_data(as_text=True))
            self.assertNotIn("super-secreto", " ".join(logs.output))

    def test_model_conversion(self):
        data = fila()
        self.query.return_value = [data]
        mascotas = Mascota.get_all()
        self.query.assert_called_once_with("SELECT * FROM mascotas ORDER BY id;")
        self.assertIsInstance(mascotas[0], Mascota)
        self.assertEqual(vars(mascotas[0]), data)

    def test_models_distinguish_empty_from_false(self):
        for method, args in ((Mascota.get_all, ()),):
            with self.subTest(method=method.__name__):
                self.query.return_value = []
                self.assertEqual(method(*args), [])
                self.query.return_value = False
                with self.assertRaises(pymysql.MySQLError):
                    method(*args)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("mysqlconnection.pymysql.connect")
        self.connect = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.connection = self.connect.return_value
        self.context = self.connection.cursor.return_value
        self.cursor = self.context.__enter__.return_value

    def test_default_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            MySQLConnection()
        self.connect.assert_called_once_with(
            host="127.0.0.1", port=3306, user="skillnest", password="",
            database="primera_flask", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor, autocommit=True, connect_timeout=5,
        )

    def test_environment_and_database_argument(self):
        with patch.dict(os.environ, {"MYSQL_HOST": "db.local", "MYSQL_PORT": "3307",
                                    "MYSQL_USER": "lector", "MYSQL_PASSWORD": "prueba",
                                    "MYSQL_DATABASE": "otra"}, clear=True):
            MySQLConnection()
            self.assertEqual(self.connect.call_args.kwargs["database"], "otra")
            MySQLConnection("explicita")
        config = self.connect.call_args.kwargs
        self.assertEqual(config["database"], "explicita")
        self.assertEqual(config["host"], "db.local")
        self.assertEqual(config["port"], 3307)
        self.assertEqual(config["user"], "lector")
        self.assertEqual(config["password"], "prueba")

    def test_return_values_parameters_and_close_order(self):
        self.cursor.fetchall.return_value = (fila(),)
        self.cursor.lastrowid = 51
        events = MagicMock()
        events.attach_mock(self.context.__exit__, "cursor_exit")
        events.attach_mock(self.connection.close, "close")
        for sql, params, expected in (
            (" SELECT * FROM mascotas WHERE tipo = %(tipo)s;", {"tipo": "Perro"}, [fila()]),
            ("SELECT * FROM mascotas;", None, [fila()]),
            ("INSERT INTO mascotas (nombre) VALUES (%(nombre)s);", {"nombre": "Luna"}, 51),
            ("UPDATE mascotas SET color = %(color)s;", {"color": "Blanco"}, None),
            ("DELETE FROM mascotas WHERE id = %(id)s;", {"id": 99}, None),
        ):
            with self.subTest(sql=sql):
                events.reset_mock()
                result = MySQLConnection().query_db(sql, params)
                self.assertEqual(result, expected)
                self.cursor.execute.assert_called_with(sql, params)
                self.assertEqual([call[0] for call in events.mock_calls], ["cursor_exit", "close"])

    def test_query_error_logs_generic_message_and_closes(self):
        self.cursor.execute.side_effect = pymysql.MySQLError("secret-value SQL")
        with self.assertLogs("mysqlconnection", level="ERROR") as logs:
            result = MySQLConnection().query_db("SELECT secret-value", {"key": "secret-value"})
        self.assertIs(result, False)
        self.assertNotIn("secret-value", " ".join(logs.output))
        self.assertNotIn("SQL", " ".join(logs.output))
        self.context.__exit__.assert_called_once()
        self.connection.close.assert_called_once()

    def test_cursor_open_error_also_closes(self):
        self.connection.cursor.side_effect = pymysql.MySQLError("private")
        with self.assertLogs("mysqlconnection", level="ERROR"):
            self.assertIs(MySQLConnection().query_db("SELECT 1"), False)
        self.connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
