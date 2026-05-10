class SuscripcionStreaming:
    costos_suscripcion = {
        "Gratis": 0,
        "Estándar": 5.99,
        "Premium": 10.99
    }

    def __init__(self, usuario, tipo_suscripcion="Gratis"):
        self.usuario = usuario
        self.tipo_suscripcion = tipo_suscripcion
        self.costo_mensual = self.costos_suscripcion[tipo_suscripcion]
        self.saldo_pendiente = self.costo_mensual

    def realizar_pago(self, monto):
        """Reduce el saldo pendiente según el monto pagado."""

        self.saldo_pendiente = self.saldo_pendiente - monto

        if self.saldo_pendiente < 0:
            self.saldo_pendiente = 0

        print(self.usuario, "pagó", monto)
        print("Saldo pendiente:", self.saldo_pendiente)

    def cambiar_suscripcion(self, nuevo_tipo):
        """Cambia el tipo de suscripción y actualiza el costo mensual."""
        
        if nuevo_tipo == "Gratis" or nuevo_tipo == "Estándar" or nuevo_tipo == "Premium":

            self.tipo_suscripcion = nuevo_tipo
            self.costo_mensual = self.costos_suscripcion[nuevo_tipo]
            self.saldo_pendiente += self.costo_mensual

            print(self.usuario, "cambió su suscripción a", nuevo_tipo)
        else:
            print("Tipo de suscripción no válido")
    def ver_contenido_exclusivo(self):
        """Permite ver contenido exclusivo según el tipo de suscripción."""

        if self.tipo_suscripcion == "Gratis":
            print(self.usuario, "no tiene acceso a contenido exclusivo")

        else:
            print(self.usuario, "puede ver contenido exclusivo")

    def mostrar_info_suscripcion(self):
        """Muestra la información de la suscripción del usuario."""

        print("\n--- Información de Suscripción ---")
        print(f"Usuario: {self.usuario}")
        print(f"Tipo: {self.tipo_suscripcion}")
        print(f"Costo mensual: {self.costo_mensual}")
        print(f"Saldo pendiente: {self.saldo_pendiente}")


# ---------------- PRUEBAS ----------------

# Crear 3 usuarios
usuario1 = SuscripcionStreaming("Juan", "Gratis")
usuario2 = SuscripcionStreaming("María", "Estándar")
usuario3 = SuscripcionStreaming("Pedro", "Premium")


# Primer usuario
usuario1.ver_contenido_exclusivo()
usuario1.cambiar_suscripcion("Estándar")
usuario1.realizar_pago(5.99)
usuario1.mostrar_info_suscripcion()


# Segundo usuario
usuario2.ver_contenido_exclusivo()
usuario2.cambiar_suscripcion("Premium")
usuario2.realizar_pago(3)
usuario2.realizar_pago(15)
usuario2.mostrar_info_suscripcion()


# Tercer usuario
usuario3.realizar_pago(5)
usuario3.ver_contenido_exclusivo()
usuario3.mostrar_info_suscripcion()