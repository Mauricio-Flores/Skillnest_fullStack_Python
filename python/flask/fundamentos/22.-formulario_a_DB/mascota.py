from conexion import conectar


class Animal:

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre_animal = datos["nombre"]
        self.categoria = datos["tipo"]
        self.detalle = datos["color"]
        self.creado = datos["created_at"]
        self.actualizado = datos["updated_at"]


    @classmethod
    def listar(cls):

        consulta = """
            SELECT
                id,
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            FROM mascotas
            ORDER BY id;
        """

        registros = conectar(
            "primera_flask"
        ).ejecutar(consulta)


        animales = []

        for registro in registros:
            animales.append(
                cls(registro)
            )

        return animales


    @classmethod
    def crear(cls, datos):

        consulta = """
            INSERT INTO mascotas
            (
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            )
            VALUES
            (
                %(nombre)s,
                %(tipo)s,
                %(color)s,
                NOW(),
                NOW()
            );
        """

        return conectar(
            "primera_flask"
        ).ejecutar(
            consulta,
            datos
        )