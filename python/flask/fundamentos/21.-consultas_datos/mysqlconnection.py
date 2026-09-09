import logging
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))
logger = logging.getLogger(__name__)


class MySQLConnection:
    def __init__(self, db=None):
        self.connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
            port=int(os.environ.get("MYSQL_PORT", "3306")),
            user=os.environ.get("MYSQL_USER", "skillnest"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=db if db is not None else os.environ.get("MYSQL_DATABASE", "primera_flask"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=5,
        )

    def query_db(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                if query.strip().lower().startswith("select"):
                    return list(cursor.fetchall())
                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid
                return None
        except pymysql.MySQLError:
            logger.error("No se pudo ejecutar la consulta a la base de datos.")
            return False
        finally:
            self.connection.close()


def connectToMySQL(db=None):
    return MySQLConnection(db)
