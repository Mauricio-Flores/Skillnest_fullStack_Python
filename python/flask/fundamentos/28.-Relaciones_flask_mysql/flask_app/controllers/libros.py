# ==========================================================
# CONTROLADOR DE LIBROS
# ==========================================================

from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.libro import Libro

from flask_app.models.autor import Autor


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario para crear un libro.

    También recupera todos los autores para que
    el usuario pueda seleccionar uno.
    """
    todos_autores = Autor.get_all()

    return render_template(
        "index.html",
        todos_autores=todos_autores
    )


# ==========================================================
# CREATE
# ==========================================================

@app.route("/crear", methods=["POST"])
def crear():
    """
    Recibe el formulario y crea un libro.
    """
    datos = {
        "titulo": request.form["titulo"].strip(),
        "genero": request.form["genero"].strip(),
        "editorial": request.form["editorial"].strip(),
        "autor_id": request.form["autor_id"]
    }

    Libro.save(datos)

    return redirect(url_for("libros"))


# ==========================================================
# READ
# LISTADO DE LIBROS
# ==========================================================

@app.route("/libros")
def libros():
    """
    Muestra todos los libros.
    """
    todos_los_libros = Libro.get_all()

    return render_template(
        "index.html",
        libros=todos_los_libros
    )


# ==========================================================
# READ
# AUTOR + LIBROS
# ==========================================================

@app.route("/autores/<int:id>")
def autor(id):
    """
    Muestra un autor junto con
    todos sus libros relacionados.
    """
    datos = {"id": id}

    autor = Autor.get_autor_y_libros(datos)

    if autor is None:
        return ("Autor no encontrado", 404)

    return render_template(
        "autor.html",
        autor=autor
    )


# ==========================================================
# LISTADO DE AUTORES
# ==========================================================

@app.route("/autores")
def autores():
    """
    Muestra todos los autores.
    """
    todos_autores = Autor.get_all()

    return render_template(
        "autores.html",
        autores=todos_autores
    )
