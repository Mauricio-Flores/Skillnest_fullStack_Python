import time
import sys
def carga():
    an = ["/", "-", "\\"]
    for i in range(20):
        print(f"\rCargando {an[i % len(an)]}", end="")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\rPrograma cargado con exito")
carga()
## Atributos, metodos de clase. métodos estáticos

## Definición de la clase
class Estudiantes: 
    # Atributos de la clase
    colegio  = "Liceo Comercial Vate Vicente Huidobro"
    # Lista en donde esten todos los estudiantes
    estudiantes = []

    # Metodo CONSTRCUTOR 
    def __init__(self, nombre, nota):
        #Atributos de instancia
        self.nombre = nombre
        self.nota = nota

        # Agregar elemento a lista de estudiante (objeto)
        Estudiantes.estudiantes.append(self)

    # Metodo de instancia
    def mostrar_info(self):
        print(f"Nombre: {self.nombre}")
        print(f"Nota: {self.nota}")
    
    # Método de CLASE 
    # Usa "cls" porque trabaja con la información de la clase
    @classmethod
    def cambiar_colegio(cls, nuevo_nombre):
        cls.colegiob = nuevo_nombre

    @classmethod #Contar la cantidad de estudiantes existemtes
    def cantidad_estudiantes(cls):
        return len(cls.estudiantes)

    #Metodo estático
    #Este eno usa CLS ni SELF, solo parametors.
    @staticmethod
    def probar(nota):
        if nota >= 4:
            return True
        else:
            return False
            
# Creación de objetos (Instancias)
e1 = Estudiantes("Donovan", 4.0)
e2 = Estudiantes("RandyGod", 6.7)
# Uso de metodos de instancias
print("== MÉTODO DE INSTANCIAS ==")
# Mostrar datos del estudiante
e1.mostrar_info()
print()
e2.mostrar_info()
print()
#Usar atributo de clase
print("===  ===")
print(e1.colegio)
print(e2.colegio)
print()

# Uso de método de clase
print("=== MÉTODO DE CLASE ===")

Estudiantes.cambiar_colegio("Purkuyen")
e1.colegio = "VVH"
print(e1.colegio)
print(e2.colegio)
print()

#Contar estudiantes 
print("=== CONTAR ESTUDIANTES ===")
print(f"Total estudiantes: {Estudiantes.cantidad_estudiantes()}")

# Método estatico 
print("=== MÉTODO ESTATICO ===")

print(f"¿{e1.nombre} aprueba?")
print(Estudiantes.aprobar)

## Función repaso
## Crear una función que valide usuario y contraseña

def validador(user, password):
    if user == "matias123" and password == "matias123":
        print(f"Bienvenido, {user}!")
        return True
    elif password == "matias123":
        print("Esa contraseña le pertenece a matias123")
        return False
    else:
        print("Acceso denegado")
        return False

def enviarDatos():
    userName = input("Ingrese su usuario: ")    
    password = input("Ingrese su contraseña: ")
    validador(userName, password)
enviarDatos()