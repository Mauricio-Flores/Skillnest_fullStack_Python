import logging

import pymysql


logger = logging.getLogger(__name__)


class MySQLConnection:
    """Abre una conexion para una sola consulta."""

    def __init__(self, db):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=5,
        )

    def query_db(self, query, data=None):
        """SELECT: lista; INSERT: id; otros: None; error SQL: False."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                operation = query.strip().split()[0].lower()
                if operation == "select":
                    return list(cursor.fetchall())
                if operation == "insert":
                    return cursor.lastrowid
                return None
        except pymysql.MySQLError:
            logger.error("No se pudo ejecutar la consulta de base de datos.")
            return False
        finally:
            # El cursor debe salir de su contexto antes de cerrar la conexion.
            self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)
