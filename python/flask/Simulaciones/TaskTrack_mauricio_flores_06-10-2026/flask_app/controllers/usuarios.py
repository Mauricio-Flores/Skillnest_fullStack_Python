from flask import flash, redirect, render_template, request, session, url_for

from flask_app import app, bcrypt
from flask_app.helpers import login_requerido
from flask_app.models.tarea import Tarea
from flask_app.models.usuario import Usuario


@app.route("/")
def inicio():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("inicio.html", registro={}, login_email="")


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.form.to_dict()
    datos["email"] = datos.get("email", "").strip().lower()
    if not Usuario.validar_registro(datos):
        datos.pop("password", None)
        datos.pop("confirmar_password", None)
        return render_template("inicio.html", registro=datos, login_email=""), 400

    password_segura = bcrypt.generate_password_hash(datos["password"]).decode("utf-8")
    usuario_id = Usuario.crear(
        {
            "nombre": datos["nombre"].strip(),
            "apellido": datos["apellido"].strip(),
            "email": datos["email"],
            "password": password_segura,
        }
    )
    if not usuario_id:
        flash("No se pudo crear la cuenta. Inténtalo nuevamente.", "registro")
        return render_template("inicio.html", registro=datos, login_email=""), 500

    session.clear()
    session["usuario_id"] = usuario_id
    session["usuario_nombre"] = datos["nombre"].strip()
    flash("Cuenta creada correctamente. ¡Bienvenido a TaskTrack!", "exito")
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    usuario = Usuario.obtener_por_email(email)

    if not usuario or not bcrypt.check_password_hash(usuario.password, password):
        flash("Correo o contraseña incorrectos.", "login")
        return render_template("inicio.html", registro={}, login_email=email), 401

    session.clear()
    session["usuario_id"] = usuario.id
    session["usuario_nombre"] = usuario.nombre
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "exito")
    return redirect(url_for("inicio"))


@app.route("/dashboard")
@login_requerido
def dashboard():
    estado = request.args.get("estado", "").strip()
    busqueda = request.args.get("buscar", "").strip()
    tareas = Tarea.obtener_del_usuario(session["usuario_id"], estado, busqueda)
    proximas = Tarea.obtener_proximas(session["usuario_id"])
    resumen = Tarea.resumen(session["usuario_id"])
    return render_template(
        "dashboard.html",
        tareas=tareas,
        proximas=proximas,
        resumen=resumen,
        estado=estado,
        busqueda=busqueda,
        dias_restantes=Tarea.dias_restantes,
    )


@app.route("/perfil")
@login_requerido
def perfil():
    usuario = Usuario.obtener_por_id(session["usuario_id"])
    if not usuario:
        session.clear()
        return redirect(url_for("inicio"))
    return render_template("perfil.html", usuario=usuario, datos={})


@app.route("/perfil/actualizar", methods=["POST"])
@login_requerido
def actualizar_perfil():
    datos = request.form.to_dict()
    datos["email"] = datos.get("email", "").strip().lower()
    if not Usuario.validar_perfil(datos, session["usuario_id"]):
        usuario = Usuario.obtener_por_id(session["usuario_id"])
        return render_template("perfil.html", usuario=usuario, datos=datos), 400

    Usuario.actualizar(
        {
            "id": session["usuario_id"],
            "nombre": datos["nombre"].strip(),
            "apellido": datos["apellido"].strip(),
            "email": datos["email"],
        }
    )
    session["usuario_nombre"] = datos["nombre"].strip()
    flash("Perfil actualizado correctamente.", "exito")
    return redirect(url_for("perfil"))
