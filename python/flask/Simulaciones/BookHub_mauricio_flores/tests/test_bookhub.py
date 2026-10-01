from datetime import date, timedelta
import pytest
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.libro import Libro
from flask_app.models.favorito import Favorito
from flask_app.config.mysqlconnection import connectToMySQL


def post(cliente, ruta, datos=None, seguir=False):
    cliente.get('/', follow_redirects=True)
    with cliente.session_transaction() as sesion:
        token = sesion['csrf_token']
    return cliente.post(ruta, data={**(datos or {}), 'csrf_token': token}, follow_redirects=seguir)


def registro(cliente, email='ana@example.com'):
    return post(cliente, '/registro', {
        'nombre': 'Ana', 'apellido': 'Rojas', 'email': email,
        'password': 'Clave1234', 'confirmar': 'Clave1234',
    }, seguir=True)


def datos_libro(**cambios):
    return dict(titulo='Libro de prueba', autor='Autora de prueba', genero='Novela',
                fecha=date.today().isoformat(), descripcion='Descripción completa del libro.', **cambios)


def crear_libro(cliente):
    post(cliente, '/libros/nuevo', datos_libro())
    with app.app_context():
        return connectToMySQL().query_db('SELECT id FROM libros ORDER BY id DESC LIMIT 1')[0]['id']


@pytest.mark.parametrize('ruta', ['/libros', '/explorar', '/favoritos', '/libros/nuevo', '/libros/1', '/libros/editar/1'])
def test_rutas_privadas(cliente, ruta):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 302
    assert respuesta.headers['Location'].endswith('/')


def test_registro_hash_y_sesion(cliente):
    respuesta = registro(cliente)
    assert respuesta.status_code == 200
    assert b'Cuenta creada correctamente' in respuesta.data
    with app.app_context():
        usuario = Usuario.buscar_por_email('ana@example.com')
        assert usuario.password != 'Clave1234'
        assert bcrypt.check_password_hash(usuario.password, 'Clave1234')
    with cliente.session_transaction() as sesion:
        assert sesion['usuario_id'] == usuario.id


def test_registro_invalido_no_crea_usuario(cliente):
    respuesta = post(cliente, '/registro', {
        'nombre': 'A', 'apellido': '', 'email': 'no-es-correo',
        'password': '123', 'confirmar': '456'})
    assert respuesta.status_code == 422
    assert b'Las contrase' in respuesta.data
    with app.app_context():
        assert not connectToMySQL().query_db('SELECT id FROM usuarios')


def test_email_unico(cliente):
    registro(cliente)
    post(cliente, '/logout')
    respuesta = registro(cliente, 'ANA@EXAMPLE.COM')
    assert b'ya est' in respuesta.data
    with app.app_context():
        assert len(connectToMySQL().query_db('SELECT id FROM usuarios')) == 1


def test_password_largo_no_produce_error(cliente):
    respuesta = post(cliente, '/registro', {'nombre': 'Ana', 'apellido': 'Rojas',
        'email': 'ana@example.com', 'password': 'á' * 40, 'confirmar': 'á' * 40})
    assert respuesta.status_code == 422
    assert b'72 bytes' in respuesta.data


def test_login_logout_y_clave_incorrecta(cliente):
    registro(cliente)
    post(cliente, '/logout')
    with cliente.session_transaction() as sesion:
        assert 'usuario_id' not in sesion
    respuesta = post(cliente, '/login', {'email': 'ana@example.com', 'password': 'incorrecta'})
    assert respuesta.status_code == 422
    assert cliente.get('/libros').status_code == 302
    respuesta = post(cliente, '/login', {'email': 'ana@example.com', 'password': 'Clave1234'}, seguir=True)
    assert respuesta.status_code == 200
    assert b'Mis Libros' in respuesta.data


def test_csrf_y_mutaciones_solo_post(cliente):
    assert cliente.post('/registro', data={}).status_code == 400
    assert cliente.post('/registro', data={'csrf_token': 'inválido'}).status_code == 400
    registro(cliente)
    libro_id = crear_libro(cliente)
    assert cliente.get(f'/libros/eliminar/{libro_id}').status_code == 405
    assert cliente.get('/logout').status_code == 405
    assert cliente.post(f'/libros/eliminar/{libro_id}', data={}).status_code == 400
    with app.app_context():
        assert Libro.buscar(libro_id)


def test_crud_y_formulario_precargado(cliente):
    registro(cliente)
    libro_id = crear_libro(cliente)
    assert b'Libro de prueba' in cliente.get('/libros').data
    assert b'Descripci' in cliente.get(f'/libros/{libro_id}').data
    respuesta = cliente.get(f'/libros/editar/{libro_id}')
    assert b'value="Libro de prueba"' in respuesta.data
    assert b'selected>Novela' in respuesta.data
    datos = datos_libro()
    datos['titulo'] = 'Libro actualizado'
    assert post(cliente, f'/libros/editar/{libro_id}', datos).status_code == 302
    with app.app_context():
        assert Libro.buscar(libro_id)['titulo'] == 'Libro actualizado'
    respuesta = post(cliente, f'/libros/eliminar/{libro_id}', seguir=True)
    assert b'Libro eliminado correctamente' in respuesta.data
    assert cliente.get(f'/libros/{libro_id}').status_code == 404


@pytest.mark.parametrize('campo,valor', [
    ('titulo', 'X'), ('autor', ''), ('genero', 'inventado'),
    ('fecha', ''), ('fecha', '2026-02-30'),
    ('fecha', (date.today() - timedelta(days=1)).isoformat()),
    ('descripcion', 'corta'),
])
def test_validaciones_libro_en_backend(cliente, campo, valor):
    registro(cliente)
    datos = datos_libro()
    datos[campo] = valor
    respuesta = post(cliente, '/libros/nuevo', datos)
    assert respuesta.status_code == 422
    with app.app_context():
        assert not connectToMySQL().query_db('SELECT id FROM libros')


def test_edicion_invalida_conserva_datos(cliente):
    registro(cliente)
    libro_id = crear_libro(cliente)
    datos = datos_libro()
    datos['fecha'] = '2000-01-01'
    respuesta = post(cliente, f'/libros/editar/{libro_id}', datos)
    assert respuesta.status_code == 422
    with app.app_context():
        assert Libro.buscar(libro_id)['fecha'] == date.today()


def test_otra_cuenta_no_edita_ni_borra(cliente):
    registro(cliente)
    libro_id = crear_libro(cliente)
    post(cliente, '/logout')
    registro(cliente, 'otra@example.com')
    assert b'Libro de prueba' in cliente.get('/explorar').data
    assert cliente.get(f'/libros/{libro_id}').status_code == 200
    assert cliente.get(f'/libros/editar/{libro_id}').status_code == 403
    assert post(cliente, f'/libros/editar/{libro_id}', datos_libro()).status_code == 403
    assert post(cliente, f'/libros/eliminar/{libro_id}').status_code == 403
    with app.app_context():
        libro = Libro.buscar(libro_id)
        assert libro
        otra = Usuario.buscar_por_email('otra@example.com')
        assert Libro.eliminar(libro_id, otra.id) == 0
        assert Libro.buscar(libro_id)


def test_no_se_puede_falsificar_el_dueno(cliente):
    registro(cliente)
    datos = datos_libro()
    datos['usuario_id'] = 99999
    post(cliente, '/libros/nuevo', datos)
    with app.app_context():
        usuario = Usuario.buscar_por_email('ana@example.com')
        assert Libro.propios(usuario.id)[0]['usuario_id'] == usuario.id


def test_favoritos_relaciones_duplicados_y_cascada(cliente):
    registro(cliente)
    libro_id = crear_libro(cliente)
    post(cliente, '/logout')
    registro(cliente, 'otra@example.com')
    respuesta = post(cliente, f'/favoritos/agregar/{libro_id}', seguir=True)
    assert b'Agregar a favoritos' not in respuesta.data
    assert b'Usuarios que agregaron este libro a favoritos (1)' in respuesta.data
    assert b'Libro de prueba' in cliente.get('/favoritos').data
    post(cliente, f'/favoritos/agregar/{libro_id}')
    with app.app_context():
        usuario = Usuario.buscar_por_email('otra@example.com')
        Favorito.agregar(usuario.id, libro_id)
        assert len(Favorito.usuarios(libro_id)) == 1
        assert Libro.buscar(libro_id)['total_favoritos'] == 1
    post(cliente, '/logout')
    post(cliente, '/login', {'email': 'ana@example.com', 'password': 'Clave1234'})
    assert b'Libro de prueba' not in cliente.get('/favoritos').data
    post(cliente, f'/libros/eliminar/{libro_id}')
    with app.app_context():
        assert not Favorito.usuarios(libro_id)
    assert post(cliente, f'/favoritos/agregar/{libro_id}').status_code == 404


def test_escape_jinja_y_sql_parametrizado(cliente):
    registro(cliente)
    datos = datos_libro()
    datos['titulo'] = '<script>alert(1)</script>'
    datos['autor'] = "O'Reilly"
    post(cliente, '/libros/nuevo', datos)
    respuesta = cliente.get('/libros')
    assert b'&lt;script&gt;' in respuesta.data
    assert b'<script>alert(1)</script>' not in respuesta.data
    post(cliente, '/logout')
    respuesta = post(cliente, '/login', {'email': "' OR 1=1 --", 'password': 'Clave1234'})
    assert respuesta.status_code == 422


def test_sesion_de_usuario_eliminado_se_limpia(cliente):
    registro(cliente)
    with app.app_context():
        connectToMySQL().query_db('DELETE FROM usuarios')
    assert cliente.get('/libros').status_code == 302
    with cliente.session_transaction() as sesion:
        assert 'usuario_id' not in sesion
