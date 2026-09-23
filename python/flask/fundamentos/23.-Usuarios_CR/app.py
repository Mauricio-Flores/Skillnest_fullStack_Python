from flask import Flask, render_template, request, redirect, url_for
from usuario import Usuario

app = Flask(__name__)

@app.route("/usuarios")
def listar_usuarios():
def formulario_usuario():
    return render_template("usuario_nuevo.html")

@app.route("/usuarios/crear", methods=["POST"])
def guardar_usuario():
    datos = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"]
    }

    Usuario.crear(datos)

    return redirect(url_for("listar_usuarios"))

if __name__ == "__main__":
    app.run(debug=True)
