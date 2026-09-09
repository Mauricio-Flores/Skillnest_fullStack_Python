import pymysql

from mysqlconnection import connectToMySQL


class Mascota:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.tipo = data["tipo"]
        self.color = data["color"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        resultados = connectToMySQL().query_db(
            "SELECT * FROM mascotas ORDER BY id;"
        )
        if resultados is False:
            raise pymysql.MySQLError("No se pudieron consultar las mascotas.")
        return [cls(data) for data in resultados]
