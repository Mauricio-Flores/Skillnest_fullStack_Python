import pytest

from flask_app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True, SECRET_KEY="clave-pruebas")
    with app.test_client() as cliente:
        yield cliente


@pytest.fixture
def sesion_iniciada(client):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = 1
        sesion["usuario_nombre"] = "Mauricio"
    return client
