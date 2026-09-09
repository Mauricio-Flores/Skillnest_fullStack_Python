from flask import Flask, render_template
from pymysql import MySQLError

from mascota import Mascota


app = Flask(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html", todas_mascotas=Mascota.get_all()
    )


@app.errorhandler(MySQLError)
def error_mysql(error):
    app.logger.error("No se pudo acceder a la base de datos.")
    return render_template("error.html"), 503


if __name__ == "__main__":
    app.run()
