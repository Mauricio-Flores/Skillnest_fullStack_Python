from flask import Flask, render_template, request, redirect, url_for
from usuario import Usuario

app = Flask(__name__)

@app.route("/usuarios")
def mostrar_usuarios():
    lista = Usuario.listar()
    return render_template("usuarios.html", usuarios=lista)

@app.route("/usuarios/nuevo")
def nuevo():
    return render_template("usuario_nuevo.html")

@app.route("/usuarios/guardar", methods=["POST"])
def guardar():
    datos = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"]
    }

    Usuario.crear(datos)

    return redirect(url_for("mostrar_usuarios"))


if __name__ == "__main__":
    app.run(debug=True)
