from flask import abort, redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.restaurante import Taqueria
from flask_app.models.taco import Especialidad


@app.route("/")
def index():
    return render_template("index.html", taquerias=Taqueria.get_all())


@app.route("/crear", methods=["POST"])
def crear():
    data = {
        "tortilla": request.form.get("tortilla", "").strip(),
        "guiso": request.form.get("guiso", "").strip(),
        "salsa": request.form.get("salsa", "").strip(),
        "restaurante_id": request.form.get("restaurante_id", ""),
    }

    if not all(data.values()):
        return redirect(url_for("index"))

    Especialidad.save(data)
    return redirect(url_for("tacos"))


@app.route("/tacos")
def tacos():
    return render_template("tacos.html", tacos=Especialidad.get_all())


@app.route("/restaurantes")
def restaurantes():
    return render_template("restaurantes.html", taquerias=Taqueria.get_all())


@app.route("/restaurantes/<int:identificador>")
def restaurante(identificador):
    taqueria = Taqueria.get_with_tacos({"id": identificador})

    if taqueria is None:
        abort(404, "Restaurante no encontrado")

    return render_template("restaurante.html", taqueria=taqueria)
