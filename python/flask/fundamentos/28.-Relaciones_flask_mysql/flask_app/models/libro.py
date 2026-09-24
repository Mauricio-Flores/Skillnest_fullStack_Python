# ==========================================================
# MODELO LIBRO
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL


class Libro:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Libro.
        """
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.genero = data["genero"]
        self.editorial = data["editorial"]
        self.autor_id = data["autor_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo libro.

        Necesita también el ID del autor
        al que pertenece.
        """
        query = """
            INSERT INTO libros
            (
                titulo,
                genero,
                editorial,
                autor_id
            )
            VALUES
            (
                %(titulo)s,
                %(genero)s,
                %(editorial)s,
                %(autor_id)s
            );
        """

        return connectToMySQL("esquema_libros").query_db(query, datos)

    # ======================================================
    # READ
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los libros.
        """
        query = """
            SELECT
                id,
                titulo,
                genero,
                editorial,
                autor_id,
                created_at,
                updated_at
            FROM libros
            ORDER BY id;
        """

        resultados = connectToMySQL("esquema_libros").query_db(query)

        libros = []

        for libro in resultados:
            libros.append(cls(libro))

        return libros
