import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt


load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "tasktrack-clave-desarrollo")
bcrypt = Bcrypt(app)

from flask_app.controllers import categorias, tareas, usuarios  # noqa: E402, F401
