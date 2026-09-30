from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuario import DATABASE_NAME


class FollowLink:
    """Provides persistence operations for follower relationships."""

    @classmethod
    def list_all(cls):
        query = """
            SELECT
                target.id AS usuario_id,
                CONCAT(target.nombre, ' ', target.apellido) AS usuario_nombre,
                follower.id AS seguidor_id,
                CONCAT(follower.nombre, ' ', follower.apellido) AS seguidor_nombre
            FROM seguidores AS relation
            INNER JOIN usuarios AS target ON relation.usuario_id = target.id
            INNER JOIN usuarios AS follower ON relation.seguidor_id = follower.id
            ORDER BY target.nombre, target.apellido, follower.nombre, follower.apellido;
        """
        rows = connectToMySQL(DATABASE_NAME).query_db(query)
        return [] if rows is False else rows

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO seguidores (usuario_id, seguidor_id)
            VALUES (%(usuario_id)s, %(seguidor_id)s);
        """
        return connectToMySQL(DATABASE_NAME).query_db(query, data)
