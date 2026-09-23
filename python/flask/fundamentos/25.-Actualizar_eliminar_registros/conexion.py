import pymysql.cursors

class Conexion:

    def __init__(self, base):
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database=base,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def ejecutar(self, sql, datos=None):
        with self.db.cursor() as cursor:
            try:
                cursor.execute(sql, datos)

                if sql.strip().lower().startswith("select"):
                    return cursor.fetchall()

                return cursor.lastrowid

            except Exception as error:
                print(error)
                return False

            finally:
                self.db.close()

def conectar(base):
    return Conexion(base)
