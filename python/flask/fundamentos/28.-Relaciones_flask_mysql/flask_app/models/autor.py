# ==========================================================
# MODELO AUTOR
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.libro import Libro


class Autor:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Autor.
        """
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # Lista donde almacenaremos los objetos Libro relacionados.
        self.libros = []

    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo autor.
        """
        query = """
            INSERT INTO autores
            (
                nombre
            )
            VALUES
            (
                %(nombre)s
            );
        """

        return connectToMySQL("esquema_libros").query_db(query, datos)

    # ======================================================
    # READ
    # OBTENER TODOS LOS AUTORES
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los autores.
        """
        query = """
            SELECT
                id,
                nombre,
                created_at,
                updated_at
            FROM autores
            ORDER BY id;
        """

        resultados = connectToMySQL("esquema_libros").query_db(query)

        autores = []

        for autor in resultados:
            autores.append(cls(autor))

        return autores

    # ======================================================
    # READ
    # AUTOR + LIBROS
    # ======================================================

    @classmethod
    def get_autor_y_libros(cls, datos):
        """
        Recupera un autor junto con
        todos los libros relacionados.
        """
        query = """
            SELECT
                autores.id AS autor_id,
                autores.nombre AS autor_nombre,
                autores.created_at AS autor_created_at,
                autores.updated_at AS autor_updated_at,
                libros.id AS libro_id,
                libros.titulo AS libro_titulo,
                libros.genero AS libro_genero,
                libros.editorial AS libro_editorial,
                libros.autor_id AS libro_autor_id,
                libros.created_at AS libro_created_at,
                libros.updated_at AS libro_updated_at
            FROM autores
            LEFT JOIN libros
                ON libros.autor_id = autores.id
            WHERE autores.id = %(id)s;
        """

        resultados = connectToMySQL("esquema_libros").query_db(query, datos)

        # Si no existe el autor.
        if not resultados:
            return None

        # Crear objeto Autor.
        autor_data = {
            "id": resultados[0]["autor_id"],
            "nombre": resultados[0]["autor_nombre"],
            "created_at": resultados[0]["autor_created_at"],
            "updated_at": resultados[0]["autor_updated_at"]
        }

        autor = cls(autor_data)

        # Recorrer los resultados del JOIN.
        for fila_en_db in resultados:

            # Como utilizamos LEFT JOIN, el autor puede no tener
            # libros. En ese caso libro_id será None.
            if fila_en_db["libro_id"] is not None:

                datos_libro = {
                    "id": fila_en_db["libro_id"],
                    "titulo": fila_en_db["libro_titulo"],
                    "genero": fila_en_db["libro_genero"],
                    "editorial": fila_en_db["libro_editorial"],
                    "autor_id": fila_en_db["libro_autor_id"],
                    "created_at": fila_en_db["libro_created_at"],
                    "updated_at": fila_en_db["libro_updated_at"]
                }

                # Convertimos el diccionario en un objeto Libro
                # y lo agregamos al autor.
                autor.libros.append(Libro(datos_libro))

        return autor
