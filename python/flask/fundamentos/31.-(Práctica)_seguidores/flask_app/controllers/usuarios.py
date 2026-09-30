from flask import flash, redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.seguidor import FollowLink
from flask_app.models.usuario import MemberRecord


@app.get("/")
def home():
    return redirect(url_for("show_users"))


@app.get("/usuarios")
def show_users():
    return render_template(
        "usuarios.html",
        usuarios=MemberRecord.list_all(),
        relaciones=FollowLink.list_all(),
    )


@app.post("/usuarios/crear")
def create_user():
    data = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
    }
    if not all(data.values()):
        flash("Todos los campos son obligatorios.", "danger")
    elif MemberRecord.create(data) is False:
        flash("No fue posible crear el usuario.", "danger")
    else:
        flash("Usuario creado correctamente.", "success")
    return redirect(url_for("show_users"))


@app.post("/seguir")
def create_follow_relation():
    try:
        data = {
            "usuario_id": int(request.form.get("usuario_id", "")),
            "seguidor_id": int(request.form.get("seguidor_id", "")),
        }
    except ValueError:
        flash("Los identificadores no son válidos.", "danger")
        return redirect(url_for("show_users"))

    if MemberRecord.find(data["usuario_id"]) is None:
        flash("El usuario seleccionado no existe.", "danger")
    elif MemberRecord.find(data["seguidor_id"]) is None:
        flash("El seguidor seleccionado no existe.", "danger")
    elif FollowLink.create(data) is False:
        flash("No fue posible registrar la relación.", "danger")
    else:
        flash("Relación registrada correctamente.", "success")
    return redirect(url_for("show_users"))
