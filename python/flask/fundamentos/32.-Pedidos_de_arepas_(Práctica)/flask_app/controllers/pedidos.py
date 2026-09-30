from flask import flash, redirect, render_template, request, url_for

from flask_app import app
from flask_app.models.pedido import OrdenArepa


@app.route("/")
def inicio():
    return redirect(url_for("lista_pedidos"))


@app.route("/pedidos")
def lista_pedidos():
    return render_template("pedidos.html", pedidos=OrdenArepa.get_all())


@app.route("/pedidos/nuevo")
def nuevo_pedido():
    return render_template("nuevo_pedido.html")


@app.route("/pedidos/crear", methods=["POST"])
def crear_pedido():
    data = {
        "nombre": request.form.get("nombre", "").strip(),
        "tipo_arepa": request.form.get("tipo_arepa", "").strip(),
        "cantidad": request.form.get("cantidad", "").strip(),
    }

    if not OrdenArepa.validar_pedido(data):
        return redirect(url_for("nuevo_pedido"))

    data["cantidad"] = int(data["cantidad"])
    if OrdenArepa.save(data) is False:
        flash("No fue posible guardar el pedido.", "danger")
        return redirect(url_for("nuevo_pedido"))

    flash("Pedido creado correctamente.", "success")
    return redirect(url_for("lista_pedidos"))
