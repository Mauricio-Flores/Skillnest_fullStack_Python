#Ejercicio N°1
def ejercicio1():
    n = int(input("¿Cuantos números deseas ver?: "))
    pares = []
    for i in range(1, ( n * 2 )+ 1):
        if i % 2 == 0:
            pares.append(i)
    print(f"Mostrando pares: {pares}")

#Ejercicio N°2
def ejercicio2():
    edad = int(input("Ingresa tu edad: "))
    if edad > 17:
        print("Eres mayor de edad. ")
    else:
        print("Eres menor de edad")

#Ejercicio N°3
def ejercicio3():
    descuento = 0
    total = 0
    pagar = int(input("Ingresa el valor del producto: "))
    cantidad = int(input("Ingresa la cantidad: "))
    pagar = pagar * cantidad
    if pagar >= 100:
        total = pagar * 0.85
        descuento = pagar * 0.15
        print(f"subTotal: {pagar}\ndescuento: -{descuento}\nTotal: {total}")
    else :
        print(f"total a pagar: {pagar}")

#Ejercicio N°4
def ejercicio4():
    n = int(input("Ingrsa un número: "))
    if n > 0:
        if n % 2 == 0:
            print("El número ingresado es positivo-par")
        else:
            print("El número ingresado es positivo-impar")
    elif n < 0:
        if n  % 2 == 0:
            print("El número ingresado es negativo-par")
        else:
            print("El número ingresado es negativo-impar")
    else: 
        print("El número ingresado es cero")

#Ejercicio N°5
def ejercicio5():
    n = int(input("Ingresa un número: "))
    for i in range(1, 13):
        resultado = n * i
        if resultado % 3 == 0:
            print(f"del {n} solo estos números son divisibles por 3: {resultado}")

#Ejercicio N°6
def ejercicio6():
    suma = 0
    while True:
        numero = int(input("Ingresa un número: "))
        if numero < 0:
            break
        suma += numero 
    print(f"La suma total es: {suma}")

#Ejercicio N°7
def ejercicio7():
    pal = input("Ingresa una frase o palabra: ")
    voc = 0
    for i in pal.lower():
        if i in "aeiouáéíóú":
            voc += 1
    print(f"En tu frase/palabra hay {voc} vocales.")

#Ejercicio N°8
def ejercicio8():
    con = "12345678"
    intentos = 1
    while True:
        ingresa = input("Ingresa la contraseña: ")
        if ingresa == con:
            print("Acceso concedido")
            break
        else:
            intentos += 1
            if intentos > 3:
                print("Acceso denegado.")
                break
            else:
                print(f"Numeros de intentos: {intentos}")

#Ejercicio N°9
def ejercicio9():
    arr = []
    nombreTotal = 0
    while True:
        ingresar = input("Ingresa 5 nombres: ")
        arr.append(ingresar)
        nombreTotal += 1
        if nombreTotal >= 5:
            arr = arr[::-1]
            print(arr)
            break

#Ejercicio N°10
def ejercicio10():
    cantidad = int(input("¿Cuántas notas deseas ingresar?: "))
    notas = []
    for i in range(cantidad):
        nota = float(input(f"nota {i+1}: "))
        notas.append(nota)
    promedio = sum(notas) / len(notas)
    print("\nResultados:")
    print(f"Promedio: {promedio}")
    print(f"Nota más alta: {max(notas)}")
    print(f"Nota más baja: {min(notas)}")

#Ejercicio N°11
def ejercicio11():
    cantidad = int(input("Cuantos números desea ingresar: "))
    mayor50 = []
    nUser = []
    for i in range(1, cantidad + 1):
        arrayUsuario = int(input("Ingrese número: "))
        if arrayUsuario > 50:
            mayor50.append(arrayUsuario)
        else:
            nUser.append(arrayUsuario)
    print(f"Valores ingresados por el usuario: {nUser} \nValores mayores a 50: {mayor50}")

#Ejercicio N°12
def ejercicio12():
    ciudades = ["santiago", "valparaíso", "concepción", "la serena", "antofagasta","temuco", "iquique", "puerto montt", "arica", "punta arenas"]
    buscar = input("Ingrese una ciudad: ")
    if buscar in ciudades:
        print(f"La ciudad está en la lista, en la posición {ciudades.index(buscar)}")
    else:
        print("La ciudad no se encuentra en la lista")

#Ejercicio N°13
def ejercicio13():
    pro = []
    pre = []
    for i in range(3):
        nom = input("Nombre del producto: ")
        pres = int(input("Precio: "))
        pro.append(nom)
        pre.append(pres)
    print("\nInvetario:")
    for i in range(3):
        print(f"Producto: {pro[i]} - Precio: {pre[i]}")

#Ejercicio N°14
def ejercicio14():
    lista = []
    while True: 
        item = input("Agrega un articulo (Ingresa `terminar` para finalizar): ")
        if item.lower() == "terminar":
            break
        lista.append(item)
    lista.sort()
    print(f"Lista ordenada: {lista}")

#Ejercicio N°15
def ejercicio15():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    temps = []
    for dia in dias:
        temp = int(input(f"Temperatura del {dia}: "))
        temps.append(temp)
    promedio = sum(temps) / len(temps)
    mayores_25 = len([t for t in temps if t > 25])
    min_temp = min(temps)
    dia_min = dias[temps.index(min_temp)]

    print(f"Promedio semanal: {promedio}")
    print(f"Dias sobre 25°: {mayores_25}")
    print(f"Dia mas frio: {dia_min} ({min_temp}°C)") 

continuar = True
while continuar:
    print("\n ejercicio python: ")
    print("--- 1.- Ejercicio  1 ---:")
    print("--- 2.- Ejercicio  2 ---:")
    print("--- 3.- Ejercicio  3 ---:")
    print("--- 4.- Ejercicio  4 ---:")
    print("--- 5.- Ejercicio  5 ---:")
    print("--- 6.- Ejercicio  6 ---:")
    print("--- 7.- Ejercicio  7 ---:")
    print("--- 8.- Ejercicio  8 ---:")
    print("--- 9.- Ejercicio  9 ---:")
    print("--- 10.- Ejercicio  10: ---")
    print("--- 11.- Ejercicio  11: ---")
    print("--- 12.- Ejercicio  12: ---")
    print("--- 13.- Ejercicio  13: ---")
    print("--- 14.- Ejercicio  14: ---")
    print("--- 15.- Ejercicio  15: ---")
    opcion = input("\n--- Elige una opción: (1:15) (0 para salir)")
    if opcion == "1":
        print("\nEjecutando ejercicio 1: ")
        ejercicio1()
    elif opcion == "2":
        print("\nEjecutando ejercicio 2: ")
        ejercicio2()
    elif opcion == "3":
        print("\nEjecutando ejercicio 3: ")
        ejercicio3()
    elif opcion == "4":
        print("\nEjecutando ejercicio 4: ")
        ejercicio4()
    elif opcion == "5":
        print("\nEjecutando ejercicio 5: ")
        ejercicio5()
    elif opcion == "6":
        print("\nEjecutando ejercicio 6: ")
        ejercicio6()
    elif opcion == "7":
        print("\nEjecutando ejercicio 7: ")
        ejercicio7()
    elif opcion == "8":
        print("\nEjecutando ejercicio 8: ")
        ejercicio8()
    elif opcion == "9":
        print("\nEjecutando ejercicio 9: ")
        ejercicio9()
    elif opcion == "10":
        print("\nEjecutando ejercicio 10: ")
        ejercicio10()
    elif opcion == "11":
        print("\nEjecutando ejercicio 11: ")
        ejercicio11()
    elif opcion == "12":
        print("\nEjecutando ejercicio 12: ")
        ejercicio12()
    elif opcion == "13":
        print("\nEjecutando ejercicio 13: ")
        ejercicio13()
    elif opcion == "14":
        print("\nEjecutando ejercicio 14: ")
        ejercicio14()
    elif opcion == "15":
        print("\nEjecutando ejercicio 15: ")
        ejercicio15()
    elif opcion == "0":
        print("Saliendo...")
        continuar = False