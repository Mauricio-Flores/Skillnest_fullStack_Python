from flask import flash, redirect, render_template, request, session

from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario


@app.route("/")
def inicio():
    if "usuario_id" in session:
        return redirect("/exito")
    return render_template("index.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect("/")

    password_encriptada = bcrypt.generate_password_hash(
        request.form["password"]
    ).decode("utf-8")

    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": password_encriptada,
    }

    usuario_id = Usuario.guardar(datos)
    if not usuario_id:
        flash("No se pudo completar el registro. Inténtalo nuevamente.", "registro")
        return redirect("/")

    session["usuario_id"] = usuario_id
    return redirect("/exito")


@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    email = request.form.get("email_login", "").strip().lower()
    password = request.form.get("password_login", "")

    if not email or not password:
        flash("Completa el correo y la contraseña.", "login")
        return redirect("/")

    usuario = Usuario.obtener_por_email({"email": email})

    if usuario is None or not bcrypt.check_password_hash(usuario.password, password):
        flash("El correo o la contraseña son incorrectos.", "login")
        return redirect("/")

    session["usuario_id"] = usuario.id
    return redirect("/exito")


@app.route("/exito")
def exito():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para ingresar.", "login")
        return redirect("/")

    usuario = Usuario.obtener_por_id({"id": session["usuario_id"]})
    if usuario is None:
        session.clear()
        return redirect("/")

    return render_template("exito.html", usuario=usuario)


@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/")
