import os

import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            db=os.getenv("DB_NAME", db),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        data = data or {}
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                if query.lstrip().lower().startswith("insert"):
                    return cursor.lastrowid
                if query.lstrip().lower().startswith("select"):
                    return cursor.fetchall()
                return cursor.rowcount
        except pymysql.MySQLError as error:
            print(f"Error de MySQL: {error}")
            return False
        finally:
            self.connection.close()


def connectToMySQL(db=None):
    return MySQLConnection(db or os.getenv("DB_NAME", "tasktrack"))
