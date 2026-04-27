#Creación de la clase usuario - entidad
class Usuario:
    def __init__(self): #constructor
        self.nombre = "Nariyoshi"
        self.apellido = "Miyagi"
        self.email = "miyagi@codingdojo.la"
        self.limite_credito = 30000
        self.saldo_pagar = 0

#Instancias de una clase
miyagi = Usuario()

daniel = Usuario()

dany = Usuario()

#Accedemos a los atributos de la instancia
print(miyagi.nombre) #Imprime: Nariyoshi
print(daniel.apellido) #Imprime: Miyagi
print(daniel.email) #Imprime: miyagi@codingdojo.la
print(daniel.limite_credito) #Imprime:30000
print(daniel.saldo_pagar) #Imprimer: 0

#Nuevos valores asignados a atributos de la instancia
daniel.nombre = "Juan"
daniel.apellido = "Diaz"
daniel.email = "miyagi@codingdojo.la"
daniel.limite_credito = 320000
daniel.saldo_pagar = 120

print(daniel.saldo_pagar) #Imprimer: 0

#Valores anueva instancia

dany.nombre = "Dani"
dany.apellido = "nose"
dany.email = "Dani@codingdojo.la"
dany.limite_credito = 520000
dany.saldo_pagar = 1200

#Imprime cada instancia
print(miyagi.nombre) 
print(daniel.nombre) 
print(dany.email) 
