# Función ne python
def multiplicar(num1, num2): #Definimos la función múltiplicación con los parametros
    resultado = num1 * num2 #instrucciones dentro de la función
    return resultado #Regresamos valor de resultado

a = int(input("Ingrese primer número."))
b = int(input("Ingrese segundo número"))
re_mu = multiplicar(a, b)
#LLamado a la función con argumentos 5 y 5
print(re_mu)
#Se guarda en la variable el resultado que la función regréso. Imprime: 25

def buenos_dias(nombre):
    print("Buenos dias " + nombre)

#Llamada a la función y asignación de valor a parámetro
buenos_dias("Alegría")
buenos_dias("al amor")
buenos_dias("a la vida")
buenos_dias("señor sol")

def buenos_dias2(nombre):
    return "Buenos días " + nombre

#El valor de retorno de la función es "Buenos días python", por lo que el valor de mi variable frase será ese

frase = buenos_dias2("Python")
print(frase)

#Ejercicio de retorno valor.
#Crear una función que reciba una frase + un parametro
#Devolver el valor de la frase completa e imprimir

def ejer_retorno(frase, palabra):
    return f"{frase} {palabra}"
            
def recibirFrase():
    frase = input("Ingrese una frase: ")
    palabra = input("Ingresa una palabra: ")
    resultadoFrase = ejer_retorno(frase, palabra)
    print(resultadoFrase)