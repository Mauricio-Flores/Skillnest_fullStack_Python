from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.taco import Especialidad


class Taqueria:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.tacos = []

    @classmethod
    def get_all(cls):
        query = """
            SELECT id, nombre, created_at, updated_at
            FROM restaurantes
            ORDER BY id;
        """
        results = connectToMySQL("esquema_tacos").query_db(query)
        return [cls(taqueria) for taqueria in results] if results is not False else []

    @classmethod
    def get_with_tacos(cls, data):
        query = """
            SELECT
                restaurantes.id AS restaurante_id,
                restaurantes.nombre AS restaurante_nombre,
                restaurantes.created_at AS restaurante_created_at,
                restaurantes.updated_at AS restaurante_updated_at,
                tacos.id AS taco_id,
                tacos.tortilla AS taco_tortilla,
                tacos.guiso AS taco_guiso,
                tacos.salsa AS taco_salsa,
                tacos.restaurante_id AS taco_restaurante_id,
                tacos.created_at AS taco_created_at,
                tacos.updated_at AS taco_updated_at
            FROM restaurantes
            LEFT JOIN tacos ON tacos.restaurante_id = restaurantes.id
            WHERE restaurantes.id = %(id)s;
        """
        results = connectToMySQL("esquema_tacos").query_db(query, data)

        if not results:
            return None

        taqueria = cls(
            {
                "id": results[0]["restaurante_id"],
                "nombre": results[0]["restaurante_nombre"],
                "created_at": results[0]["restaurante_created_at"],
                "updated_at": results[0]["restaurante_updated_at"],
            }
        )

        for row in results:
            if row["taco_id"] is not None:
                taqueria.tacos.append(
                    Especialidad(
                        {
                            "id": row["taco_id"],
                            "tortilla": row["taco_tortilla"],
                            "guiso": row["taco_guiso"],
                            "salsa": row["taco_salsa"],
                            "restaurante_id": row["taco_restaurante_id"],
                            "created_at": row["taco_created_at"],
                            "updated_at": row["taco_updated_at"],
                        }
                    )
                )

        return taqueria
