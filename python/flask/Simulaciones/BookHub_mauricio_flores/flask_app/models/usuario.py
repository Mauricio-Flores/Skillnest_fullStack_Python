import re
from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.password = datos['password']

    @classmethod
    def buscar_por_email(cls, email):
        filas = connectToMySQL().query_db('SELECT * FROM usuarios WHERE email = %(email)s;', {'email': email})
        return cls(filas[0]) if filas else None

    @classmethod
    def buscar_por_id(cls, usuario_id):
        filas = connectToMySQL().query_db('SELECT * FROM usuarios WHERE id = %(id)s;', {'id': usuario_id})
        return cls(filas[0]) if filas else None

    @staticmethod
    def crear(datos):
        return connectToMySQL().query_db('''
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        ''', datos)

    @staticmethod
    def validar(datos):
        errores = []
        for campo in ['nombre', 'apellido']:
            if not 2 <= len(datos.get(campo, '')) <= 45:
                errores.append(f'El {campo} debe tener entre 2 y 45 caracteres.')
        email = datos.get('email', '')
        if len(email) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            errores.append('Ingresa un correo electrónico válido.')
        elif Usuario.buscar_por_email(email):
            errores.append('Este correo electrónico ya está registrado.')
        password = datos.get('password', '')
        if len(password) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres.')
        if len(password.encode('utf-8')) > 72:
            errores.append('La contraseña no puede superar 72 bytes.')
        if password != datos.get('confirmar', ''):
            errores.append('Las contraseñas deben ser iguales.')
        return errores
