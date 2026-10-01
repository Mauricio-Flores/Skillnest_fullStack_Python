from flask import Blueprint, render_template, redirect, url_for, flash, g, abort
from flask_app.models.favorito import Favorito
from flask_app.models.libro import Libro
from flask_app.utils.seguridad import login_requerido

favoritos = Blueprint('favoritos', __name__)


@favoritos.get('/favoritos')
@login_requerido
def inicio():
    return render_template('favoritos.html', libros=Favorito.libros(g.usuario.id))


@favoritos.post('/favoritos/agregar/<int:libro_id>')
@login_requerido
def agregar(libro_id):
    if Libro.buscar(libro_id) is None:
        abort(404)
    if Favorito.existe(g.usuario.id, libro_id):
        flash('Este libro ya está en tus favoritos.', 'info')
    else:
        Favorito.agregar(g.usuario.id, libro_id)
        flash('Libro agregado a favoritos.', 'success')
    return redirect(url_for('libros.detalle', libro_id=libro_id))
