from conexion import conectar


class Usuario:

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.email = datos["email"]


    @classmethod
    def listar(cls):
        sql = '''
        SELECT *
        FROM usuarios
        ORDER BY id;
        '''

        registros = conectar("esquema_usuarios").ejecutar(sql)

        return [cls(usuario) for usuario in registros]


    @classmethod
    def crear(cls, datos):
        sql = '''
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
        '''

        return conectar("esquema_usuarios").ejecutar(sql, datos)
