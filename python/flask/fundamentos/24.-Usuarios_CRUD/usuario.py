from conexion import conectar


class Usuario:

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.email = datos["email"]
        self.fecha_creacion = datos["created_at"]
        self.fecha_actualizacion = datos["updated_at"]


    @classmethod
    def listar(cls):

        sql = """
        SELECT *
        FROM usuarios
        ORDER BY id;
        """

        registros = conectar("esquema_usuarios").ejecutar(sql)

        usuarios = []

        for registro in registros:
            usuarios.append(cls(registro))

        return usuarios


    @classmethod
    def crear(cls, datos):

        sql = """
        INSERT INTO usuarios
        (
            nombre,
            apellido,
            email,
            created_at,
            updated_at
        )
        VALUES
        (
            %(nombre)s,
            %(apellido)s,
            %(email)s,
            NOW(),
            NOW()
        );
        """

        return conectar("esquema_usuarios").ejecutar(sql, datos)
