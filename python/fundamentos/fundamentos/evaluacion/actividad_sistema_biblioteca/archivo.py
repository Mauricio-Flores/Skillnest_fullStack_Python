#Mauricio Flores
#Ignacio Dias
#Fabian Cartes 
#Ignacio Peña
#Alexiel Retamales
import os
def limpiarConsola():
    os.system('cls')
    
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
    def __init__(self, idLibro, nombreLibro, autor, fecha, disponible = True):
        self.idLibro = idLibro
        self.nombreLibro = nombreLibro
        self.disponible = disponible
        self.autor = autor
        self.fecha = fecha
        
    def mostrar_info(self):
        print(f"Nombre: {self.nombreLibro}\nAutor: {self.autor}\nfecha: {self.fecha}\nID: {self.idLibro}")
        
    def cambiar_disponibilidad(self):
        self.disponible = not self.disponible
    
class Prestamo:
    def __init__(self, usuario, libro, fecha):
        self.usuario = usuario
        self.libro = libro
        self.fecha = fecha 
        
    def pedir_prestamo(self):
        if self.libro.disponible == True:
            print("Prestamo concedido ")
            self.libro.cambiar_disponibilidad()
        else:
            print("El libro no esta disponible ")
    
    def devolver_libro(self):
        self.libro.cambiar_disponibilidad()
        
usuarios = []
libros = [
    Libro(1, "Cien años de soledad", "Gabriel García Márquez", "1967", ),
    Libro(2, "El principito", "Antoine de Saint-Exupéry", "1943"),
    Libro(3, "Don Quijote de la Mancha", "Miguel de Cervantes", "1605"),
    Libro(4, "Harry Potter y la piedra filosofal", "J.K. Rowling", "1997"),
    Libro(5, "El señor de los anillos", "J.R.R. Tolkien", "1954")
]
prestamos = []
contador_id = 1
libro_id = 6
while True:
    print("\n=== SISTEMA BIBLIOTECA ===")
    if len(usuarios) < 1:
        print("\nUsuarios: 0")
        nuevo_usuario = input("Agrega un usuario: ")
        print("Usuario agregado con exito!")
        correo = input("Ingresa tu correo: ")
        print("Correo agregado con exito!")
        nuevo = Usuario(contador_id, nuevo_usuario, correo)
        usuarios.append(nuevo)
        contador_id +=1
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
        print("0.- Salir")
        op = int(input("\nIngresa una opción\n"))
        if op == 1: #Alexiel
            limpiarConsola()
            nombre = input("Ingresa el nombre del usuario: ")
            correo = input("Ingresa el correo: ")
            nuevo_usuario = Usuario(contador_id, nombre, correo)
            usuarios.append(nuevo_usuario)
            print("Usuario agregado")
            contador_id += 1
        elif op == 2:
            limpiarConsola()
            print("De que usuario deseas ver la información:")
            for i in usuarios:
                print("ID:", i.idUsuario, "Nombre: ", i.nombre)
            op = int(input("Ingresa solo el id del usuario que deseas ver\n"))
            for i in usuarios:
                if i.idUsuario == op:
                    i.mostrar_datos()
            continue
        elif op == 3:
            limpiarConsola()
            print("De que usuario deseas cambiar el correo: ")
            for i in usuarios:
                print("ID:", i.idUsuario, "Nombre: ", i.nombre, "Correo: ", i.correo)
            op = int(input("Ingresa solo el id del usuario que deseas cambiar el correo\n"))
            for i in usuarios:
                if i.idUsuario == op:
                    nuevoCorreo = input("Ingresa tu nuevo correo: ")
                    i.cambiar_correo(nuevoCorreo)
            continue
        elif op == 4:
            limpiarConsola()
            for i in libros:
                if i.disponible == True:
                    print(i.nombreLibro, "- Disponible")
            continue
        elif op == 5:
            limpiarConsola()
            print("agregar libro")
            nombre = input ("Nombre oh titulo de libro")
            autor = input ("autor de libro")
            fecha = input ("año de publicacion")
            nuevo_libro = Libro(libro_id,nombre,autor,fecha)
            libros.append(nuevo_libro)
            libro_id += 1
        elif op == 6:
            limpiarConsola()
            for i in libros:
                print(f"ID: {i.idLibro} nombre: {i.nombreLibro}")
            op = int(input("Ingresa solo el id del libro que deseas ver\n"))
            limpiarConsola()
            for i in libros:
                if i.idLibro == op:
                    i.mostrar_info()
            continue
        elif op == 7:
            limpiarConsola()
            for i in usuarios:
                print(f"ID: {i.idUsuario} nombre: {i.nombre}")
            op_usuario = int(input("Ingresa solo el id del usuario que va a hacer el prestamo\n"))
            for i in usuarios:
                if i.idUsuario == op_usuario:
                    print(f"{i.nombre} ¿Que libro deseas pedir prestado?\n")
                    for e in libros:
                        if e.disponible == True:
                            print(f"ID: {e.idLibro} nombre: {e.nombreLibro}")
                    op_libro = int(input("Que libro deseas pedir prestado (Ingresa solo el id): "))
                    for e in libros:
                        if e.idLibro == op_libro:
                            fecha = input("En cuantos dias haras devolución: ")
                            nuevo = Prestamo(i, e, fecha )
                            prestamos.append(nuevo)
                            nuevo.pedir_prestamo()  
            continue
        elif op == 8:
            limpiarConsola()
            print("Libro para devolver: ")
            for i in libros:
                if i.disponible == False:
                    print(f"ID: {i.idLibro}, nombre: {i.nombreLibro}")
            op = int(input("Que libro deseas devolver(Ingresa solo el ID): "))
            for p in prestamos:
                if p.libro.idLibro == op:
                    p.devolver_libro()
        elif op == 0:
            break