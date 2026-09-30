import re

from flask import flash

from flask_app.config.mysqlconnection import open_mysql

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
DATABASE_NAME = "esquema_usuarios"


class RegistroUsuario:
    """Representa y persiste un registro de la tabla usuarios."""

    def __init__(self, values):
        self.id = values["id"]
        self.nombre = values["nombre"]
        self.apellido = values["apellido"]
        self.email = values["email"]
        self.created_at = values["created_at"]
        self.updated_at = values["updated_at"]

    @staticmethod
    def validar_datos(values):
        """Valida los datos recibidos antes de intentar insertarlos."""
        is_valid = True

        if not values["nombre"]:
            flash("El nombre es obligatorio.", "error")
            is_valid = False

        if not values["apellido"]:
            flash("El apellido es obligatorio.", "error")
            is_valid = False

        if not values["email"]:
            flash("El email es obligatorio.", "error")
            is_valid = False
        elif not EMAIL_PATTERN.match(values["email"]):
            flash("El email no tiene un formato valido.", "error")
            is_valid = False

        return is_valid

    @classmethod
    def obtener_todos(cls):
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            ORDER BY id DESC;
        """
        rows = open_mysql(DATABASE_NAME).execute(query)

        if rows is False:
            return []
        return [cls(row) for row in rows]

    @classmethod
    def crear(cls, values):
        query = """
            INSERT INTO usuarios (nombre, apellido, email)
            VALUES (%(nombre)s, %(apellido)s, %(email)s);
        """
        return open_mysql(DATABASE_NAME).execute(query, values)
