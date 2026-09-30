import os

import pymysql.cursors


class DatabaseSession:
    """Executes parameterized queries against the configured MySQL database."""

    def __init__(self, database):
        self.database = database

    def query_db(self, query, data=None):
        connection = None
        try:
            connection = pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "localhost"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", ""),
                database=self.database,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                statement = query.lstrip().lower()
                if statement.startswith("select"):
                    return cursor.fetchall()
                if statement.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
        except pymysql.MySQLError as error:
            print(f"Database error: {error}")
            return False
        finally:
            if connection is not None:
                connection.close()


def connectToMySQL(database):
    return DatabaseSession(database)
