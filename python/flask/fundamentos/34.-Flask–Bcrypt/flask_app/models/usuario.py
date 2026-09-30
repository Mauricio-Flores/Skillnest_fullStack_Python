"""Account model and registration validation."""

import os
import re

from flask import flash

from flask_app.config.mysqlconnection import connect_to_mysql

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
DATABASE_NAME = os.getenv("DB_NAME", "esquema_loginreg")


class Account:
    """Represent a row from the usuarios table."""

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_registration(data):
        is_valid = True
        fields = (
            ("nombre", "nombre", "Nombre", 2),
            ("apellido", "apellido", "Apellido", 2),
        )

        for key, category, label, minimum_length in fields:
            if not data[key]:
                flash(f"El {label.lower()} es obligatorio.", category)
                is_valid = False
            elif len(data[key]) < minimum_length:
                flash(
                    f"El {label.lower()} debe tener al menos {minimum_length} caracteres.",
                    category,
                )
                is_valid = False

        if not data["email"]:
            flash("El email es obligatorio.", "email")
            is_valid = False
        elif not EMAIL_PATTERN.fullmatch(data["email"]):
            flash("El email no tiene un formato válido.", "email")
            is_valid = False

        if not data["password"]:
            flash("La contraseña es obligatoria.", "password")
            is_valid = False
        elif len(data["password"]) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "password")
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connect_to_mysql(DATABASE_NAME).execute(query, data)

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connect_to_mysql(DATABASE_NAME).execute(query, data)
        return cls(results[0]) if len(results) == 1 else None

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connect_to_mysql(DATABASE_NAME).execute(query, data)
        return cls(results[0]) if len(results) == 1 else None

    @classmethod
    def email_exists(cls, data):
        query = "SELECT id FROM usuarios WHERE email = %(email)s;"
        return bool(connect_to_mysql(DATABASE_NAME).execute(query, data))
