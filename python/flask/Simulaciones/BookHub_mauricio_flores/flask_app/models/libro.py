from datetime import date
from flask_app.config.mysqlconnection import connectToMySQL


class Libro:
    GENEROS = ('Novela', 'Fábula', 'Ciencia Ficción', 'Romance', 'Desarrollo Personal',
               'Fantasía', 'Misterio', 'Historia', 'Poesía', 'Otro')

    CONSULTA = '''
        SELECT libros.*, usuarios.nombre AS nombre_usuario,
               usuarios.apellido AS apellido_usuario,
               (SELECT COUNT(*) FROM favoritos WHERE favoritos.libro_id = libros.id) AS total_favoritos
        FROM libros
        JOIN usuarios ON usuarios.id = libros.usuario_id
    '''

    @staticmethod
    def propios(usuario_id):
        return connectToMySQL().query_db(Libro.CONSULTA +
            ' WHERE libros.usuario_id = %(id)s ORDER BY libros.created_at DESC, libros.id DESC;', {'id': usuario_id})

    @staticmethod
    def comunidad(usuario_id):
        return connectToMySQL().query_db(Libro.CONSULTA +
            ' WHERE libros.usuario_id <> %(id)s ORDER BY libros.created_at DESC, libros.id DESC;', {'id': usuario_id})

    @staticmethod
    def buscar(libro_id):
        filas = connectToMySQL().query_db(Libro.CONSULTA + ' WHERE libros.id = %(id)s;', {'id': libro_id})
        return filas[0] if filas else None

    @staticmethod
    def crear(datos):
        return connectToMySQL().query_db('''
            INSERT INTO libros (titulo, autor, genero, fecha, descripcion, usuario_id)
            VALUES (%(titulo)s, %(autor)s, %(genero)s, %(fecha)s, %(descripcion)s, %(usuario_id)s);
        ''', datos)

    @staticmethod
    def actualizar(datos):
        return connectToMySQL().query_db('''
            UPDATE libros SET titulo=%(titulo)s, autor=%(autor)s, genero=%(genero)s,
                fecha=%(fecha)s, descripcion=%(descripcion)s
            WHERE id=%(id)s AND usuario_id=%(usuario_id)s;
        ''', datos)

    @staticmethod
    def eliminar(libro_id, usuario_id):
        return connectToMySQL().query_db(
            'DELETE FROM libros WHERE id=%(id)s AND usuario_id=%(usuario_id)s;',
            {'id': libro_id, 'usuario_id': usuario_id})

    @staticmethod
    def validar(datos):
        errores = []
        if not 2 <= len(datos.get('titulo', '')) <= 150:
            errores.append('El título debe tener entre 2 y 150 caracteres.')
        if not 2 <= len(datos.get('autor', '')) <= 100:
            errores.append('El autor debe tener entre 2 y 100 caracteres.')
        if datos.get('genero') not in Libro.GENEROS:
            errores.append('Selecciona un género válido.')
        try:
            fecha = date.fromisoformat(datos.get('fecha', ''))
            if fecha < date.today():
                errores.append('La fecha de publicación no puede ser pasada.')
        except ValueError:
            errores.append('Ingresa una fecha de publicación válida.')
        if not 10 <= len(datos.get('descripcion', '')) <= 5000:
            errores.append('La descripción debe tener entre 10 y 5000 caracteres.')
        return errores
