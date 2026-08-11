from flask import Flask, render_template, request

app = Flask(__name__)


# ==========================================
# Página principal
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# Recibir formulario
# ==========================================

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    nombre = request.form.get("nombre")
    email = request.form.get("email")
    edad = request.form.get("edad")
    ciudad = request.form.get("ciudad")

    return render_template(
        "usuario.html",
        nombre=nombre,
        email=email,
        edad=edad,
        ciudad=ciudad
    )


# ==========================================
# Ejecutar servidor
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

