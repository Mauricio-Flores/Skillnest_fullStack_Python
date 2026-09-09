import pymysql

from mysqlconnection import connectToMySQL


class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.edad = data["edad"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        resultados = connectToMySQL().query_db(
            "SELECT * FROM usuarios ORDER BY id;"
        )
        if resultados is False:
            raise pymysql.MySQLError("No se pudieron consultar los usuarios.")
        return [cls(data) for data in resultados]
