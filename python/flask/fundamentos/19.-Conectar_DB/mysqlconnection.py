import logging
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name('.env'))
logger = logging.getLogger(__name__)


class MySQLConnection:
    """Abre una conexion para una sola consulta."""

    def __init__(self, db=None):
        try:
            port = int(os.environ.get("MYSQL_PORT", "3306"))
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            raise pymysql.MySQLError("Configuracion de MySQL invalida.") from None

        self.connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
            port=port,
            user=os.environ.get("MYSQL_USER", "skillnest"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=db if db is not None else os.environ.get(
                "MYSQL_DATABASE", "primera_flask"
            ),
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


def connectToMySQL(db=None):
    return MySQLConnection(db)
