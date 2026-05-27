import os
import mysql.connector

def limpiarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="library"
)

cursor = conexion.cursor(dictionary=True)

class Usuario:
    def __init__(self, idUsuario, nombre, correo):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.correo = correo

    def mostrar_datos(self):
        print(f"Nombre: {self.nombre}\nCorreo: {self.correo}\nID: {self.idUsuario}")

    def cambiar_correo(self, nCorreo):
        self.correo = nCorreo

class Libro:
    def __init__(self, idLibro, nombreLibro, autor, stock):
        self.idLibro = idLibro
        self.nombreLibro = nombreLibro
        self.autor = autor
        self.stock = stock

    def mostrar_info(self):
        print(f"Nombre: {self.nombreLibro}\nAutor: {self.autor}\nStock: {self.stock}\nID: {self.idLibro}")

class Prestamo:
    def __init__(self, usuario, libro, fecha):
        self.usuario = usuario
        self.libro = libro
        self.fecha = fecha

usuarios = []
libros = []
prestamos = []

while True:
    print("\n=== SISTEMA BIBLIOTECA ===")
    cursor.execute("SELECT * FROM usuarios WHERE deleted = 0")
    usuarios_db = cursor.fetchall()
    if len(usuarios_db) < 1:
        print("\nUsuarios: 0")
        nuevo_usuario = input("Agrega un usuario: ")
        print("Usuario agregado con exito!")
        correo = input("Ingresa tu correo: ")
        print("Correo agregado con exito!")
        sql = """
        INSERT INTO usuarios(nombre, correo)
        VALUES(%s, %s)
        """
        valores = (nuevo_usuario, correo)
        cursor.execute(sql, valores)
        conexion.commit()
        continue
    else:
        print("Elige una opción: ")
        print("1.- Agregar nuevo usuario")
        print("2.- ver información de usuario")
        print("3.- cambiar correo")
        print("4.- ver libros disponibles")
        print("5.- Agregar un libro")
        print("6.- mostrar info de un libro")
        print("7.- hacer un prestamo")
        print("8.- devolver libro")
        print("9.- ver prestamos")
        print("0.- Salir")
        op = int(input("\nIngresa una opción\n"))
        if op == 1:
            limpiarConsola()
            nombre = input("Ingresa el nombre del usuario: ")
            correo = input("Ingresa el correo: ")
            sql = """
            INSERT INTO usuarios(nombre, correo)
            VALUES(%s, %s)
            """
            valores = (nombre, correo)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Usuario agregado")
        elif op == 2:
            limpiarConsola()
            print("De que usuario deseas ver la información:")
            cursor.execute("SELECT * FROM usuarios WHERE deleted = 0")
            usuarios_db = cursor.fetchall()
            for i in usuarios_db:
                print("ID:", i["id_usuario"], "Nombre:", i["nombre"])
            op = int(input("Ingresa solo el id del usuario que deseas ver\n"))
            cursor.execute("""
            SELECT * FROM usuarios
            WHERE id_usuario = %s
            """, (op,))
            usuario = cursor.fetchone()
            if usuario:
                print(f"Nombre: {usuario['nombre']}")
                print(f"Correo: {usuario['correo']}")
                print(f"ID: {usuario['id_usuario']}")
            continue
        elif op == 3:
            limpiarConsola()
            print("De que usuario deseas cambiar el correo: ")
            cursor.execute("SELECT * FROM usuarios WHERE deleted = 0")
            usuarios_db = cursor.fetchall()
            for i in usuarios_db:
                print("ID:", i["id_usuario"], "Nombre:", i["nombre"], "Correo:", i["correo"])
            op = int(input("Ingresa solo el id del usuario que deseas cambiar el correo\n"))
            nuevoCorreo = input("Ingresa tu nuevo correo: ")
            cursor.execute("""
            UPDATE usuarios
            SET correo = %s
            WHERE id_usuario = %s
            """, (nuevoCorreo, op))
            conexion.commit()
            continue
        elif op == 4:
            limpiarConsola()
            cursor.execute("""
            SELECT * FROM libros
            WHERE stock > 0
            AND deleted = 0
            """)
            libros_db = cursor.fetchall()
            for i in libros_db:
                print(i["titulo"], "- Disponible")
            continue
        elif op == 5:
            limpiarConsola()
            print("agregar libro")
            nombre = input("Nombre o titulo de libro: ")
            autor = input("autor de libro: ")
            stock = int(input("Cantidad de libros: "))
            sql = """
            INSERT INTO libros(titulo, autor, stock)
            VALUES(%s, %s, %s)
            """
            valores = (nombre, autor, stock)
            cursor.execute(sql, valores)
            conexion.commit()
        elif op == 6:
            limpiarConsola()
            cursor.execute("""
            SELECT * FROM libros
            WHERE deleted = 0
            """)
            libros_db = cursor.fetchall()
            for i in libros_db:
                print(f"ID: {i['id_libro']} nombre: {i['titulo']}")
            op = int(input("Ingresa solo el id del libro que deseas ver\n"))
            limpiarConsola()
            cursor.execute("""
            SELECT * FROM libros
            WHERE id_libro = %s
            """, (op,))
            libro = cursor.fetchone()
            if libro:
                print(f"Nombre: {libro['titulo']}")
                print(f"Autor: {libro['autor']}")
                print(f"Stock: {libro['stock']}")
                print(f"ID: {libro['id_libro']}")
            continue
        elif op == 7:
            limpiarConsola()
            cursor.execute("""
            SELECT * FROM usuarios
            WHERE deleted = 0
            """)
            usuarios_db = cursor.fetchall()
            for i in usuarios_db:
                print(f"ID: {i['id_usuario']} nombre: {i['nombre']}")
            op_usuario = int(input("Ingresa solo el id del usuario que va a hacer el prestamo\n"))
            print("¿Que libro deseas pedir prestado?\n")
            cursor.execute("""
            SELECT * FROM libros
            WHERE stock > 0
            AND deleted = 0
            """)
            libros_db = cursor.fetchall()
            for e in libros_db:
                print(f"ID: {e['id_libro']} nombre: {e['titulo']}")
            op_libro = int(input("Que libro deseas pedir prestado (Ingresa solo el id): "))
            cursor.execute("""
            INSERT INTO prestamos(id_usuario, id_libro, fecha_prestamo)
            VALUES(%s, %s, NOW())
            """, (op_usuario, op_libro))
            cursor.execute("""
            UPDATE libros
            SET stock = stock - 1
            WHERE id_libro = %s
            """, (op_libro,))
            conexion.commit()
            print("Prestamo concedido")
            continue
        elif op == 8:
            limpiarConsola()
            print("Libro para devolver: ")
            cursor.execute("""
            SELECT prestamos.id_prestamo, libros.titulo
            FROM prestamos
            INNER JOIN libros
            ON prestamos.id_libro = libros.id_libro
            WHERE prestamos.estado = 1
            """)
            prestamos_db = cursor.fetchall()
            for i in prestamos_db:
                print(f"ID Prestamo: {i['id_prestamo']}, Libro: {i['titulo']}")
            op = int(input("Que prestamo deseas devolver(Ingresa solo el ID): "))
            cursor.execute("""
            SELECT * FROM prestamos
            WHERE id_prestamo = %s
            """, (op,))
            prestamo = cursor.fetchone()
            if prestamo:
                cursor.execute("""
                UPDATE libros
                SET stock = stock + 1
                WHERE id_libro = %s
                """, (prestamo["id_libro"],))
                cursor.execute("""
                UPDATE prestamos
                SET estado = 0
                WHERE id_prestamo = %s
                """, (op,))
                conexion.commit()
                print("Libro devuelto")
        elif op == 9:
            limpiarConsola()
            cursor.execute("""
            SELECT
            prestamos.id_prestamo,
            usuarios.nombre,
            libros.titulo,
            prestamos.fecha_prestamo,
            prestamos.estado
            FROM prestamos
            INNER JOIN usuarios
            ON prestamos.id_usuario = usuarios.id_usuario
            INNER JOIN libros
            ON prestamos.id_libro = libros.id_libro
            """)
            prestamos_db = cursor.fetchall()
            for p in prestamos_db:
                estado = "Activo"
                if p["estado"] == 0:
                    estado = "Devuelto"
                print(f"""
Prestamo ID: {p['id_prestamo']}
Usuario: {p['nombre']}
Libro: {p['titulo']}
Fecha: {p['fecha_prestamo']}
Estado: {estado}
""")
            continue
        elif op == 0:
            cursor.close()
            conexion.close()
            break