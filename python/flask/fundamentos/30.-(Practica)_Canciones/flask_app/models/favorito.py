from flask_app.config.mysqlconnection import connectToMySQL


class MarcadoFavorito:
    @classmethod
    def exists(cls, data):
        query = """
            SELECT usuario_id, cancion_id
            FROM favoritos
            WHERE usuario_id = %(usuario_id)s AND cancion_id = %(cancion_id)s;
        """
        return bool(connectToMySQL("esquema_canciones").query_db(query, data))

    @classmethod
    def add(cls, data):
        query = """
            INSERT INTO favoritos (usuario_id, cancion_id)
            VALUES (%(usuario_id)s, %(cancion_id)s);
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)
