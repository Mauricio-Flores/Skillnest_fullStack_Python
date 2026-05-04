import os
def limpiar_consola():
    os.system('cls')

# Reciba una lista de números enteros y muestre cuál es el número mayor y cuál es el menor.
def menorMayor(lista):
    mayor = 0
    menor = 1000000000000000000000000
    
    for i in range(len(lista)):
        if lista[i] > mayor:
            mayor = lista[i]
        if lista[i] < menor:
            menor = lista[i]
        else:
            pass
    return f'El numero mayor de la lista: {lista} es el {mayor} y el menor es el {menor}'

# Reciba una cadena de texto y cuente cuántas vocales contiene.
def cadena(oka):
    texto = oka.lower()
    vocal = 0
    tildes = 0
    for i in texto:
        if i == "a" or i == "e" or i == "i" or i == "o" or i == "u":
            vocal += 1
        elif i == "á" or i == "é" or i == "í" or i == "ó" or i == "ú":
            tildes += 1
        else:
            pass
    return f'El  texto tiene {vocal + tildes} vocales, de las cuales {tildes} llevan tildes'

# Reciba una lista de nombres y muestre únicamente aquellos que tengan más de 5 letras.
def nombre(cadena):
    pasan = []
    for i in range(len(cadena)):
        if len(cadena[i]) > 5:
            pasan.append(cadena[i])
        else:
            pass
    
    return f'Los nombres que pasan son: {" ♥︎ ".join(pasan)}'

# Reciba una lista de notas (números decimales), calcule el promedio e indique si el estudiante aprueba (promedio mayor o igual a 4.0).
def decimales(notas):
    prom = 0
    for i in range(len(notas)):
            prom += notas[i]
            
    promedio = prom / (len(notas))
    if promedio >= 4.0 and promedio <= 7.0:
        print(f"➢ El estudiante pasa con un promedio de {promedio}")
    elif promedio < 4.0 and promedio >= 1.0:
        print(f"➢ El estudiante lamentablemente no pasa con un promedio de {promedio} ☹")

# Reciba una lista de precios de productos y aplique un descuento del 10%, mostrando el valor original y el nuevo valor.
def desc(num):
    return num * 0.9

def productos(mercado):
    precio = []
    for i in range(len(mercado)):
        precio.append(desc(mercado[i]))
    
    for i in range(len(mercado)):
        print(f"El antigo precio es de {mercado[i]} y el nuevo es de {precio[i]}")

# Reciba un número entero y determine si es par o impar.
def im(num):
    if num == "" or type(num) != str:
        if num % 2 == 0:
            print(f"El {num} es par ദ്ദി ˉ͈̀꒳ˉ͈́ )✧")
        else:
            print(f"El {num} es impar /ᐠ • ˕ •マ ?")
    else:
        print("Por favor ingresar elemento válido")

# Reciba una lista de edades y muestre cuántas personas son mayores de edad (18 años o más).
def edades(personas):
    mayores = 0 
    for i in range(len(personas)):
        if personas[i] >= 18:
            mayores += 1
    return f"Hay {mayores} personas mayores"

# Reciba una lista de palabras y permita buscar cuántas veces aparece una palabra específica ingresada por el usuario.
def palabras(oka):
    noPuedeSer = {}
    for i in range(len(oka)):
        cantVeces = 0
        for f in range(len(oka)):
            if oka[i] == oka[f]:
                cantVeces += 1
        noPuedeSer[oka[i]] = cantVeces
    return noPuedeSer

# Reciba una lista de números y genere una nueva lista que contenga únicamente los números positivos.
def exclusion(justiciaParaLosNegativos):
    discriminadores = []
    for i in range(len(justiciaParaLosNegativos)):
        if justiciaParaLosNegativos[i] >= 0:
            discriminadores.append(justiciaParaLosNegativos[i])
    return discriminadores

# Reciba una lista de productos (utilizando diccionarios con nombre y stock) y muestre cuáles tienen un stock menor a 5 unidades.
def stockcio(pelusas):
    for prod, cant in pelusas.items():
        if cant < 5:
            print(f"¡ALERTA! el producto {prod} tiene muy poco stock({cant})")

# 合 Menu ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
sueño = False
print("Bienvenido Python!! Que deseas ver hoy?")

while not sueño:
    inp = int(input("\nPor favor elegir ejercicio(1 - 10, 0 = salir):_"))

# EJERCICIO UNO
    if inp == 1:
        limpiar_consola()
        print("LLevando al ejercicio uno \n ❝ Mayor y menor ❞")
        arreglo = []
        put = int(input("Cuantos numeros deseas ingresar?:_"))
        for i in range(put):
            num = int(input("≫"))
            arreglo.append(num)
        print(menorMayor(arreglo))
# EJERCICIO DOS
    elif inp == 2:
        limpiar_consola()
        print("LLevando al ejercicio dos \n ❝ Cantidad de vocales ❞")
        text = input("Qué vas a escribir hoy?:_")
        print(cadena(text))
# EJERCICIO TRES
    elif inp == 3:
        limpiar_consola()
        print("LLevando al ejercicio tres \n ❝ Nombres con mas de 5 Letras ❞")
        arreglo = []
        put = int(input("Cuantos nombres deseas ingresar?:_"))
        for i in range(put):
            nombres = input("≫")
            arreglo.append(nombres)
        print(nombre(arreglo))
# EJERCICIO CUATRO
    elif inp == 4:
        limpiar_consola()
        print("LLevando al ejercicio cuatro \n ❝ Notas y promedios ❞")
        arreglo = []
        put = int(input("Cuantas notas deseas ingresar?:_"))
        for i in range(put):
            num = float(input("≫"))
            arreglo.append(num)
        print(decimales(arreglo))
# EJERCICIO CINCO
    elif inp == 5:
        limpiar_consola()
        print("LLevando al ejercicio cinco \n ❝ Productos con descuentos ❞")
        arreglo = []
        put = int(input("Cuantas vale tu producto?:_"))
        for i in range(put):
            num = int(input("≫"))
            arreglo.append(num)
        print(productos(arreglo))
# EJERCICIO SEIS
    elif inp == 6:
        limpiar_consola()
        print("LLevando al ejercicio seis \n ❝ Par o Impar ❞")
        numero = int(input("Ingresa un numero para saber si es par o impar:_"))
        print(im(numero))
# EJERCICIO SIETE
    elif inp == 7:
        limpiar_consola()
        print("LLevando al ejercicio siete \n ❝ Mayores de edad ❞")
        arreglo = []
        put = int(input("Ingresar edades:_"))
        for i in range(put):
            num = int(input("≫"))
            arreglo.append(num)
        print(edades(arreglo))
    elif inp == 8:
# EJERCICIO OCHO
        limpiar_consola()
        print("LLevando al ejercicio ocho \n ❝ Cuantas veces aparece una palabra ❞")
        arreglo = []
        put = int(input("Cuantos elementos deseas ingresar?:_"))
        for i in range(put):
            cosa = input("≫")
            arreglo.append(cosa)
        print(palabras(arreglo))
    elif inp == 9:
# EJERCICIO NUEVE
        limpiar_consola()
        print("LLevando al ejercicio nueve \n ❝ Discriminadores de negativos ❞")
        arreglo = []
        put = int(input("Cuantos números vas a ingresar?:_"))
        for i in range(put):
            num = int(input("≫"))
            arreglo.append(num)
        print(exclusion(arreglo))
# EJERCICIO DIEZ
    elif inp == 10:
        limpiar_consola()
        print("LLevando al ejercicio diez \n ❝ Stock ❞")
        diccionario = {}
        put = int(input("Cuantos elementos vas a ingresar?:_"))
        for i in range(put):
            clave = input("Ingresa elemnto:_")
            valor = int(input("Ingresa valor:_"))
            diccionario[clave] = valor
        print(stockcio(diccionario))
    elif inp == 0:
        limpiar_consola()
        print("Saliendo𓍯𓂃𓏧♡")
        sueño = True
    else:
        print("ඞඞඞඞඞඞඞඞඞඞ")