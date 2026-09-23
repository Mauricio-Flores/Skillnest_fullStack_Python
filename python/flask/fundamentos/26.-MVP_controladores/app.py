from flask import Flask, render_template, request, redirect, url_for
from usuario import Usuario

app = Flask(__name__)


@app.route("/usuarios")
def inicio():
    usuarios = Usuario.listar()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/nuevo")
def nuevo_usuario():
    return render_template("nuevo.html")


@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    datos = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"]
    }

    Usuario.crear(datos)

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
