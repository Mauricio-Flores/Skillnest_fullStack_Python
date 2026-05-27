'''
Escenario Genérico (Debe seleccionar)
Una empresa necesita desarrollar un sistema para administrar información básica de sus procesos internos. El sistema deberá permitir registrar entidades relevantes del negocio, almacenar información organizada y relacionar los datos entre sí.
Cada grupo deberá trabajar sobre un escenario asignado por el docente (biblioteca, veterinaria, tienda, gimnasio, videojuegos, escuela, entre otros) y diseñar una solución utilizando Programación Orientada a Objetos.
El trabajo debe considerar exclusivamente la creación de 3 clases principales relacionadas entre sí. Posteriormente, dichas clases deberán transformarse en tablas de base de datos relacionales utilizando SQL, incorporando claves primarias, claves foráneas y campos de auditoría.


Escenario 1 — Sistema de Biblioteca
Una biblioteca necesita un sistema para administrar sus libros, usuarios y préstamos. El objetivo es organizar la información y controlar qué usuarios solicitan libros.
Clases sugeridas
Usuario
Libro
Prestamo
Métodos sugeridos
Clase Usuario
mostrar_datos()
actualizar_correo()
Clase Libro
mostrar_informacion()
cambiar_disponibilidad()
Clase Prestamo
registrar_prestamo()
devolver_libro()
'''

class Usuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def mostrar_datos(self):
        return f"Nombre: {self.nombre}, Correo: {self.correo}"

    def actualizar_correo(self, nuevo_correo):
        self.correo = nuevo_correo
        return f"Correo actualizado a: {self.correo}"

class Libro:
    def __init__(self, titulo, autor, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def mostrar_informacion(self):
        disponibilidad = "Disponible" if self.disponible else "No disponible"
        return f"Título: {self.titulo}, Autor: {self.autor}, Disponibilidad: {disponibilidad}"

    def cambiar_disponibilidad(self):
        self.disponible = not self.disponible
        estado = "Disponible" if self.disponible else "No disponible"
        return f"El libro '{self.titulo}' ahora está {estado}."

class Prestamo:
    def __init__(self, usuario, libro):
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = None
        self.fecha_devolucion = None

    def registrar_prestamo(self, fecha_prestamo):
        if self.libro.disponible:
            self.libro.cambiar_disponibilidad()
            self.fecha_prestamo = fecha_prestamo
            return f"Préstamo registrado: {self.usuario.nombre} ha prestado '{self.libro.titulo}' el {self.fecha_prestamo}."
        else:
            return f"El libro '{self.libro.titulo}' no está disponible para préstamo."

    def devolver_libro(self, fecha_devolucion):
        if not self.libro.disponible:
            self.libro.cambiar_disponibilidad()
            self.fecha_devolucion = fecha_devolucion
            return f"Libro devuelto: {self.usuario.nombre} ha devuelto '{self.libro.titulo}' el {self.fecha_devolucion}."
        else:
            return f"El libro '{self.libro.titulo}' ya está disponible, no se puede devolver."

