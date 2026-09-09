from flask import Flask, abort, render_template
from pymysql import MySQLError

from mascota import Mascota

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", mascotas=Mascota.get_all())


@app.get("/mascota/<int:id>")
def mostrar_mascota(id):
    mascota = Mascota.get_by_id(id)
    if mascota is None:
        abort(404)
    return render_template("mascota.html", mascota=mascota)


@app.get("/mascota/nombre/<path:nombre>")
def buscar_nombre(nombre):
    mascota = Mascota.get_by_name(nombre)
    if mascota is None:
        abort(404)
    return render_template("mascota.html", mascota=mascota)


@app.errorhandler(404)
def no_encontrada(error):
    return render_template("error.html", codigo=404,
                           mensaje="Mascota o pagina no encontrada."), 404


@app.errorhandler(MySQLError)
def base_no_disponible(error):
    return render_template("error.html", codigo=503,
                           mensaje="La base de datos no esta disponible."), 503


if __name__ == "__main__":
    app.run()
