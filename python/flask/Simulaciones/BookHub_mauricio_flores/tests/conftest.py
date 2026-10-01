import os
from pathlib import Path
import pymysql
import pytest

# Permite importar la aplicación incluso antes de configurar .env para desarrollo.
os.environ.setdefault('SECRET_KEY', 'clave-solo-para-pruebas-locales')
from flask_app import app


@pytest.fixture(autouse=True)
def base_pruebas():
    anterior = app.config.copy()
    app.config.update(TESTING=True, DB_NAME='bookhub_pruebas', BCRYPT_LOG_ROUNDS=4)
    assert app.config['DB_NAME'] == 'bookhub_pruebas'
    conexion = pymysql.connect(
        host=app.config['DB_HOST'], port=app.config['DB_PORT'],
        user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
        database='bookhub_pruebas', charset='utf8mb4', autocommit=True)
    sql = (Path(__file__).resolve().parents[1] / 'resources/bookhub.sql').read_text(encoding='utf-8')
    sql = '\n'.join(linea for linea in sql.splitlines() if not linea.strip().startswith('--'))
    with conexion.cursor() as cursor:
        for sentencia in sql.split(';'):
            sentencia = sentencia.strip()
            if sentencia and not sentencia.upper().startswith(('CREATE DATABASE', 'USE ')):
                cursor.execute(sentencia)
        cursor.execute('DELETE FROM favoritos')
        cursor.execute('DELETE FROM libros')
        cursor.execute('DELETE FROM usuarios')
    conexion.close()
    yield
    app.config.clear()
    app.config.update(anterior)


@pytest.fixture
def cliente():
    return app.test_client()
