import secrets
from functools import wraps
from flask import session, request, abort, flash, redirect, url_for, g


def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def verificar_csrf():
    if request.method == 'POST':
        recibido = request.form.get('csrf_token', '')
        esperado = session.get('csrf_token', '')
        if not esperado or not secrets.compare_digest(esperado.encode('utf-8'), recibido.encode('utf-8')):
            abort(400)


def login_requerido(funcion):
    @wraps(funcion)
    def ruta_protegida(*args, **kwargs):
        if g.usuario is None:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('usuarios.inicio'))
        return funcion(*args, **kwargs)
    return ruta_protegida
