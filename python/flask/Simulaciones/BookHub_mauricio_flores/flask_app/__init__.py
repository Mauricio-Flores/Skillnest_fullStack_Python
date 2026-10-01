import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for, flash, g
from flask_bcrypt import Bcrypt
import pymysql

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv(
        'SECRET_KEY',
        'ba887c8050f215b8442382f0c1d44243ead3afce56e2d0a4763ed7df620ccf18'
    ),
    DB_HOST=os.getenv('DB_HOST', '127.0.0.1'),
    DB_PORT=int(os.getenv('DB_PORT', '3306')),
    DB_USER=os.getenv('DB_USER', 'root'),
    DB_PASSWORD=os.getenv('DB_PASSWORD', ''),
    DB_NAME=os.getenv('DB_NAME', 'bookhub'),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    MAX_CONTENT_LENGTH=64 * 1024,
)

bcrypt = Bcrypt(app)

from flask_app.utils.seguridad import verificar_csrf, csrf_token
from flask_app.models.usuario import Usuario
from flask_app.controllers.usuarios import usuarios
from flask_app.controllers.libros import libros
from flask_app.controllers.favoritos import favoritos

app.before_request(verificar_csrf)
app.jinja_env.globals['csrf_token'] = csrf_token
app.register_blueprint(usuarios)
app.register_blueprint(libros)
app.register_blueprint(favoritos)


@app.before_request
def cargar_usuario():
    g.usuario = None
    if 'usuario_id' in session:
        g.usuario = Usuario.buscar_por_id(session['usuario_id'])
        if g.usuario is None:
            session.clear()
            flash('Tu sesión ya no es válida. Inicia sesión nuevamente.', 'warning')
            return redirect(url_for('usuarios.inicio'))


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(413)
def error_cliente(error):
    mensajes = {
        400: 'La solicitud no es válida. Recarga el formulario e inténtalo nuevamente.',
        403: 'No puedes modificar ni eliminar un libro que no te pertenece.',
        404: 'La página o el libro que buscas no existe.',
        413: 'El formulario supera el tamaño permitido.',
    }
    return render_template('error.html', codigo=error.code, mensaje=mensajes[error.code]), error.code


@app.errorhandler(pymysql.MySQLError)
def error_base_datos(error):
    app.logger.error('Error de MySQL: %s', error)
    return render_template('error.html', codigo=503,
                           mensaje='No se pudo acceder a MySQL. Revisa la configuración y que el servidor esté iniciado.'), 503
