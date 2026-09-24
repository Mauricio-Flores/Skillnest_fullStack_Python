# ==========================================================
# PUNTO DE ENTRADA
# ==========================================================

from flask_app import app

# Carga las rutas definidas en flask_app/controllers/libros.py
from flask_app.controllers import libros


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)
