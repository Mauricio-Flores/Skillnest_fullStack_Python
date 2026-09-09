import os
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import quote

import pymysql

from app import app
from mascota import Mascota
from mysqlconnection import MySQLConnection


ROW = {
    "id": 3, "nombre": "Luna", "tipo": "Perro", "color": "Blanco",
    "created_at": "2026-01-02 10:00:00", "updated_at": "2026-02-03 11:00:00",
}


class ModelTests(unittest.TestCase):
    def setUp(self):
        patcher = patch("mascota.connectToMySQL")
        self.connect = patcher.start()
        self.addCleanup(patcher.stop)
        self.query = self.connect.return_value.query_db
        self.query.return_value = [ROW]

    def test_all_attributes_and_list_objects(self):
        mascotas = Mascota.get_all()
        self.assertEqual(len(mascotas), 1)
        self.assertIsInstance(mascotas[0], Mascota)
        self.assertEqual(vars(mascotas[0]), ROW)
        self.query.assert_called_once_with("SELECT * FROM mascotas ORDER BY id;")

    def test_id_parameter(self):
        self.assertEqual(Mascota.get_by_id(3).id, 3)
        query, data = self.query.call_args.args
        self.assertIn("WHERE id = %(id_mascota)s", query)
        self.assertEqual(data, {"id_mascota": 3})

    def test_names_are_data(self):
        for nombre in ("O'Brien", "' OR 1=1 --"):
            with self.subTest(nombre=nombre):
                self.assertIsInstance(Mascota.get_by_name(nombre), Mascota)
                query, data = self.query.call_args.args
                self.assertIn("WHERE nombre = %(nombre_mascota)s", query)
                self.assertNotIn(nombre, query)
                self.assertEqual(data, {"nombre_mascota": nombre})

    def test_modelo_sin_desafio(self):
        self.assertFalse(hasattr(Mascota, "get_by_tipo"))

    def test_empty_results_and_database_failures_are_distinct(self):
        cases = [(Mascota.get_all, (), []), (Mascota.get_by_id, (3,), None),
                 (Mascota.get_by_name, ("Luna",), None)]
        for method, args, empty in cases:
            with self.subTest(method=method.__name__):
                self.query.return_value = []
                self.assertEqual(method(*args), empty)
                self.query.return_value = False
                with self.assertRaises(pymysql.MySQLError):
                    method(*args)


class RouteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        patcher = patch("mascota.connectToMySQL")
        self.connect = patcher.start()
        self.addCleanup(patcher.stop)
        self.query = self.connect.return_value.query_db
        self.query.return_value = [ROW]

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/mascota/3"', response.text)

    def test_detail_and_name_show_every_attribute(self):
        for path in ("/mascota/3", "/mascota/nombre/Luna"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                for value in ROW.values():
                    self.assertIn(str(value), response.text)

    def test_missing_and_invalid_routes(self):
        self.query.return_value = []
        for path in ("/mascota/999999", "/mascota/nombre/NoExiste",
                     "/mascota/abc", "/no-existe"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                self.assertIn("no encontrada", response.text)

    def test_rutas_eliminadas_no_consultan(self):
        for path in ("/mascotas/tipo/Perro", "/mascotas/tipo/Perro/Gato",
                     "/mascotas/tipo/NoExiste"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
        self.connect.assert_not_called()

    def test_empty_list(self):
        self.query.return_value = []
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("No existen mascotas registradas", response.text)

    def test_escaped_html(self):
        payload = '<script>alert("x")</script>'
        self.query.return_value = [dict(ROW, nombre=payload, tipo=payload, color=payload)]
        for path in ("/", "/mascota/3", "/mascota/nombre/Luna"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(payload, response.text)
            self.assertIn("&lt;script&gt;", response.text)

    def test_apostrophe_route_preserves_parameter(self):
        self.client.get("/mascota/nombre/" + quote("O'Brien", safe=""))
        self.assertEqual(self.query.call_args.args[1], {"nombre_mascota": "O'Brien"})

    def test_slashes_in_name(self):
        self.query.return_value = [dict(ROW, nombre="Luna/Sol")]
        for path, parameter, value in (
            ("/mascota/nombre/Luna/Sol", "nombre_mascota", "Luna/Sol"),
        ):
            with self.subTest(path=path):
                self.query.reset_mock()
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(value, response.text)
                self.query.assert_called_once()
                self.assertEqual(self.query.call_args.args[1], {parameter: value})

    def test_database_failure_returns_generic_503(self):
        for connection_error in (False, True):
            self.query.return_value = False
            self.connect.side_effect = pymysql.MySQLError("secret SQL password") if connection_error else None
            for path in ("/", "/mascota/3", "/mascota/nombre/Luna"):
                with self.subTest(path=path, connection_error=connection_error):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 503)
                    self.assertEqual(response.mimetype, "text/html")
                    self.assertIn(".env", response.text)
                    self.assertNotIn("secret SQL password", response.text)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        patcher = patch("mysqlconnection.pymysql.connect")
        self.connect = patcher.start()
        self.addCleanup(patcher.stop)
        self.connection = self.connect.return_value
        self.context = self.connection.cursor.return_value
        self.cursor = self.context.__enter__.return_value

    @patch.dict(os.environ, {}, clear=True)
    def test_default_configuration(self):
        MySQLConnection()
        self.connect.assert_called_once_with(
            host="127.0.0.1", port=3306, user="skillnest", password="",
            database="primera_flask", charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor, autocommit=True, connect_timeout=5,
        )

    @patch.dict(os.environ, {"MYSQL_HOST": "db.local", "MYSQL_PORT": "3307",
                           "MYSQL_USER": "lector", "MYSQL_PASSWORD": "test-only",
                           "MYSQL_DATABASE": "otra"}, clear=True)
    def test_environment_and_explicit_database(self):
        MySQLConnection()
        options = self.connect.call_args.kwargs
        self.assertEqual((options["host"], options["port"], options["user"],
                          options["password"], options["database"]),
                         ("db.local", 3307, "lector", "test-only", "otra"))
        MySQLConnection("explicita")
        self.assertEqual(self.connect.call_args.kwargs["database"], "explicita")

    def test_query_return_contract_and_close_order(self):
        self.cursor.fetchall.return_value = (ROW,)
        self.cursor.lastrowid = 9
        cases = [(" SELECT * FROM mascotas", [ROW]), ("SELECT 1 WHERE FALSE", []),
                 ("INSERT INTO mascotas (nombre) VALUES (%(nombre)s)", 9),
                 ("UPDATE mascotas SET nombre = %(nombre)s", None)]
        for query, expected in cases:
            with self.subTest(query=query):
                self.connection.reset_mock()
                self.cursor.fetchall.return_value = () if expected == [] else (ROW,)
                events = MagicMock()
                events.attach_mock(self.context.__exit__, "exit")
                events.attach_mock(self.connection.close, "close")
                data = {"nombre": "O'Brien"}
                self.assertEqual(MySQLConnection().query_db(query, data), expected)
                self.cursor.execute.assert_called_with(query, data)
                self.assertEqual([call[0] for call in events.mock_calls], ["exit", "close"])
                self.connection.close.assert_called_once_with()

    def test_query_error_is_false_and_logs_no_sensitive_details(self):
        self.cursor.execute.side_effect = pymysql.MySQLError("secret SQL value")
        with self.assertLogs("mysqlconnection", level="ERROR") as logs:
            self.assertIs(MySQLConnection().query_db("SELECT secret", {"key": "private"}), False)
        self.assertNotIn("secret", " ".join(logs.output))
        self.assertNotIn("private", " ".join(logs.output))
        self.context.__exit__.assert_called_once()
        self.connection.close.assert_called_once_with()

    def test_cursor_creation_failure_closes_connection(self):
        self.connection.cursor.side_effect = pymysql.MySQLError("private")
        with self.assertLogs("mysqlconnection", level="ERROR"):
            self.assertIs(MySQLConnection().query_db("SELECT 1"), False)
        self.connection.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
