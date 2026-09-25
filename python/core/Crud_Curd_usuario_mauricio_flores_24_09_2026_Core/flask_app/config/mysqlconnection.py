import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                statement = query.strip().lower()

                if statement.startswith("select"):
                    return cursor.fetchall()

                if statement.startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount
            except Exception as error:
                print("Error en MySQL:", error)
                return False
            finally:
                self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)
