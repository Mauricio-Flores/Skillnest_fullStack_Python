from flask_app.config.mysqlconnection import connectToMySQL


class Persona:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.favoritos = []

    @classmethod
    def get_all(cls):
        query = """
            SELECT id, nombre, email, contrasena, created_at, updated_at
            FROM usuarios
            ORDER BY id;
        """
        results = connectToMySQL("esquema_canciones").query_db(query)
        return [cls(usuario) for usuario in results] if results is not False else []

    @classmethod
    def get_by_id(cls, identifier):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL("esquema_canciones").query_db(query, {"id": identifier})
        return cls(results[0]) if results else None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, email, contrasena)
            VALUES (%(nombre)s, %(email)s, %(contrasena)s);
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)

    @classmethod
    def get_with_favorites(cls, data):
        query = """
            SELECT
                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at,
                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista
            FROM usuarios
            LEFT JOIN favoritos ON favoritos.usuario_id = usuarios.id
            LEFT JOIN canciones ON favoritos.cancion_id = canciones.id
            WHERE usuarios.id = %(id)s;
        """
        results = connectToMySQL("esquema_canciones").query_db(query, data)

        if not results:
            return None

        persona = cls(
            {
                "id": results[0]["usuario_id"],
                "nombre": results[0]["usuario_nombre"],
                "email": results[0]["usuario_email"],
                "contrasena": results[0]["usuario_contrasena"],
                "created_at": results[0]["usuario_created_at"],
                "updated_at": results[0]["usuario_updated_at"],
            }
        )
        persona.favoritos = [
            {"id": row["cancion_id"], "titulo": row["cancion_titulo"], "artista": row["cancion_artista"]}
            for row in results
            if row["cancion_id"] is not None
        ]
        return persona
