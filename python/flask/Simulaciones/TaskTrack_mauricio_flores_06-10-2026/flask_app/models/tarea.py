from datetime import date, datetime

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


DB = "tasktrack"
PRIORIDADES = ("Alta", "Media", "Baja")
ESTADOS = ("Pendiente", "En progreso", "Completada")


class Tarea:
    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.descripcion = data["descripcion"]
        self.prioridad = data["prioridad"]
        self.estado = data["estado"]
        self.fecha_limite = data["fecha_limite"]
        self.usuario_id = data["usuario_id"]
        self.categoria_id = data["categoria_id"]
        self.categoria = data.get("categoria", "")
        self.creador = data.get("creador", "")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO tareas
                (titulo, descripcion, prioridad, estado, fecha_limite, usuario_id, categoria_id)
            VALUES
                (%(titulo)s, %(descripcion)s, %(prioridad)s, 'Pendiente',
                 %(fecha_limite)s, %(usuario_id)s, %(categoria_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_del_usuario(cls, usuario_id, estado="", busqueda=""):
        query = """
            SELECT t.*, c.nombre AS categoria,
                   CONCAT(u.nombre, ' ', u.apellido) AS creador
            FROM tareas t
            JOIN categorias c ON c.id = t.categoria_id
            JOIN usuarios u ON u.id = t.usuario_id
            WHERE t.usuario_id = %(usuario_id)s
        """
        data = {"usuario_id": usuario_id, "estado": estado, "busqueda": f"%{busqueda}%"}
        if estado in ESTADOS:
            query += " AND t.estado = %(estado)s"
        if busqueda:
            query += " AND t.titulo LIKE %(busqueda)s"
        query += " ORDER BY t.fecha_limite ASC, t.created_at DESC;"
        resultados = connectToMySQL(DB).query_db(query, data) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def obtener_proximas(cls, usuario_id, limite=5):
        query = """
            SELECT t.*, c.nombre AS categoria,
                   CONCAT(u.nombre, ' ', u.apellido) AS creador
            FROM tareas t
            JOIN categorias c ON c.id = t.categoria_id
            JOIN usuarios u ON u.id = t.usuario_id
            WHERE t.usuario_id = %(usuario_id)s
              AND t.fecha_limite >= CURDATE()
              AND t.estado != 'Completada'
            ORDER BY t.fecha_limite ASC
            LIMIT %(limite)s;
        """
        resultados = connectToMySQL(DB).query_db(
            query, {"usuario_id": usuario_id, "limite": limite}
        ) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def obtener_por_id_y_usuario(cls, tarea_id, usuario_id):
        query = """
            SELECT t.*, c.nombre AS categoria,
                   CONCAT(u.nombre, ' ', u.apellido) AS creador
            FROM tareas t
            JOIN categorias c ON c.id = t.categoria_id
            JOIN usuarios u ON u.id = t.usuario_id
            WHERE t.id = %(id)s AND t.usuario_id = %(usuario_id)s
            LIMIT 1;
        """
        resultado = connectToMySQL(DB).query_db(
            query, {"id": tarea_id, "usuario_id": usuario_id}
        )
        return cls(resultado[0]) if resultado else None

    @classmethod
    def obtener_por_categoria(cls, categoria_id, usuario_id):
        query = """
            SELECT t.*, c.nombre AS categoria,
                   CONCAT(u.nombre, ' ', u.apellido) AS creador
            FROM tareas t
            JOIN categorias c ON c.id = t.categoria_id
            JOIN usuarios u ON u.id = t.usuario_id
            WHERE t.categoria_id = %(categoria_id)s AND t.usuario_id = %(usuario_id)s
            ORDER BY t.fecha_limite ASC;
        """
        resultados = connectToMySQL(DB).query_db(
            query, {"categoria_id": categoria_id, "usuario_id": usuario_id}
        ) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE tareas SET titulo = %(titulo)s, descripcion = %(descripcion)s,
                prioridad = %(prioridad)s, estado = %(estado)s,
                fecha_limite = %(fecha_limite)s, categoria_id = %(categoria_id)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def completar(cls, tarea_id, usuario_id):
        query = """
            UPDATE tareas SET estado = 'Completada'
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB).query_db(query, {"id": tarea_id, "usuario_id": usuario_id})

    @classmethod
    def borrar(cls, tarea_id, usuario_id):
        query = "DELETE FROM tareas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(DB).query_db(query, {"id": tarea_id, "usuario_id": usuario_id})

    @classmethod
    def resumen(cls, usuario_id):
        query = """
            SELECT COUNT(*) AS total,
                SUM(estado = 'Pendiente') AS pendientes,
                SUM(estado = 'En progreso') AS en_progreso,
                SUM(estado = 'Completada') AS completadas,
                SUM(prioridad = 'Alta') AS alta,
                SUM(prioridad = 'Media') AS media,
                SUM(prioridad = 'Baja') AS baja
            FROM tareas WHERE usuario_id = %(usuario_id)s;
        """
        resultado = connectToMySQL(DB).query_db(query, {"usuario_id": usuario_id})
        vacio = {"total": 0, "pendientes": 0, "en_progreso": 0, "completadas": 0,
                 "alta": 0, "media": 0, "baja": 0}
        if not resultado:
            return vacio
        return {clave: (valor or 0) for clave, valor in resultado[0].items()}

    @staticmethod
    def dias_restantes(fecha_limite):
        if isinstance(fecha_limite, datetime):
            fecha_limite = fecha_limite.date()
        return (fecha_limite - date.today()).days

    @staticmethod
    def validar(formulario, usuario_id, permitir_pasada=False):
        valido = True
        titulo = formulario.get("titulo", "").strip()
        descripcion = formulario.get("descripcion", "").strip()
        prioridad = formulario.get("prioridad", "")
        estado = formulario.get("estado", "Pendiente")
        fecha_texto = formulario.get("fecha_limite", "")
        categoria_id = formulario.get("categoria_id", "")

        if len(titulo) < 3:
            flash("El título debe tener al menos 3 caracteres.", "tarea")
            valido = False
        if len(descripcion) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "tarea")
            valido = False
        if prioridad not in PRIORIDADES:
            flash("Selecciona una prioridad válida.", "tarea")
            valido = False
        if estado not in ESTADOS:
            flash("Selecciona un estado válido.", "tarea")
            valido = False

        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
            if not permitir_pasada and fecha < date.today():
                flash("La fecha límite no puede estar en el pasado.", "tarea")
                valido = False
        except ValueError:
            flash("Ingresa una fecha límite válida.", "tarea")
            valido = False

        try:
            categoria_id = int(categoria_id)
        except (TypeError, ValueError):
            categoria_id = 0

        from flask_app.models.categoria import Categoria

        if not Categoria.obtener_por_id_y_usuario(categoria_id, usuario_id):
            flash("Selecciona una categoría que te pertenezca.", "tarea")
            valido = False
        return valido
