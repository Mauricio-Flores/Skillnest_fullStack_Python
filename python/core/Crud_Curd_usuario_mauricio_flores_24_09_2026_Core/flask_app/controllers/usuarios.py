from flask import redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.usuario import Usuario


@app.route("/")
def inicio():
    return redirect(url_for("usuarios"))


@app.route("/usuarios")
def usuarios():
    personas = Usuario.get_all()
    return render_template("index.html", usuarios=personas)


@app.route("/usuarios/nuevo")
def nuevo():
    return render_template("nuevo.html")


@app.route("/usuarios/crear", methods=["POST"])
def crear():
    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip(),
    }

    if not datos["nombre"] or not datos["apellido"] or not datos["email"]:
        return render_template("nuevo.html", error="Todos los campos son obligatorios.", datos=datos)

    respuesta = Usuario.save(datos)

    if respuesta is False:
        return render_template("nuevo.html", error="No fue posible crear el usuario.", datos=datos)

    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:id>")
def detalle(id):
    persona = Usuario.get_by_id(id)

    if persona is None:
        return "Usuario no encontrado", 404

    return render_template("detalle.html", usuario=persona)


@app.route("/usuarios/editar/<int:id>")
def editar(id):
    persona = Usuario.get_by_id(id)

    if persona is None:
        return "Usuario no encontrado", 404

    return render_template("editar.html", usuario=persona)


@app.route("/usuarios/<int:id>/actualizar", methods=["POST"])
def actualizar(id):
    datos = {
        "id": id,
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip(),
    }

    if not datos["nombre"] or not datos["apellido"] or not datos["email"]:
        persona = Usuario.get_by_id(id)
        return render_template("editar.html", usuario=persona, error="Todos los campos son obligatorios.")

    respuesta = Usuario.update(datos)

    if respuesta is False:
        persona = Usuario.get_by_id(id)
        return render_template("editar.html", usuario=persona, error="No fue posible actualizar el usuario.")

    return redirect(url_for("usuarios"))


@app.route("/usuarios/borrar/<int:id>")
def borrar(id):
    respuesta = Usuario.delete({"id": id})

    if respuesta is False:
        return "No fue posible eliminar el usuario.", 500

    return redirect(url_for("usuarios"))
