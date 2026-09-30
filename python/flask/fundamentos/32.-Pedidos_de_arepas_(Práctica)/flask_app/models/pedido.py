from flask import flash

from flask_app.config.mysqlconnection import connect_to_mysql


class OrdenArepa:
    """Representa un pedido almacenado en la tabla pedidos."""

    database = "esquema_arepas"

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.tipo_arepa = data["tipo_arepa"]
        self.cantidad = data["cantidad"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validar_pedido(data):
        es_valido = True

        if not data["nombre"]:
            flash("El nombre es obligatorio.", "danger")
            es_valido = False
        elif len(data["nombre"]) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        if not data["tipo_arepa"]:
            flash("El tipo de arepa es obligatorio.", "danger")
            es_valido = False

        if not data["cantidad"]:
            flash("La cantidad es obligatoria.", "danger")
            es_valido = False
        else:
            try:
                if int(data["cantidad"]) <= 0:
                    flash("La cantidad debe ser mayor que 0.", "danger")
                    es_valido = False
            except ValueError:
                flash("La cantidad debe ser mayor que 0.", "danger")
                es_valido = False

        return es_valido

    @classmethod
    def get_all(cls):
        query = """
            SELECT id, nombre, tipo_arepa, cantidad, created_at, updated_at
            FROM pedidos
            ORDER BY id DESC;
        """
        results = connect_to_mysql(cls.database).query_db(query) or []
        return [cls(row) for row in results]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO pedidos (nombre, tipo_arepa, cantidad)
            VALUES (%(nombre)s, %(tipo_arepa)s, %(cantidad)s);
        """
        return connect_to_mysql(cls.database).query_db(query, data)
