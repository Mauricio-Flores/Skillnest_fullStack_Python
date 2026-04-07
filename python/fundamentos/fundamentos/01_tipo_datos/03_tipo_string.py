# Concatenar 
print("Esta es una cadenas de caracteres.")

# Contactenar cadenas y variables
print("Esta es una cadenas de caracteres.")

print("Esta es una cadenas de caracteres.")

# Type casting
print("¿Cuántas vocales hay? " + 5) 
# ERROR: TypeError: can only concatenate str (not "int") to str
print("¿Cuántas vocales hay? " + str(5)) #Imprime: ¿Cuántas vocales hay? 5

# Conversión numerica
tiempo_preparacion = 1
tiempo_horneado = "2"
tiempo_total = tiempo_preparacion + tiempo_horneado 
#ERROR: TypeError: unsupported operand type(s) for +: 'int' and 'str'
tiempo_total = tiempo_preparacion + int(tiempo_horneado) #Imprime: 3

# Interpolación de cadenas literal
nombre = "Marcelo"
edad = 29
print(f"Mi nombre es {nombre} y tengo {edad} años de edad.")

# String.format
nombre = "Marcelo"
edad = 29
print("Mi nombre es {} y tengo {} años de edad.".format(nombre, edad))

#Imprime: Mi nombre es Marcelo y tengo 29 años de edad.
print("Tengo {} años de edad y mi nombre es {}".format(edad, nombre))

#Imprime: Tengo 29 años de edad y mi nombre es Marcelo

#Formatting 
nombre = "Marcelo"
edad = 29
print("Mi nombre es %s y tengo %d años de edad." % (nombre, edad))
#Imprime: Mi nombre es Marcelo y tengo 29 años de edad. 