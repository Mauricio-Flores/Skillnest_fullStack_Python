from flask import flash, redirect, render_template, request, session, url_for

from flask_app import app
from flask_app.helpers import login_requerido
from flask_app.models.categoria import Categoria
from flask_app.models.comentario import Comentario
from flask_app.models.tarea import ESTADOS, PRIORIDADES, Tarea


def buscar_tarea_propia(tarea_id):
    tarea = Tarea.obtener_por_id_y_usuario(tarea_id, session["usuario_id"])
    if not tarea:
        flash("La tarea no existe o no tienes permiso para verla.", "error")
    return tarea


@app.route("/tareas/nueva")
@login_requerido
def nueva_tarea():
    categorias = Categoria.obtener_del_usuario(session["usuario_id"])
    return render_template(
        "tarea_form.html",
        titulo_pagina="Nueva Tarea",
        accion=url_for("crear_tarea"),
        boton="Guardar",
        tarea=None,
        datos={},
        categorias=categorias,
        prioridades=PRIORIDADES,
        estados=ESTADOS,
    )


@app.route("/tareas/crear", methods=["POST"])
@login_requerido
def crear_tarea():
    datos = request.form.to_dict()
    datos["estado"] = "Pendiente"
    if not Tarea.validar(datos, session["usuario_id"]):
        categorias = Categoria.obtener_del_usuario(session["usuario_id"])
        return render_template(
            "tarea_form.html",
            titulo_pagina="Nueva Tarea",
            accion=url_for("crear_tarea"),
            boton="Guardar",
            tarea=None,
            datos=datos,
            categorias=categorias,
            prioridades=PRIORIDADES,
            estados=ESTADOS,
        ), 400

    datos["usuario_id"] = session["usuario_id"]
    tarea_id = Tarea.crear(datos)
    flash("Tarea creada correctamente.", "exito")
    return redirect(url_for("detalle_tarea", tarea_id=tarea_id))


@app.route("/tareas/<int:tarea_id>")
@login_requerido
def detalle_tarea(tarea_id):
    tarea = buscar_tarea_propia(tarea_id)
    if not tarea:
        return redirect(url_for("dashboard"))
    comentarios = Comentario.obtener_de_tarea(tarea_id)
    return render_template("tarea_detalle.html", tarea=tarea, comentarios=comentarios)


@app.route("/tareas/editar/<int:tarea_id>")
@login_requerido
def editar_tarea(tarea_id):
    tarea = buscar_tarea_propia(tarea_id)
    if not tarea:
        return redirect(url_for("dashboard"))
    categorias = Categoria.obtener_del_usuario(session["usuario_id"])
    return render_template(
        "tarea_form.html",
        titulo_pagina="Editar Tarea",
        accion=url_for("actualizar_tarea", tarea_id=tarea_id),
        boton="Actualizar",
        tarea=tarea,
        datos={},
        categorias=categorias,
        prioridades=PRIORIDADES,
        estados=ESTADOS,
    )


@app.route("/tareas/<int:tarea_id>/actualizar", methods=["POST"])
@login_requerido
def actualizar_tarea(tarea_id):
    tarea = buscar_tarea_propia(tarea_id)
    if not tarea:
        return redirect(url_for("dashboard"))
    datos = request.form.to_dict()
    permitir_pasada = str(tarea.fecha_limite) == datos.get("fecha_limite")
    if not Tarea.validar(datos, session["usuario_id"], permitir_pasada):
        categorias = Categoria.obtener_del_usuario(session["usuario_id"])
        return render_template(
            "tarea_form.html",
            titulo_pagina="Editar Tarea",
            accion=url_for("actualizar_tarea", tarea_id=tarea_id),
            boton="Actualizar",
            tarea=tarea,
            datos=datos,
            categorias=categorias,
            prioridades=PRIORIDADES,
            estados=ESTADOS,
        ), 400

    datos["id"] = tarea_id
    datos["usuario_id"] = session["usuario_id"]
    Tarea.actualizar(datos)
    flash("Tarea actualizada correctamente.", "exito")
    return redirect(url_for("detalle_tarea", tarea_id=tarea_id))


@app.route("/tareas/<int:tarea_id>/completar", methods=["POST"])
@login_requerido
def completar_tarea(tarea_id):
    if not buscar_tarea_propia(tarea_id):
        return redirect(url_for("dashboard"))
    Tarea.completar(tarea_id, session["usuario_id"])
    flash("Tarea marcada como completada.", "exito")
    return redirect(request.referrer or url_for("dashboard"))


@app.route("/tareas/<int:tarea_id>/borrar", methods=["POST"])
@login_requerido
def borrar_tarea(tarea_id):
    if not buscar_tarea_propia(tarea_id):
        return redirect(url_for("dashboard"))
    Tarea.borrar(tarea_id, session["usuario_id"])
    flash("Tarea eliminada.", "exito")
    return redirect(url_for("dashboard"))


@app.route("/tareas/<int:tarea_id>/comentarios", methods=["POST"])
@login_requerido
def crear_comentario(tarea_id):
    if not buscar_tarea_propia(tarea_id):
        return redirect(url_for("dashboard"))
    contenido = request.form.get("contenido", "").strip()
    if Comentario.validar(contenido):
        Comentario.crear(
            {"contenido": contenido, "usuario_id": session["usuario_id"], "tarea_id": tarea_id}
        )
        flash("Comentario agregado.", "exito")
    return redirect(url_for("detalle_tarea", tarea_id=tarea_id))


@app.route("/tareas/<int:tarea_id>/comentarios/<int:comentario_id>/borrar", methods=["POST"])
@login_requerido
def borrar_comentario(tarea_id, comentario_id):
    if not buscar_tarea_propia(tarea_id):
        return redirect(url_for("dashboard"))
    Comentario.borrar(comentario_id, session["usuario_id"], tarea_id)
    flash("Comentario eliminado.", "exito")
    return redirect(url_for("detalle_tarea", tarea_id=tarea_id))
