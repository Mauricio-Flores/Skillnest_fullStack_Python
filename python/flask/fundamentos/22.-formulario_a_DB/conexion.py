import pymysql.cursors


class ConexionMySQL:

    def __init__(self, base):
        self.conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database=base,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def ejecutar(self, consulta, datos=None):

        with self.conexion.cursor() as cursor:

            try:
                cursor.execute(consulta, datos)

                if consulta.strip().lower().startswith("select"):
                    return cursor.fetchall()

                if consulta.strip().lower().startswith("insert"):
                    return cursor.lastrowid

                return None

            except Exception as error:
                print(error)
                return False

            finally:
                self.conexion.close()


def conectar(base):
    return ConexionMySQL(base)