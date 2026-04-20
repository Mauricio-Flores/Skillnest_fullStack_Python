'''
Actividad: Gestor de inventario
1.- Creación: Crear una lista llamada inventario que contenga los siguientes articulos: "laptop", "ratón", "cable hdmi".
'''

inventario = ["laptop", "ratón", "monitor", "cable hdmi"]

'''
2.- Expansión utiliza el método correspondiente para agregar "impresora" y "teclado" al final de la lista.
'''
inventario.append("impresora")
inventario.append("teclado")
'''
3.- Conteo: Utiliza la función integrada para mostrar cuantos elementos totales hay en la lista.
'''
print(len(inventario))
'''
4.- Acceso y modificación: Modifica "teclado" por "teclado mecanico"
'''
inventario[5] = "teclado mecanico"
print(inventario)
'''
5.- Slicing: Crea una nueva lista llamada "promoción", debe contener solo los 3 primeros elementos de la lista "inventario".
'''
promocion = inventario[0:3]
print(promocion)
'''
6.- Mostrar la lista de inventario ordenado alfabeticamente
'''
inventario.sort()
print(inventario)
'''
7.- Elimina el último elemento de la lista inventario mostrando el elemento eliminado y la lista final
'''
articuloEliminado = inventario.pop()
print(articuloEliminado)
print(inventario)