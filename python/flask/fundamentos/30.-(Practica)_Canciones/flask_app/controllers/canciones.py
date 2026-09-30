from flask import abort, flash, redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.cancion import Pista
from flask_app.models.favorito import MarcadoFavorito
from flask_app.models.usuario import Persona


@app.route("/")
def inicio():
    return redirect(url_for("usuarios"))


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", usuarios=Persona.get_all())


@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    data = {
        "nombre": request.form.get("nombre", "").strip(),
        "email": request.form.get("email", "").strip(),
        "contrasena": request.form.get("contrasena", "").strip(),
    }

    if not all(data.values()):
        flash("Todos los campos son obligatorios.", "danger")
    elif Persona.save(data) is False:
        flash("No fue posible crear el usuario.", "danger")
    else:
        flash("Usuario creado correctamente.", "success")

    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:identificador>")
def mostrar_usuario(identificador):
    persona = Persona.get_with_favorites({"id": identificador})

    if persona is None:
        abort(404, "Usuario no encontrado")

    return render_template(
        "mostrar_usuario.html",
        usuario=persona,
        canciones=Pista.get_all(),
    )


@app.route("/canciones")
def canciones():
    return render_template("canciones.html", canciones=Pista.get_all())


@app.route("/canciones/crear", methods=["POST"])
def crear_cancion():
    data = {
        "titulo": request.form.get("titulo", "").strip(),
        "artista": request.form.get("artista", "").strip(),
    }

    if not all(data.values()):
        flash("Titulo y artista son obligatorios.", "danger")
    elif Pista.save(data) is False:
        flash("No fue posible crear la cancion.", "danger")
    else:
        flash("Cancion creada correctamente.", "success")

    return redirect(url_for("canciones"))


@app.route("/canciones/<int:identificador>")
def mostrar_cancion(identificador):
    pista = Pista.get_with_users({"id": identificador})

    if pista is None:
        abort(404, "Cancion no encontrada")

    return render_template(
        "mostrar_cancion.html",
        cancion=pista,
        usuarios=Persona.get_all(),
    )


@app.route("/favoritos/agregar", methods=["POST"])
def agregar_favorito():
    origen = request.form.get("origen")

    try:
        data = {
            "usuario_id": int(request.form["usuario_id"]),
            "cancion_id": int(request.form["cancion_id"]),
        }
    except (KeyError, ValueError):
        flash("Los identificadores no son validos.", "danger")
        return redirect(url_for("usuarios"))

    if Persona.get_by_id(data["usuario_id"]) is None:
        flash("El usuario seleccionado no existe.", "danger")
    elif Pista.get_by_id(data["cancion_id"]) is None:
        flash("La cancion seleccionada no existe.", "danger")
    elif MarcadoFavorito.exists(data):
        flash("Esta cancion ya esta entre los favoritos del usuario.", "warning")
    elif MarcadoFavorito.add(data) is False:
        flash("No fue posible agregar el favorito.", "danger")
    else:
        flash("Favorito agregado correctamente.", "success")

    if origen == "cancion":
        return redirect(url_for("mostrar_cancion", identificador=data["cancion_id"]))

    return redirect(url_for("mostrar_usuario", identificador=data["usuario_id"]))
