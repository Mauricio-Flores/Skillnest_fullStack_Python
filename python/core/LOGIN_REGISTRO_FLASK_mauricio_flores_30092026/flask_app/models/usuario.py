import re
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


BASE_DE_DATOS = "inicio_sesion"
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
NOMBRE_REGEX = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+$")


class Usuario:
    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.email = datos["email"]
        self.password = datos["password"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]

    @classmethod
    def guardar(cls, datos):
        consulta = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def obtener_por_email(cls, datos):
        consulta = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, datos):
        consulta = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

        if not resultado:
            return None
        return cls(resultado[0])

    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        nombre = formulario.get("nombre", "").strip()
        apellido = formulario.get("apellido", "").strip()
        email = formulario.get("email", "").strip().lower()
        password = formulario.get("password", "")
        confirmar_password = formulario.get("confirmar_password", "")

        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.match(nombre):
            flash("El nombre solo puede contener letras.", "registro")
            es_valido = False

        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.match(apellido):
            flash("El apellido solo puede contener letras.", "registro")
            es_valido = False

        if not EMAIL_REGEX.match(email):
            flash("Ingresa un correo electrónico válido.", "registro")
            es_valido = False
        elif Usuario.obtener_por_email({"email": email}):
            flash("El correo electrónico ya está registrado.", "registro")
            es_valido = False

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
        else:
            if not re.search(r"[A-Z]", password):
                flash("La contraseña debe incluir al menos una mayúscula.", "registro")
                es_valido = False
            if not re.search(r"[0-9]", password):
                flash("La contraseña debe incluir al menos un número.", "registro")
                es_valido = False

        if password != confirmar_password:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido
