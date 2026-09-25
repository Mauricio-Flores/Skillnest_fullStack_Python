import logging

import pymysql.cursors


logger = logging.getLogger(__name__)


class MySQLConnection:
    """Abre una conexion para una consulta y la cierra al terminar."""

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
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                operation = query.strip().lower()
                if operation.startswith("select"):
                    return list(cursor.fetchall())
                if operation.startswith("insert"):
                    return cursor.lastrowid
                return None
        except pymysql.MySQLError:
            logger.error("No se pudo ejecutar la consulta a la base de datos.")
            return False
        finally:
            self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)
