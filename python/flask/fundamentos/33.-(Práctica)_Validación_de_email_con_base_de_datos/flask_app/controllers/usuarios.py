from flask import flash, redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.usuario import RegistroUsuario


@app.get("/")
def inicio():
    return redirect(url_for("usuarios"))


@app.get("/usuarios")
def usuarios():
    return render_template("usuarios.html", usuarios=RegistroUsuario.obtener_todos())


@app.get("/usuarios/nuevo")
def nuevo_usuario():
    return render_template("nuevo_usuario.html")


@app.post("/usuarios/crear")
def crear_usuario():
    values = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
    }

    if not RegistroUsuario.validar_datos(values):
        return redirect(url_for("nuevo_usuario"))

    if RegistroUsuario.crear(values) is False:
        flash("No fue posible crear el usuario.", "error")
        return redirect(url_for("nuevo_usuario"))

    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("usuarios"))
