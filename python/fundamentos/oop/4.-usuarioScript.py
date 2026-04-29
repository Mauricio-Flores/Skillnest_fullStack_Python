class UsuarioStreaming:
   def __init__(self, nombre, email, suscripcion="Gratis"):
       self.nombre = nombre
       self.email = email
       self.suscripcion = suscripcion
       self.lista_reproduccion = []


   def agregar_a_lista(self, titulo):
       """Agrega un contenido a la lista de reproducción del usuario."""
       self.lista_reproduccion.append(titulo)
       print(f"Titulo {titulo} agregado correctamente ")

   def ver_contenido(self, titulo):
        """Simula que el usuario reproduce un contenido."""
        if titulo in self.lista_reproduccion:
            print(f"el usuario {self.nombre} esta viendo '{titulo}'")
        else:
           print(f"Titulo no encontrado {titulo}")

   def cambiar_suscripcion(self, nueva_suscripcion):
        """Cambia el tipo de suscripción del usuario."""
        susAntigua = self.suscripcion
        self.suscripcion = nueva_suscripcion
        print(f"Suscripción cambió de {susAntigua} a {nueva_suscripcion}")

   def mostrar_info_usuario(self):
        """Muestra la información del usuario y su lista de reproducción."""
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
        print(f"Suscripción: {self.suscripcion}")
        if len(self.lista_reproduccion) == 0:
            print("La lista de reproduccion esta vacía")
        else:
            print(f"Lista de reproducción: \n- {"\n- ".join(self.lista_reproduccion)}")

camilo = UsuarioStreaming("camilo", "camilo@gmail.com")
camilo.agregar_a_lista("La casa de papel")
camilo.cambiar_suscripcion("premium")
camilo.ver_contenido("La casa de papel")
camilo.mostrar_info_usuario()

luis = UsuarioStreaming("luis", "luisechaverria@gmail.com")
luis.agregar_a_lista("Shrek")
luis.cambiar_suscripcion("estandar")
luis.ver_contenido("Shrek")
luis.mostrar_info_usuario()

#Todos los valores que se deban registrar debe ser con input
joaquinGamer = UsuarioStreaming("Joaquin" "JoaquinGamer@gey.com", "Gratis")
print(joaquinGamer)
#Añadir un menu de While para llamar a los métodos.
#(Menú de selección)

