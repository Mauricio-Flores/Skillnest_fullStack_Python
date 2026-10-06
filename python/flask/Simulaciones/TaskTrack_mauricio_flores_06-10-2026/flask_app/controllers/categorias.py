from flask import flash, redirect, render_template, request, session, url_for

from flask_app import app
from flask_app.helpers import login_requerido
from flask_app.models.categoria import Categoria
from flask_app.models.tarea import Tarea


@app.route("/categorias")
@login_requerido
def categorias():
    lista = Categoria.obtener_del_usuario(session["usuario_id"])
    editar_id = request.args.get("editar", type=int)
    categoria_editar = None
    if editar_id:
        categoria_editar = Categoria.obtener_por_id_y_usuario(editar_id, session["usuario_id"])
        if not categoria_editar:
            flash("La categoría no existe o no te pertenece.", "error")
    return render_template(
        "categorias.html", categorias=lista, categoria_editar=categoria_editar, nombre_form=""
    )


@app.route("/categorias/crear", methods=["POST"])
@login_requerido
def crear_categoria():
    nombre = request.form.get("nombre", "").strip()
    if not Categoria.validar(nombre, session["usuario_id"]):
        lista = Categoria.obtener_del_usuario(session["usuario_id"])
        return render_template(
            "categorias.html", categorias=lista, categoria_editar=None, nombre_form=nombre
        ), 400
    Categoria.crear({"nombre": nombre, "usuario_id": session["usuario_id"]})
    flash("Categoría creada correctamente.", "exito")
    return redirect(url_for("categorias"))


@app.route("/categorias/<int:categoria_id>")
@login_requerido
def detalle_categoria(categoria_id):
    categoria = Categoria.obtener_por_id_y_usuario(categoria_id, session["usuario_id"])
    if not categoria:
        flash("La categoría no existe o no te pertenece.", "error")
        return redirect(url_for("categorias"))
    tareas = Tarea.obtener_por_categoria(categoria_id, session["usuario_id"])
    return render_template("categoria_detalle.html", categoria=categoria, tareas=tareas)


@app.route("/categorias/<int:categoria_id>/actualizar", methods=["POST"])
@login_requerido
def actualizar_categoria(categoria_id):
    categoria = Categoria.obtener_por_id_y_usuario(categoria_id, session["usuario_id"])
    if not categoria:
        flash("La categoría no existe o no te pertenece.", "error")
        return redirect(url_for("categorias"))

    nombre = request.form.get("nombre", "").strip()
    if not Categoria.validar(nombre, session["usuario_id"], categoria_id):
        lista = Categoria.obtener_del_usuario(session["usuario_id"])
        categoria.nombre = nombre
        return render_template(
            "categorias.html", categorias=lista, categoria_editar=categoria, nombre_form=""
        ), 400

    Categoria.actualizar(
        {"id": categoria_id, "nombre": nombre, "usuario_id": session["usuario_id"]}
    )
    flash("Categoría actualizada correctamente.", "exito")
    return redirect(url_for("categorias"))


@app.route("/categorias/<int:categoria_id>/borrar", methods=["POST"])
@login_requerido
def borrar_categoria(categoria_id):
    categoria = Categoria.obtener_por_id_y_usuario(categoria_id, session["usuario_id"])
    if not categoria:
        flash("La categoría no existe o no te pertenece.", "error")
        return redirect(url_for("categorias"))
    if categoria.cantidad_tareas > 0:
        flash("No puedes borrar una categoría que todavía contiene tareas.", "error")
        return redirect(url_for("categorias"))
    Categoria.borrar(categoria_id, session["usuario_id"])
    flash("Categoría eliminada.", "exito")
    return redirect(url_for("categorias"))
