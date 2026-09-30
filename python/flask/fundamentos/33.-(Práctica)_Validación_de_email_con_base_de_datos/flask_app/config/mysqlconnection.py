import os

import pymysql.cursors


class DatabaseConnector:
    """Ejecuta consultas contra una base de datos MySQL."""

    def __init__(self, database_name):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "localhost"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", ""),
                database=database_name,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        except pymysql.MySQLError as error:
            print(f"No se pudo conectar a la base de datos: {error}")

    def execute(self, query, values=None):
        """Devuelve filas, el id insertado o las filas afectadas."""
        if self.connection is None:
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                statement_type = query.lstrip().lower()

                if statement_type.startswith("select"):
                    return cursor.fetchall()
                if statement_type.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
        except pymysql.MySQLError as error:
            print(f"Error de base de datos: {error}")
            return False
        finally:
            if self.connection is not None:
                self.connection.close()


def open_mysql(database_name):
    """Crea un conector para la base de datos indicada."""
    return DatabaseConnector(database_name)
