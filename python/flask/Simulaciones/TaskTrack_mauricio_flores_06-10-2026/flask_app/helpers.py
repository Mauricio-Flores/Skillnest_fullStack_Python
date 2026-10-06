from functools import wraps

from flask import flash, redirect, session, url_for


def login_requerido(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para continuar.", "login")
            return redirect(url_for("inicio"))
        return funcion(*args, **kwargs)

    return decorador
