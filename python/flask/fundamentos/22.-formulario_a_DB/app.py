from flask import Flask, render_template, request, redirect, url_for
from animal import Animal


app = Flask(__name__)


@app.route("/")
def inicio():

    animales = Animal.listar()

    return render_template(
        "inicio.html",
        animales=animales
    )


@app.route("/nuevo_animal", methods=["POST"])
def nuevo_animal():

    datos = {
        "nombre": request.form["nombre"],
        "tipo": request.form["tipo"],
        "color": request.form["color"]
    }

    Animal.crear(datos)

    return redirect(
        url_for("inicio")
    )


if __name__ == "__main__":
    app.run(debug=True)