from flask_app.config.mysqlconnection import connectToMySQL


class Especialidad:
    def __init__(self, data):
        self.id = data["id"]
        self.tortilla = data["tortilla"]
        self.guiso = data["guiso"]
        self.salsa = data["salsa"]
        self.restaurante_id = data["restaurante_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO tacos (tortilla, guiso, salsa, restaurante_id)
            VALUES (%(tortilla)s, %(guiso)s, %(salsa)s, %(restaurante_id)s);
        """
        return connectToMySQL("esquema_tacos").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
            SELECT id, tortilla, guiso, salsa, restaurante_id, created_at, updated_at
            FROM tacos
            ORDER BY id;
        """
        results = connectToMySQL("esquema_tacos").query_db(query)
        return [cls(taco) for taco in results] if results is not False else []
