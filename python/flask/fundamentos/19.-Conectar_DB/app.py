from flask import Flask, render_template
import pymysql

from mascota import Mascota
from usuario import Usuario


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", mascotas=Mascota.get_all())


@app.get("/usuarios")
def usuarios():
    return render_template("usuarios.html", usuarios=Usuario.get_all())


@app.errorhandler(404)
def no_encontrado(error):
    return render_template("404.html"), 404


@app.errorhandler(pymysql.MySQLError)
def base_no_disponible(error):
    app.logger.error("Base de datos no disponible.")
    return render_template("503.html"), 503


if __name__ == "__main__":
    app.run()
