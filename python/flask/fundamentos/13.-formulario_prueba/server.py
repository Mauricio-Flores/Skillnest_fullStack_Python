# Importamos Flask para crear la aplicación,
# render_template para cargar archivos HTML,
# request para acceder a los datos enviados por el usuario
# y redirect para redirigir a otra URL.
from flask import Flask, render_template, request, redirect


# Creamos una aplicación Flask.
# __name__ le indica a Flask dónde se encuentra nuestra aplicación.
app = Flask(__name__)


# @app.route("/") indica que esta función se ejecutará
# cuando el usuario entre en la página principal "/".
@app.route("/")
def index():

    # Buscamos el archivo index.html dentro de la carpeta "templates"
    # y se lo enviamos al navegador.
    return render_template("index.html")


# Esta ruta responde a /crear_usuario.
# methods=["POST"] significa que esta dirección solamente
# acepta peticiones HTTP de tipo POST.
# Normalmente esta ruta será utilizada por un formulario.
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    # request.form contiene los datos enviados
    # mediante un formulario HTML usando POST.
    #
    # Aquí buscamos el campo cuyo atributo "name" sea "nombre".
    nombre = request.form["nombre"]


    # Obtenemos el campo "email" del formulario.
    email = request.form["email"]


    # Imprimimos una línea para separar la información
    # en la consola.
    print("===========================")


    # Mostramos un mensaje en la consola.
    print("Información recibida")


    # Mostramos el nombre recibido.
    # La f delante del texto permite insertar
    # el valor de la variable dentro del texto.
    print(f"Nombre: {nombre}")


    # Mostramos el email recibido.
    print(f"Email: {email}")


    # Otra línea para separar la información.
    print("===========================")


    # Redirigimos al usuario hacia /mostrar_usuario.
    return redirect("/mostrar_usuario")


# Creamos otra ruta.
#
# Cuando el usuario visite /mostrar_usuario,
# se ejecutará esta función.
@app.route("/mostrar_usuario")
def mostrar_usuario():

    # Mostramos un mensaje en la consola.
    print("Usuario redirigido")


    # Mostramos los datos que contiene request.form.
    print(request.form)


    # Cargamos mostrar.html desde la carpeta templates.
    return render_template("mostrar.html")


# Esta condición comprueba si este archivo Python
# se está ejecutando directamente.
#
# Si ejecutamos:
# python app.py
#
# __name__ tendrá el valor "__main__".
if __name__ == "__main__":

    # Iniciamos el servidor de Flask.
    #
    # debug=True activa el modo de depuración:
    # - muestra errores más detallados
    # - reinicia automáticamente el servidor
    #   cuando modificamos el código.
    app.run(debug=True)
