import pymysql
import pymysql.cursors


class ConexionMySQL:
    """Ejecuta consultas contra una base de datos MySQL."""

    def __init__(self, database):
        self.database = database

    def query_db(self, query, data=None):
        try:
            with pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database=self.database,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, data)
                    query_type = query.lstrip().lower()

                    if query_type.startswith("select"):
                        return cursor.fetchall()
                    if query_type.startswith("insert"):
                        return cursor.lastrowid
                    return cursor.rowcount
        except pymysql.MySQLError as error:
            print(f"Database error: {error}")
            return False


def connect_to_mysql(database):
    return ConexionMySQL(database)
