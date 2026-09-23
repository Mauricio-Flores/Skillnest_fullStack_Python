from conexion import conectar

class Usuario:

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.email = datos["email"]

    @classmethod
    def listar(cls):
        sql = "SELECT * FROM usuarios ORDER BY id;"
        datos = conectar("esquema_usuarios").ejecutar(sql)
        return [cls(usuario) for usuario in datos]

    @classmethod
    def buscar(cls, id):
        sql = "SELECT * FROM usuarios WHERE id=%(id)s;"
        datos = conectar("esquema_usuarios").ejecutar(sql, {"id": id})
        return cls(datos[0]) if datos else None

    @classmethod
    def actualizar(cls, datos):
        sql = """
        UPDATE usuarios
        SET nombre=%(nombre)s,
            apellido=%(apellido)s,
            email=%(email)s,
            updated_at=NOW()
        WHERE id=%(id)s;
        """
        return conectar("esquema_usuarios").ejecutar(sql, datos)

    @classmethod
    def eliminar(cls, id):
        sql = "DELETE FROM usuarios WHERE id=%(id)s;"
        return conectar("esquema_usuarios").ejecutar(sql, {"id": id})
