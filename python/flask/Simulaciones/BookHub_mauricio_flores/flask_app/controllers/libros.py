from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, abort
from flask_app.models.libro import Libro
from flask_app.models.favorito import Favorito
from flask_app.utils.seguridad import login_requerido

libros = Blueprint('libros', __name__)


def buscar_libro(libro_id, comprobar_dueno=False):
    libro = Libro.buscar(libro_id)
    if libro is None:
        abort(404)
    if comprobar_dueno and libro['usuario_id'] != g.usuario.id:
        abort(403)
    return libro


def datos_formulario():
    return {campo: request.form.get(campo, '').strip()
            for campo in ['titulo', 'autor', 'genero', 'fecha', 'descripcion']}


def formulario(datos, editar=False, libro_id=None):
    return render_template('formulario.html', datos=datos, editar=editar,
                           libro_id=libro_id, generos=Libro.GENEROS, hoy=date.today().isoformat())


@libros.get('/libros')
@login_requerido
def inicio():
    return render_template('libros.html', propios=Libro.propios(g.usuario.id),
                           comunidad=Libro.comunidad(g.usuario.id))


@libros.get('/explorar')
@login_requerido
def explorar():
    return render_template('explorar.html', comunidad=Libro.comunidad(g.usuario.id))


@libros.route('/libros/nuevo', methods=['GET', 'POST'])
@login_requerido
def nuevo():
    if request.method == 'GET':
        return formulario({})
    datos = datos_formulario()
    errores = Libro.validar(datos)
    if errores:
        for error in errores:
            flash(error, 'danger')
        return formulario(datos), 422
    datos['usuario_id'] = g.usuario.id
    Libro.crear(datos)
    flash('Libro creado correctamente.', 'success')
    return redirect(url_for('libros.inicio'))


@libros.get('/libros/<int:libro_id>')
@login_requerido
def detalle(libro_id):
    libro = buscar_libro(libro_id)
    return render_template('detalle.html', libro=libro,
                           usuarios=Favorito.usuarios(libro_id),
                           es_favorito=Favorito.existe(g.usuario.id, libro_id))


@libros.route('/libros/editar/<int:libro_id>', methods=['GET', 'POST'])
@login_requerido
def editar(libro_id):
    libro = buscar_libro(libro_id, comprobar_dueno=True)
    if request.method == 'GET':
        return formulario(libro, editar=True, libro_id=libro_id)
    datos = datos_formulario()
    errores = Libro.validar(datos)
    if errores:
        for error in errores:
            flash(error, 'danger')
        return formulario(datos, editar=True, libro_id=libro_id), 422
    datos.update(id=libro_id, usuario_id=g.usuario.id)
    Libro.actualizar(datos)
    flash('Libro actualizado correctamente.', 'success')
    return redirect(url_for('libros.inicio'))


@libros.post('/libros/eliminar/<int:libro_id>')
@login_requerido
def eliminar(libro_id):
    buscar_libro(libro_id, comprobar_dueno=True)
    Libro.eliminar(libro_id, g.usuario.id)
    flash('Libro eliminado correctamente.', 'success')
    return redirect(url_for('libros.inicio'))
