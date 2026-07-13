from flask import Flask  # Importa Flask para permitirnos crear nuestra aplicación

app = Flask(__name__)    # Crea una nueva instancia de la clase Flask llamada "app"

@app.route('/')          # El decorador "@" asocia esta ruta con la función inmediatamente siguiente

def hola_mundo():

   return '¡Hola Mundo! páginas <a href="nosotros">Nosotros</a> <a href="secundario">Secundario</a> <a href="tercero">Tercero</a>'  # Devuelve la cadena '¡Hola Mundo!' como respuesta
#-----------------------------------------------------

@app.route('/nosotros')         

def nosotros():

   return '¡Conocenos un poco más!'  
#----------------------------------------------------
@app.route('/secundario')         

def secundario():

   return '¡Vienvenido secundario! <a href="nosotros">Nosotros</a>'  
#-------------------------------------------------------------
@app.route('/tercero')         

def tercero():

   return '¡<a href="/">Inicio</a>!'  

if __name__=="__main__":   # Asegúrate de que este archivo se esté ejecutando directamente y no desde un módulo diferente   

   app.run(debug=True)    # Ejecuta la aplicación en modo de depuración/debug para detectar cualquier cambio y recargarlo