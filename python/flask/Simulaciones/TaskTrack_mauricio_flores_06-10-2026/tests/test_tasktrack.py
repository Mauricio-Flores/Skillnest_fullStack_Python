from datetime import date, timedelta
from types import SimpleNamespace

from flask_app import bcrypt
from flask_app.models.categoria import Categoria
from flask_app.models.comentario import Comentario
from flask_app.models.tarea import Tarea
from flask_app.models.usuario import Usuario


def usuario_demo(password="Clave123"):
    return SimpleNamespace(
        id=1,
        nombre="Mauricio",
        apellido="Flores",
        email="mauricio@example.com",
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
    )


def categoria_demo(cantidad=0):
    return SimpleNamespace(id=2, nombre="Estudios", usuario_id=1, cantidad_tareas=cantidad)


def tarea_demo():
    return SimpleNamespace(
        id=3,
        titulo="Estudiar Flask",
        descripcion="Repasar rutas, modelos y controladores.",
        prioridad="Alta",
        estado="Pendiente",
        fecha_limite=date.today() + timedelta(days=3),
        usuario_id=1,
        categoria_id=2,
        categoria="Estudios",
        creador="Mauricio Flores",
    )


def test_inicio_es_publico(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert b"TaskTrack" in respuesta.data


def test_dashboard_exige_login(client):
    respuesta = client.get("/dashboard")
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/")


def test_nueva_tarea_exige_login(client):
    assert client.get("/tareas/nueva").status_code == 302


def test_login_rechaza_datos_incorrectos(client, monkeypatch):
    monkeypatch.setattr(Usuario, "obtener_por_email", classmethod(lambda cls, email: None))
    respuesta = client.post("/login", data={"email": "x@example.com", "password": "mala"})
    assert respuesta.status_code == 401
    assert "Correo o contraseña incorrectos" in respuesta.get_data(as_text=True)


def test_login_correcto_crea_sesion(client, monkeypatch):
    monkeypatch.setattr(Usuario, "obtener_por_email", classmethod(lambda cls, email: usuario_demo()))
    respuesta = client.post(
        "/login", data={"email": "mauricio@example.com", "password": "Clave123"}
    )
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/dashboard")
    with client.session_transaction() as sesion:
        assert sesion["usuario_id"] == 1


def test_logout_limpia_sesion(sesion_iniciada):
    respuesta = sesion_iniciada.get("/logout")
    assert respuesta.status_code == 302
    with sesion_iniciada.session_transaction() as sesion:
        assert "usuario_id" not in sesion


def test_registro_correcto(client, monkeypatch):
    monkeypatch.setattr(Usuario, "validar_registro", staticmethod(lambda datos: True))
    monkeypatch.setattr(Usuario, "crear", classmethod(lambda cls, datos: 9))
    respuesta = client.post(
        "/registro",
        data={
            "nombre": "Mauricio",
            "apellido": "Flores",
            "email": "mauricio@example.com",
            "password": "Clave123",
            "confirmar_password": "Clave123",
        },
    )
    assert respuesta.status_code == 302
    with client.session_transaction() as sesion:
        assert sesion["usuario_id"] == 9


def test_dashboard_muestra_tareas(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Tarea, "obtener_del_usuario", classmethod(lambda cls, *args: [tarea_demo()]))
    monkeypatch.setattr(Tarea, "obtener_proximas", classmethod(lambda cls, *args: [tarea_demo()]))
    monkeypatch.setattr(
        Tarea,
        "resumen",
        classmethod(lambda cls, *args: {"total": 1, "pendientes": 1, "en_progreso": 0, "completadas": 0, "alta": 1, "media": 0, "baja": 0}),
    )
    respuesta = sesion_iniciada.get("/dashboard")
    assert respuesta.status_code == 200
    assert "Estudiar Flask" in respuesta.get_data(as_text=True)


def test_formulario_nueva_tarea(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Categoria, "obtener_del_usuario", classmethod(lambda cls, uid: [categoria_demo()]))
    respuesta = sesion_iniciada.get("/tareas/nueva")
    assert respuesta.status_code == 200
    assert "Nueva Tarea" in respuesta.get_data(as_text=True)


def test_crear_tarea_conserva_datos_si_falla(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Tarea, "validar", staticmethod(lambda *args: False))
    monkeypatch.setattr(Categoria, "obtener_del_usuario", classmethod(lambda cls, uid: [categoria_demo()]))
    respuesta = sesion_iniciada.post(
        "/tareas/crear",
        data={"titulo": "Mi tarea", "descripcion": "corta", "categoria_id": "2", "prioridad": "Alta", "fecha_limite": "2026-10-20"},
    )
    assert respuesta.status_code == 400
    assert "Mi tarea" in respuesta.get_data(as_text=True)


def test_crear_tarea_correcta(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Tarea, "validar", staticmethod(lambda *args: True))
    monkeypatch.setattr(Tarea, "crear", classmethod(lambda cls, datos: 3))
    respuesta = sesion_iniciada.post(
        "/tareas/crear",
        data={"titulo": "Mi tarea", "descripcion": "Descripción suficiente", "categoria_id": "2", "prioridad": "Alta", "fecha_limite": "2026-10-20"},
    )
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/tareas/3")


def test_no_permite_ver_tarea_ajena(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Tarea, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: None))
    respuesta = sesion_iniciada.get("/tareas/99")
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/dashboard")


def test_detalle_tarea_propia(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Tarea, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: tarea_demo()))
    monkeypatch.setattr(Comentario, "obtener_de_tarea", classmethod(lambda cls, *args: []))
    respuesta = sesion_iniciada.get("/tareas/3")
    assert respuesta.status_code == 200
    assert "Repasar rutas" in respuesta.get_data(as_text=True)


def test_completar_tarea_propia(sesion_iniciada, monkeypatch):
    llamadas = []
    monkeypatch.setattr(Tarea, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: tarea_demo()))
    monkeypatch.setattr(Tarea, "completar", classmethod(lambda cls, *args: llamadas.append(args)))
    respuesta = sesion_iniciada.post("/tareas/3/completar")
    assert respuesta.status_code == 302
    assert llamadas


def test_borrar_tarea_propia(sesion_iniciada, monkeypatch):
    llamadas = []
    monkeypatch.setattr(Tarea, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: tarea_demo()))
    monkeypatch.setattr(Tarea, "borrar", classmethod(lambda cls, *args: llamadas.append(args)))
    respuesta = sesion_iniciada.post("/tareas/3/borrar")
    assert respuesta.status_code == 302
    assert llamadas


def test_lista_categorias(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Categoria, "obtener_del_usuario", classmethod(lambda cls, uid: [categoria_demo()]))
    respuesta = sesion_iniciada.get("/categorias")
    assert respuesta.status_code == 200
    assert "Estudios" in respuesta.get_data(as_text=True)


def test_crear_categoria_correcta(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Categoria, "validar", staticmethod(lambda *args: True))
    monkeypatch.setattr(Categoria, "crear", classmethod(lambda cls, datos: 2))
    respuesta = sesion_iniciada.post("/categorias/crear", data={"nombre": "Estudios"})
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/categorias")


def test_no_borra_categoria_con_tareas(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Categoria, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: categoria_demo(2)))
    respuesta = sesion_iniciada.post("/categorias/2/borrar")
    assert respuesta.status_code == 302


def test_detalle_categoria(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Categoria, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: categoria_demo(1)))
    monkeypatch.setattr(Tarea, "obtener_por_categoria", classmethod(lambda cls, *args: [tarea_demo()]))
    respuesta = sesion_iniciada.get("/categorias/2")
    assert respuesta.status_code == 200
    assert "Estudiar Flask" in respuesta.get_data(as_text=True)


def test_crear_comentario(sesion_iniciada, monkeypatch):
    llamadas = []
    monkeypatch.setattr(Tarea, "obtener_por_id_y_usuario", classmethod(lambda cls, *args: tarea_demo()))
    monkeypatch.setattr(Comentario, "validar", staticmethod(lambda texto: True))
    monkeypatch.setattr(Comentario, "crear", classmethod(lambda cls, datos: llamadas.append(datos)))
    respuesta = sesion_iniciada.post("/tareas/3/comentarios", data={"contenido": "Buen avance"})
    assert respuesta.status_code == 302
    assert llamadas[0]["tarea_id"] == 3


def test_perfil_muestra_usuario(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Usuario, "obtener_por_id", classmethod(lambda cls, uid: usuario_demo()))
    respuesta = sesion_iniciada.get("/perfil")
    assert respuesta.status_code == 200
    assert "mauricio@example.com" in respuesta.get_data(as_text=True)


def test_actualizar_perfil(sesion_iniciada, monkeypatch):
    monkeypatch.setattr(Usuario, "validar_perfil", staticmethod(lambda *args: True))
    monkeypatch.setattr(Usuario, "actualizar", classmethod(lambda cls, datos: 1))
    respuesta = sesion_iniciada.post(
        "/perfil/actualizar",
        data={"nombre": "Mauricio", "apellido": "Flores", "email": "nuevo@example.com"},
    )
    assert respuesta.status_code == 302
    with sesion_iniciada.session_transaction() as sesion:
        assert sesion["usuario_nombre"] == "Mauricio"
