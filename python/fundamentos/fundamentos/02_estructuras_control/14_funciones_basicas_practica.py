import os
#Ejercicio 1
# Calcula experiencia
def multiplica_por_2(num):
    result = []
    for i in range(num + 1):
        result.append(i * 2)
    return result
def resultado1():
    result1 = multiplica_por_2(5)
    print(result1)
# Debe retornar: [0, 2, 4, 6, 8, 10]

#Ejercicio 2
# Analiza publicaciones
def suma_y_resta(num):
    suma = num[0] + num[1]
    print(suma)
    resta = num[0] - num[1]
    return resta
def resultado2():
    result2 = suma_y_resta([120, 115])
    print(result2)

# Imprime: 235 y retorna: 5

#Ejercicio 3
# Puntaje ajustado
def sumatoria_menos_longitud(num):
    suma = sum(num)
    print(f"Suma total: {suma}")
    long = len(num)
    print(f"Longitud: {long}")
    return suma - long
def resultado3():
    result3 = sumatoria_menos_longitud([10, 5, 3, 7])
    print(f"Retorno: {result3}")
# Suma total = 25, longitud = 4, debe retornar: 21

#Ejercicio 4
# Ajusta visualizaciones
def valores_multiplicados_segundo(lista):
    if len(lista) < 2:
        print(len(lista))
        return []
    else:
        segEle = lista[1]
        nuevaLista = []
        for i in lista:
            nuevaLista.append(i * segEle)
        long = len(nuevaLista)
        print(long)
        return nuevaLista 
     
def resultado4():
    result4 = valores_multiplicados_segundo([100, 3, 50, 20])
    print(result4)
    # Imprime: 4 y retorna: [300, 9, 150, 60]
    print()
    print(valores_multiplicados_segundo([100]))
    # Imprime: 1 y retorna: []

#Ejercicio 5
# Genera precio fijo
def valor_multiplicado_longitud(valor, longitud):
    lista = []
    for i in range(longitud):
        lista.append(valor * longitud)
    return lista
def resultado5():
    print(valor_multiplicado_longitud(5, 2))
    # Debe retornar: [10, 10]

    print(valor_multiplicado_longitud(7, 5))
    # Debe retornar: [35, 35, 35, 35, 35]

def limpiarConsola():
    os.system('cls')

continuar = True
while continuar:
    print("\n ejercicio python: ")
    print("--- 1.- Ejercicio  1 ---:")
    print("--- 2.- Ejercicio  2 ---:")
    print("--- 3.- Ejercicio  3 ---:")
    print("--- 4.- Ejercicio  4 ---:")
    print("--- 5.- Ejercicio  5 ---:")
    opcion = input("\n--- Elige una opción: (1:15) (0 para salir)")
    if opcion == "1":
        limpiarConsola()
        print("\nEjecutando ejercicio 1: ")
        resultado1()
    elif opcion == "2":
        limpiarConsola()
        print("\nEjecutando ejercicio 2: ")
        resultado2()
    elif opcion == "3":
        limpiarConsola()
        print("\nEjecutando ejercicio 3: ")
        resultado3()
    elif opcion == "4":
        limpiarConsola()
        print("\nEjecutando ejercicio 4: ")
        resultado4()
    elif opcion == "5":
        limpiarConsola()
        print("\nEjecutando ejercicio 5: ")
        resultado5()
    elif opcion == 0:
        limpiarConsola()
        print("Saliendo...")
        continuar = False
    else:
        print("Opcion no valida, intenta otra vez")