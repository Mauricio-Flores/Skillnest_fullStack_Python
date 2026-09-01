from flask import Flask, render_template, request, redirect

app = Flask(__name__)
@app.route("/")
def index():
    """
    Muestra el formulario de creación de usuario.
    """
    return render_template("index.html")
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Recibe la información enviada mediante POST.
    Esta función se encarga de procesar los datos
    antes de realizar la redirección.
    """
    nombre = request.form["nombre"]
    email = request.form["email"]
    print("===================================")
    print("Información recibida")
    print(f"Nombre: {nombre}")
    print(f"Email: {email}")
    print("===================================")
    return redirect("/mostrar_usuario")

@app.route("/mostrar_usuario")
def mostrar_usuario():
    """
    Esta ruta recibe una solicitud GET después
    de la redirección.
    """
    print("Usuario redirigido")
    print(request.form)
    return render_template("mostrar.html")

if __name__ == "__main__":
    app.run(debug=True)