from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)

# Clave para manejar las sesiones
app.secret_key = "clave_secreta"

# Ruta principal: muestra el formulario
@app.route("/")
def inicio():
    return render_template("index.html")


# Ruta para recibir los datos mediante POST
@app.route("/enviar", methods=["POST"])
def enviar():
    session["nombre"] = request.form.get("nombre", "").strip()
    session["edad"] = request.form.get("edad", "").strip()
    session["color"] = request.form.get("color", "").strip()
    session["animal"] = request.form.get("animal", "").strip()

    return redirect("/futuro")


# Ruta que muestra una predicción personalizada
@app.route("/futuro")
def futuro():
    if "nombre" not in session:
        return redirect("/")

    predicciones = [
        "Encontrarás una oportunidad importante en los próximos meses. Tu esfuerzo comenzará a dar resultados.",
        "Una sorpresa inesperada llegará cuando menos lo esperes. Mantente atento a las nuevas posibilidades.",
        "Tendrás un período favorable para comenzar nuevos proyectos y conocer personas importantes.",
        "Deberás tomar una decisión importante. Confía en tu experiencia y piensa antes de actuar.",
        "Un pequeño desafío aparecerá en tu camino, pero tendrás la capacidad de superarlo y aprender de él."
    ]

    prediccion = random.choice(predicciones)

    return render_template(
        "futuro.html",
        nombre=session["nombre"],
        edad=session["edad"],
        color=session["color"],
        animal=session["animal"],
        prediccion=prediccion
    )


if __name__ == "__main__":
    app.run(debug=True)
