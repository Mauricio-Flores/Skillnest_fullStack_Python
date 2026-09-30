from flask_app.config.mysqlconnection import connectToMySQL

DATABASE_NAME = "esquema_seguidores"


class MemberRecord:
    """Represents one row from the usuarios table."""

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def list_all(cls):
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            ORDER BY nombre, apellido;
        """
        rows = connectToMySQL(DATABASE_NAME).query_db(query)
        if rows is False:
            return []
        return [cls(row) for row in rows]

    @classmethod
    def find(cls, member_id):
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            WHERE id = %(id)s;
        """
        rows = connectToMySQL(DATABASE_NAME).query_db(query, {"id": member_id})
        if not rows:
            return None
        return cls(rows[0])

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email)
            VALUES (%(nombre)s, %(apellido)s, %(email)s);
        """
        return connectToMySQL(DATABASE_NAME).query_db(query, data)
