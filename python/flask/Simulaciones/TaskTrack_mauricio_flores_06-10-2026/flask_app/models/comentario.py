from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


DB = "tasktrack"


class Comentario:
    def __init__(self, data):
        self.id = data["id"]
        self.contenido = data["contenido"]
        self.usuario_id = data["usuario_id"]
        self.tarea_id = data["tarea_id"]
        self.autor = data.get("autor", "")
        self.created_at = data.get("created_at")

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO comentarios (contenido, usuario_id, tarea_id)
            VALUES (%(contenido)s, %(usuario_id)s, %(tarea_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_de_tarea(cls, tarea_id):
        query = """
            SELECT c.*, CONCAT(u.nombre, ' ', u.apellido) AS autor
            FROM comentarios c
            JOIN usuarios u ON u.id = c.usuario_id
            WHERE c.tarea_id = %(tarea_id)s
            ORDER BY c.created_at ASC;
        """
        resultados = connectToMySQL(DB).query_db(query, {"tarea_id": tarea_id}) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def borrar(cls, comentario_id, usuario_id, tarea_id):
        query = """
            DELETE FROM comentarios
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s AND tarea_id = %(tarea_id)s;
        """
        return connectToMySQL(DB).query_db(
            query, {"id": comentario_id, "usuario_id": usuario_id, "tarea_id": tarea_id}
        )

    @staticmethod
    def validar(contenido):
        if len(contenido.strip()) < 2:
            flash("El comentario debe tener al menos 2 caracteres.", "comentario")
            return False
        if len(contenido.strip()) > 500:
            flash("El comentario no puede superar los 500 caracteres.", "comentario")
            return False
        return True
