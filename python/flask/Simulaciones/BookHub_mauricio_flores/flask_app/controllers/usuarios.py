from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from pymysql import IntegrityError
from flask_app import bcrypt
from flask_app.models.usuario import Usuario
from flask_app.utils.seguridad import login_requerido

usuarios = Blueprint('usuarios', __name__)


@usuarios.get('/')
def inicio():
    if g.usuario:
        return redirect(url_for('libros.inicio'))
    return render_template('login.html', datos={}, email_login='')


@usuarios.post('/registro')
def registro():
    if g.usuario:
        return redirect(url_for('libros.inicio'))
    datos = {campo: request.form.get(campo, '').strip() for campo in ['nombre', 'apellido', 'email']}
    datos['email'] = datos['email'].lower()
    datos['password'] = request.form.get('password', '')
    datos['confirmar'] = request.form.get('confirmar', '')
    errores = Usuario.validar(datos)
    if errores:
        for error in errores:
            flash(error, 'danger')
        return render_template('login.html', datos=datos, email_login=''), 422
    datos['password'] = bcrypt.generate_password_hash(datos['password']).decode('utf-8')
    try:
        usuario_id = Usuario.crear(datos)
    except IntegrityError as error:
        if error.args[0] != 1062:
            raise
        flash('Este correo electrónico ya está registrado.', 'danger')
        return render_template('login.html', datos=datos, email_login=''), 422
    session.clear()
    session['usuario_id'] = usuario_id
    session.permanent = True
    flash('Cuenta creada correctamente. Bienvenido a BookHub.', 'success')
    return redirect(url_for('libros.inicio'))


@usuarios.post('/login')
def login():
    if g.usuario:
        return redirect(url_for('libros.inicio'))
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    usuario = Usuario.buscar_por_email(email) if len(email) <= 254 else None
    valido = bool(usuario and len(password.encode('utf-8')) <= 72
                  and bcrypt.check_password_hash(usuario.password, password))
    if not valido:
        flash('Correo o contraseña incorrectos.', 'danger')
        return render_template('login.html', datos={}, email_login=email), 422
    session.clear()
    session['usuario_id'] = usuario.id
    session.permanent = True
    flash(f'Bienvenido, {usuario.nombre}.', 'success')
    return redirect(url_for('libros.inicio'))


@usuarios.post('/logout')
@login_requerido
def logout():
    session.clear()
    flash('Cerraste sesión correctamente.', 'success')
    return redirect(url_for('usuarios.inicio'))
