from flask_app.config.mysqlconnection import connectToMySQL


class Pista:
    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.artista = data["artista"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuarios = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM canciones ORDER BY id;"
        results = connectToMySQL("esquema_canciones").query_db(query)
        return [cls(cancion) for cancion in results] if results is not False else []

    @classmethod
    def get_by_id(cls, identifier):
        query = "SELECT * FROM canciones WHERE id = %(id)s;"
        results = connectToMySQL("esquema_canciones").query_db(query, {"id": identifier})
        return cls(results[0]) if results else None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO canciones (titulo, artista)
            VALUES (%(titulo)s, %(artista)s);
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)

    @classmethod
    def get_with_users(cls, data):
        query = """
            SELECT
                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista,
                canciones.created_at AS cancion_created_at,
                canciones.updated_at AS cancion_updated_at,
                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre
            FROM canciones
            LEFT JOIN favoritos ON favoritos.cancion_id = canciones.id
            LEFT JOIN usuarios ON favoritos.usuario_id = usuarios.id
            WHERE canciones.id = %(id)s;
        """
        results = connectToMySQL("esquema_canciones").query_db(query, data)

        if not results:
            return None

        pista = cls(
            {
                "id": results[0]["cancion_id"],
                "titulo": results[0]["cancion_titulo"],
                "artista": results[0]["cancion_artista"],
                "created_at": results[0]["cancion_created_at"],
                "updated_at": results[0]["cancion_updated_at"],
            }
        )
        pista.usuarios = [
            {"id": row["usuario_id"], "nombre": row["usuario_nombre"]}
            for row in results
            if row["usuario_id"] is not None
        ]
        return pista
