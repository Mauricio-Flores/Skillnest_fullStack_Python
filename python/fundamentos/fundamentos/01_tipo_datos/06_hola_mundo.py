# hola_mundo.py (Versión SIN respuestas)


# 1. Imprime "Hola, mundo"
#    Reemplaza el comentario con el código necesario para que, al ejecutar,
#    aparezca en pantalla la frase "Hola, mundo".
#    Ejemplo de uso: print("Mensaje")
# ---------------------------------------------------------------
print("Hola, mundo")
print()




# 2. Imprime "Hola, Valeria" con el nombre en una variable
#    a) Concatenación usando comas
#    b) Concatenación usando +
# ---------------------------------------------------------------
nombre = "Valeria"

# a) Usando comas
print("Hola", nombre)


# b) Usando +
print("Hola, " + nombre)
print()
# 3. Imprime "Hola 156!" con el número en una variable
#    a) Usando comas
#    b) Usando + (esto podría dar error si no conviertes el número a str)
# ---------------------------------------------------------------
numero = 156


# a) Usando comas
print("Hola", numero)


# b) Usando +
print("Hola, " + str(numero))
print()
# BONUS: Corrige el error con conversión de tipos si aparece.




# 4. Imprime "Me encanta comer X e Y" con dos de tus comidas favoritas
#    a) Usando .format()
#    b) Usando f-strings
# ---------------------------------------------------------------
comida1 = "pizza"
comida2 = "hamburguesa"


# a) Con .format()
print("Me encanta comer {} y {}.".format(comida1, comida2))


# b) Con f-string
print(f"Me encanta comer {comida1} y {comida2}.")
print()



# Desafío bonus: Usa al menos un método de cadena adicional.
# Ejemplo: .upper(), .lower(), .replace(), etc.
# ---------------------------------------------------------------