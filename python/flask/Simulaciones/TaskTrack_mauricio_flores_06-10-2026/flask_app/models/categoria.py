from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


DB = "tasktrack"


class Categoria:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.usuario_id = data["usuario_id"]
        self.cantidad_tareas = data.get("cantidad_tareas", 0)
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    @classmethod
    def crear(cls, data):
        query = "INSERT INTO categorias (nombre, usuario_id) VALUES (%(nombre)s, %(usuario_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_del_usuario(cls, usuario_id):
        query = """
            SELECT c.*, COUNT(t.id) AS cantidad_tareas
            FROM categorias c
            LEFT JOIN tareas t ON t.categoria_id = c.id
            WHERE c.usuario_id = %(usuario_id)s
            GROUP BY c.id
            ORDER BY c.nombre ASC;
        """
        resultados = connectToMySQL(DB).query_db(query, {"usuario_id": usuario_id}) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def obtener_por_id_y_usuario(cls, categoria_id, usuario_id):
        query = """
            SELECT c.*, COUNT(t.id) AS cantidad_tareas
            FROM categorias c
            LEFT JOIN tareas t ON t.categoria_id = c.id
            WHERE c.id = %(id)s AND c.usuario_id = %(usuario_id)s
            GROUP BY c.id;
        """
        resultado = connectToMySQL(DB).query_db(
            query, {"id": categoria_id, "usuario_id": usuario_id}
        )
        return cls(resultado[0]) if resultado else None

    @classmethod
    def existe_nombre(cls, nombre, usuario_id, excluir_id=None):
        query = """
            SELECT id FROM categorias
            WHERE LOWER(nombre) = LOWER(%(nombre)s) AND usuario_id = %(usuario_id)s
        """
        data = {"nombre": nombre, "usuario_id": usuario_id}
        if excluir_id:
            query += " AND id != %(excluir_id)s"
            data["excluir_id"] = excluir_id
        query += " LIMIT 1;"
        return bool(connectToMySQL(DB).query_db(query, data))

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE categorias SET nombre = %(nombre)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def borrar(cls, categoria_id, usuario_id):
        query = "DELETE FROM categorias WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(DB).query_db(query, {"id": categoria_id, "usuario_id": usuario_id})

    @staticmethod
    def validar(nombre, usuario_id, excluir_id=None):
        nombre = nombre.strip()
        if len(nombre) < 3:
            flash("El nombre de la categoría debe tener al menos 3 caracteres.", "categoria")
            return False
        if Categoria.existe_nombre(nombre, usuario_id, excluir_id):
            flash("Ya tienes una categoría con ese nombre.", "categoria")
            return False
        return True
