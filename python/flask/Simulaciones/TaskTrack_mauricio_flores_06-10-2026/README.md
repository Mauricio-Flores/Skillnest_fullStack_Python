# TaskTrack — Gestión de Tareas

Proyecto Flask con arquitectura MVC para registrar usuarios y administrar tareas personales mediante categorías.

## Funcionalidades

- Registro e inicio de sesión con contraseña cifrada mediante Bcrypt.
- Sesiones y rutas protegidas.
- CRUD completo de tareas.
- CRUD de categorías con cantidad de tareas.
- Detalle de tarea y comentarios.
- Validaciones de formularios y mensajes flash.
- Permisos por propietario en consultas, edición y eliminación.
- Búsqueda por título y filtro por estado.
- Marcar tareas como completadas.
- Próximas tareas ordenadas por fecha.
- Resumen por estado y prioridad.
- Interfaz adaptable a celular y computador.

## Estructura MVC

```text
TaskTrack_mauricio_flores_06-10-2026/
├── bd/tasktrack.sql
├── flask_app/
│   ├── config/mysqlconnection.py
│   ├── controllers/
│   ├── models/
│   ├── static/css/style.css
│   └── templates/
├── resources/
├── tests/
├── .env.example
├── requirements.txt
└── server.py
```

## Instalación

1. Abre `bd/tasktrack.sql` en MySQL Workbench y ejecuta todo el archivo.
2. Abre una terminal en la carpeta del proyecto.
3. Crea y activa un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

5. El proyecto ya incluye un `.env` de desarrollo. Modifica `DB_PASSWORD` si tu contraseña de MySQL no es `root`.
6. Ejecuta la aplicación:

```bash
python server.py
```

7. Abre `http://127.0.0.1:5000`.

## Pruebas

```bash
pytest -q
```

Las pruebas incluidas validan autenticación, permisos, formularios y rutas usando dobles de prueba, por lo que no modifican la base de datos real.
