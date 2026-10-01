from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.libro import Libro


class Favorito:
    @staticmethod
    def existe(usuario_id, libro_id):
        filas = connectToMySQL().query_db('''
            SELECT 1 FROM favoritos WHERE usuario_id=%(usuario_id)s AND libro_id=%(libro_id)s;
        ''', {'usuario_id': usuario_id, 'libro_id': libro_id})
        return bool(filas)

    @staticmethod
    def agregar(usuario_id, libro_id):
        # La clave primaria compuesta también impide favoritos duplicados en MySQL.
        return connectToMySQL().query_db('''
            INSERT INTO favoritos (usuario_id, libro_id) VALUES (%(usuario_id)s, %(libro_id)s)
            ON DUPLICATE KEY UPDATE libro_id=VALUES(libro_id);
        ''', {'usuario_id': usuario_id, 'libro_id': libro_id})

    @staticmethod
    def usuarios(libro_id):
        return connectToMySQL().query_db('''
            SELECT usuarios.id, usuarios.nombre, usuarios.apellido FROM usuarios
            JOIN favoritos ON favoritos.usuario_id=usuarios.id
            WHERE favoritos.libro_id=%(id)s ORDER BY usuarios.nombre, usuarios.apellido;
        ''', {'id': libro_id})

    @staticmethod
    def libros(usuario_id):
        return connectToMySQL().query_db(Libro.CONSULTA + '''
            JOIN favoritos ON favoritos.libro_id=libros.id
            WHERE favoritos.usuario_id=%(id)s ORDER BY favoritos.created_at DESC, libros.id DESC;
        ''', {'id': usuario_id})
