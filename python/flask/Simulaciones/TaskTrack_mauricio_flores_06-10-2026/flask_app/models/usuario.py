import re

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
DB = "tasktrack"


class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s LIMIT 1;"
        resultado = connectToMySQL(DB).query_db(query, {"email": email})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def obtener_por_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s LIMIT 1;"
        resultado = connectToMySQL(DB).query_db(query, {"id": usuario_id})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE usuarios
            SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validar_registro(formulario):
        valido = True
        nombre = formulario.get("nombre", "").strip()
        apellido = formulario.get("apellido", "").strip()
        email = formulario.get("email", "").strip().lower()
        password = formulario.get("password", "")

        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            valido = False
        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            valido = False
        if not EMAIL_REGEX.match(email):
            flash("Ingresa un correo electrónico válido.", "registro")
            valido = False
        elif Usuario.obtener_por_email(email):
            flash("El correo electrónico ya está registrado.", "registro")
            valido = False
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            valido = False
        if password != formulario.get("confirmar_password", ""):
            flash("Las contraseñas no coinciden.", "registro")
            valido = False
        return valido

    @staticmethod
    def validar_perfil(formulario, usuario_id):
        valido = True
        nombre = formulario.get("nombre", "").strip()
        apellido = formulario.get("apellido", "").strip()
        email = formulario.get("email", "").strip().lower()

        if len(nombre) < 2 or len(apellido) < 2:
            flash("Nombre y apellido deben tener al menos 2 caracteres.", "perfil")
            valido = False
        if not EMAIL_REGEX.match(email):
            flash("Ingresa un correo electrónico válido.", "perfil")
            valido = False
        else:
            existente = Usuario.obtener_por_email(email)
            if existente and existente.id != usuario_id:
                flash("Ese correo ya pertenece a otra cuenta.", "perfil")
                valido = False
        return valido
