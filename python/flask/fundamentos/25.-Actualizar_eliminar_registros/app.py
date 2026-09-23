from flask import Flask, render_template, request, redirect, url_for
from usuario import Usuario

app = Flask(__name__)

@app.route("/usuarios")
def lista():
    usuarios = Usuario.listar()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/ver/<int:id>")
def ver(id):
    usuario = Usuario.buscar(id)
    return render_template("usuario.html", usuario=usuario)

@app.route("/usuarios/editar/<int:id>")
def editar(id):
    usuario = Usuario.buscar(id)
    return render_template("editar.html", usuario=usuario)

@app.route("/usuarios/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    datos = {
        "id": id,
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"]
    }
    Usuario.actualizar(datos)
    return redirect(url_for("lista"))

@app.route("/usuarios/eliminar/<int:id>")
def eliminar(id):
    Usuario.eliminar(id)
    return redirect(url_for("lista"))

if __name__ == "__main__":
    app.run(debug=True)
