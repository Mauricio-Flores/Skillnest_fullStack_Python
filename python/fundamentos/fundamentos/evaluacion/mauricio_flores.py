import time
import sys
def carga():
    an = ["/", "-", "\\"]
    for i in range(20):
        print(f"\rCargando {an[i % len(an)]}", end="")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\rPrograma cargado con exito")
import os
def limpiarConsola():
    os.system('cls')
#Crear una función que reciba una lista de edades y clasifique a las personas en tres grupos: menores de edad, adultos y adultos mayores (60+).
#Debe mostrar la cantidad de personas en cada grupo.
# Ejercicio N°1 ---------------------------------------------------------------- Mauricio Flores
def clasificacionEdades(edad):
    adultoMayor = 0
    adultos = 0
    menorEdad = 0
    valoresInvalidos = 0
    for i in range(len(edad)):
        if edad[i] == "":
            pass
        elif edad[i] >= 0 and edad[i] < 18:
            menorEdad += 1
        elif edad[i] >= 18 and edad[i] < 60:
            adultos += 1
        elif edad[i] >= 60 and edad[i] < 120:
            adultoMayor += 1
        else: 
            valoresInvalidos += 1
    return f"Total edades: {edad}\nAdultos mayores: {adultoMayor}\nAdultos: {adultos}\nMenores de edad: {menorEdad}\nVampiros: {valoresInvalidos}"

def ingresarDatos():
    edades = []
    lim = input("¿Cuantas edades quieres ingresar?\n>")
    if lim == "":
        limpiarConsola()
        print("Ingresa un valor valido.")
    else:
        if lim.isdigit():
            limpiarConsola()
            limite = int(lim)
            for i in range(limite):
                edad = input(f"{i + 1}>>> ")
                if edad == "":
                    print("Valor invalido")
                    continue
                else:
                    if edad.isdigit():
                        Edad = int(edad)
                        edades.append(Edad)
                    else:
                        print("Valor invalido")
                        continue
            carga()
            print(clasificacionEdades(edades))
        else:
            limpiarConsola()
            print("Ingresa un valor valido")
# Ejercicio N°2 ---------------------------------------------------------------- Martin Acevedo
def numerosPares(lista):
    # Inicia con una lista vacía para almacenar los números pares
    numero = []
    # bucle sobre la lista de números
    for i in range(len(lista)):
        # Verifica si el número es par y mayor a 10
        if lista[i] % 2 == 0 and lista[i] > 10:
            # Agrega el número a la lista de números pares
            numero.append(lista[i])
    # Devuelve la lista de números pares
    return numero


#Listo 
# Función que llama a la función numerosPares y imprime el resultado
def ejercicio2():
    lista = []
    num_elementos = int(input("Ingrese la cantidad de números que desea ingresar: "))
    for i in range(num_elementos):
        num = int(input(f"Ingrese el número {i+1}: "))
        lista.append(num)
    nuevaLista = numerosPares(lista)
    print(nuevaLista)
    print(f"La cantidad de elementos encontrados en la lista es: {len(nuevaLista)}")
# Llama a la función ejercicio2

menu = False
while not menu:
    carga()
    nn = input("Elegir ejercicio (1 - 2) 0 para salir \n")
    if nn == "":
        limpiarConsola()
        print("Ingresa un valor valido")
    else:
        if nn.isdigit():
            n = int(nn)
            if n == 1:
                limpiarConsola()
                carga()
                print("Ejercicio N°1\n")
                ingresarDatos()
            elif n == 2:
                limpiarConsola()
                carga()
                print("Ejercicio N°2\n")
                ejercicio2()
            elif n == 0:
                limpiarConsola()
                print("Saliendo . . .")
                menu = True
            else:
                limpiarConsola()
                print("Ingresa un dato correcto")
        else:
            limpiarConsola()
            print("Ingresa un valor valido")