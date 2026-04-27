#
class Usuario:
   def __init__(self, nombre, apellido, email, limite_credito, salario_pagar):
       self.nombre = nombre
       self.apellido = apellido
       self.email = email
       self.limite_credito = limite_credito
       self.saldo_pagar = salario_pagar 

#Creación de instacias
miyagi = Usuario("Nariyoshi", "Miyagi", "miyagi@codingdojo.la", 10000, 300)
daniel = Usuario("Daniel", "Larusso", "daniel@codingdojo.la", 20000, 150)
daniel = Usuario("Dany", "Hernandez", "dany@codingdojo.com", 3000 ,200)

#Imprimir valores
print(miyagi.nombre) #Imprime: Nariyoshi
print(daniel.nombre) #Imprime: Daniel

#---------------------------
#--- Tarea rápida
'''
Crear una clase Estudiante, y asignarle los siguientes atributos:
(rut, nombre, apellido, especialidad, fecha_nac)
- Crear 3 instancias para la clase con distintos estudiantes
- Imprimir el nombre y apellido concatenado + especialidad
'''
class Estudiante:
    def __init__(self, rut, nombre, apellido, especialidad, fecha_nac):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.especialidad = especialidad 
        self.fecha_nac = fecha_nac

randy = Estudiante("22.898.879-0", "Randy", "Cortinez", "Programación", "01-01-2008")
Joaquin = Estudiante("22.433.567-2", "Joaquin", "Perez", "Programación", "01-09-2008")
Akon = Estudiante("21.999.991-9", "Akon", "Bustamante", "Programación", "22-05-2008")

print(f"My nombre es: {randy.nombre}, My apellido es: {randy.apellido}, Y pertenesco a: {randy.especialidad}")
print(f"My nombre es: {Akon.nombre}, My apellido es: {Akon.apellido}, Y pertenesco a: {Akon.especialidad}")
print(f"My nombre es: {Joaquin.nombre}, My apellido es: {Joaquin.apellido}, Y pertenesco a: {Joaquin.especialidad}")