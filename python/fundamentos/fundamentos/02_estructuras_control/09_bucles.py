for i in range(4):
   print(i)
   
for i in range(2, 8):
   print(i)

for i in range(0, 15, 3):
   print(i)
#Imprime: 0, 3, 6, 9, 12

for i in range(10, 1, -3):
   print(i)
#Imprime: 10, 7, 4

for letra in 'Python':
   print(letra)
#Imprime: 'P', 'y', 't', 'h', 'o', 'n'

lista = ['brócoli', 'pepino', 'pimiento']

for i in range( len(lista) ):
   print(i, lista[i])
#Imprime: 0 brócoli, 1 pepino, 2 pimiento

for verdura in lista:
   print(verdura)
#Imprime: brócoli, pepino, pimiento

tupla = ('fresa', 'manzana', 'cereza')

for i in range( len(tupla) ):
   print(i, tupla[i])
#Imprime: 0 fresa, 1 manzana, 2 cereza

for fruta in tupla:
   print(fruta)
#Imprime: fresa, manzana, cereza

estudiante = {"nombre": "Gonzalo", "curso": "Python"}

for clave in estudiante:
   print(clave)
#Imprime: nombre, curso

estudiante = {"nombre": "Gonzalo", "curso": "Python"}

for clave in estudiante:
   print(estudiante[clave])
#Imprime: Gonzalo, Python

platillos_tipicos = {"México": "Tacos", "Colombia": "Ajiaco", "Costa Rica": "Casado"}

#Otra forma de iterar a través de las claves
for clave in platillos_tipicos.keys():
   print(clave)
#Imprime: México, Colombia, Costa Rica

#Iteramos a través de los valores
for valor in platillos_tipicos.values():
   print(valor)
#Imprime: Tacos, Ajiaco, Casado

#Iteramos a través de los elementos (clave-valor)
for clave, valor in platillos_tipicos.items():
   print(clave, "=", valor)
#Imprime: México = Tacos, Colombia = Ajiaco, Costa Rica = Casado