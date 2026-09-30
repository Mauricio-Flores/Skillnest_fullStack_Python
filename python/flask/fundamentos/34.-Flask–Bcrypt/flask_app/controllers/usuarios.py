"""Routes for account registration and authentication."""

import secrets

import pymysql
from flask import flash, redirect, render_template, request, session

from flask_app import app, bcrypt
from flask_app.models.usuario import Account


def _csrf_token():
    """Keep a per-session token so state-changing forms reject cross-site posts."""
    return session.setdefault("csrf_token", secrets.token_urlsafe(32))


def _valid_csrf():
    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("csrf_token", "")
    return bool(session_token) and secrets.compare_digest(
        session_token, submitted_token
    )


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": _csrf_token}


@app.get("/")
def index():
    if session.get("account_id"):
        return redirect("/dashboard")
    return render_template("login.html")


@app.get("/registro")
def registro():
    if session.get("account_id"):
        return redirect("/dashboard")
    return render_template("registro.html")


@app.post("/registrar")
def registrar():
    if not _valid_csrf():
        flash("No se pudo validar el formulario. Intenta nuevamente.", "general")
        return redirect("/registro")

    account_data = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "password": request.form.get("password", ""),
    }

    if not Account.validate_registration(account_data):
        return redirect("/registro")

    if Account.email_exists({"email": account_data["email"]}):
        flash("El email ya está registrado.", "email")
        return redirect("/registro")

    account_data["password"] = bcrypt.generate_password_hash(
        account_data["password"]
    ).decode("utf-8")

    try:
        account_id = Account.save(account_data)
    except pymysql.IntegrityError:
        flash("El email ya está registrado.", "email")
        return redirect("/registro")

    if not account_id:
        flash("No fue posible registrar el usuario.", "general")
        return redirect("/registro")

    session.clear()
    session["account_id"] = account_id
    return redirect("/dashboard")


@app.post("/login")
def login():
    if not _valid_csrf():
        flash("No se pudo validar el formulario. Intenta nuevamente.", "login")
        return redirect("/")

    account = Account.find_by_email(
        {"email": request.form.get("email", "").strip().lower()}
    )
    password = request.form.get("password", "")

    if not account or not bcrypt.check_password_hash(account.password, password):
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    session.clear()
    session["account_id"] = account.id
    return redirect("/dashboard")


@app.get("/dashboard")
def dashboard():
    account_id = session.get("account_id")
    if not account_id:
        flash("Debes iniciar sesión.", "login")
        return redirect("/")

    account = Account.find_by_id({"id": account_id})
    if not account:
        session.clear()
        flash("Debes iniciar sesión.", "login")
        return redirect("/")

    return render_template("dashboard.html", usuario=account)


@app.post("/logout")
def logout():
    if not _valid_csrf():
        flash("No se pudo validar el formulario. Intenta nuevamente.", "general")
        return redirect("/")
    session.clear()
    return redirect("/")
