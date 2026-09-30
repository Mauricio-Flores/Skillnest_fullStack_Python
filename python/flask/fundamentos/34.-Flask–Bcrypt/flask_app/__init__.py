"""Application setup for the secure accounts project."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY must be configured in the environment.")

app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios  # noqa: E402, F401
