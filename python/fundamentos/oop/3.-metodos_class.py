class Usuario:
    def __init__(self, nombre, apellido, email):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.limite_credito = 30000
        self.saldo_pagar = 0
    def hacer_compra(self, monto):  #recibe como argumento el monto de la compra
        self.saldo_pagar += monto   #el saldo a pagar del usuario aumenta en la cantidad del valor recibido
    def aumentarCredito(self, aumento):
        self.limite_credito += aumento
    def cambiarCorreo(self, email):
        self.email = email

# Instacias de la clase
miyagi = Usuario("Nariyoshi", "Miyagi", "miyagi@codingdojo.la")
daniel = Usuario("Daniel", "Larusso", "daniel@codingdojo.la")

miyagi.hacer_compra(2000)
print(f"Primera compra de {miyagi.nombre}: ${miyagi.saldo_pagar}")
segundaCompra = 300
miyagi.hacer_compra(segundaCompra)
print(f"Segunda compra: ${segundaCompra}")
#Imprimir cuanto credito le queda a Miyagi
print(f"Credito disponible: ${miyagi.limite_credito - miyagi.saldo_pagar}")
#Compras de Daniel 2 compras y muesta saldo a pagar
print("---------------Compras Daniel----------------")
daniel.hacer_compra(45)
print(daniel.saldo_pagar)

#Tarea
'''
1.- Crear un nuevo método que permita aumentar el limite de crédito.
Imprimir el nuevo limite de crédito

2.- Crear un método que permita le cambiar el correo de la instancia.
Mostrar el nuevo correo
'''
miyagi.aumentarCredito(2000)
print(f"El nuevo límite de crédito es: {miyagi.limite_credito}")

miyagi.cambiarCorreo("miyagiPro@gmail.com")
print(f"El nuevo correo establecido es: {miyagi.email}")