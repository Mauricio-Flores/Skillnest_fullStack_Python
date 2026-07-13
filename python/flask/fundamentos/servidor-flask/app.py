from flask import Flask
app = Flask(__name__)

# Ruta raíz - Página de inicio
@app.route('/') 

def inicio():
   return '¡Bienvenido a nuestro servidor Flask!'
# Ruta genérica para explorar enrutamiento
@app.route('/explorar')
def explorar():
   return '🔍 ¿Qué ruta estás buscando? ¡Prueba con diferentes direcciones!'
# Rutas dinámicas para personalización
@app.route('/perfil/<nombre>')
def usuario(nombre): 
   return f'Bienvenid@ {nombre} a tu perfil personalizado en nuestra app.'
# Ruta que repite un mensaje varias veces
@app.route('/repite/<int:veces>/<mensaje>')
def repetir_mensaje(veces, mensaje):
   return (mensaje + " ") * veces
# BONUS: Página de error personalizada si el usuario ingresa una ruta inexistente
@app.errorhandler(404)
def pagina_no_encontrada(error):
    # Devolvemos el mensaje personalizado y el código de estado 404
    return "¡Sobrecarga de rutas! No encontramos a dónde quieres ir, inténtalo de nuevo.", 404
# Ejecuta el servidor
if __name__ == "__main__":
    app.run(debug=True)