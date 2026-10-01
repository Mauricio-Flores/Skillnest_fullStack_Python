# BookHub — Mauricio Flores

Aplicación Flask basada en el wireframe entregado. Permite registrarse, iniciar sesión,
publicar libros, ver los libros de la comunidad y agregarlos a favoritos.
El diseño usa Bootstrap y CSS sencillo. Los archivos de Bootstrap están incluidos,
por lo que la interfaz no depende de un CDN al ejecutarse.

## Tecnologías y estructura MVC

- Flask y Jinja2: rutas y plantillas.
- MySQL y PyMySQL: almacenamiento y consultas parametrizadas.
- Flask-Bcrypt: contraseñas protegidas con Bcrypt.
- Bootstrap 5.3.3: formularios, tablas y navegación adaptable.

```text
BookHub_mauricio_flores/
├── server.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── flask_app/
│   ├── __init__.py
│   ├── config/mysqlconnection.py
│   ├── controllers/           # Usuarios, libros y favoritos
│   ├── models/                # Consultas y validaciones
│   ├── utils/seguridad.py      # Sesiones, protección de rutas y CSRF
│   ├── templates/             # Vistas Jinja2
│   └── static/                # CSS, imagen genérica y Bootstrap
├── resources/
│   ├── bookhub.sql            # Script para MySQL Workbench
│   ├── ERD.png                # Diagrama de la base de datos
│   ├── ERD.svg
│   ├── ERD.drawio              # Diagrama editable
│   ├── ERD.md
│   ├── wireframe.png
│   └── capturas/              # Capturas reales de funcionamiento
└── tests/                     # Pruebas con una base separada
```

## Ejecutar en Windows / VS Code

Requisitos: Python 3.10 o superior, MySQL Server 8.0 o superior y MySQL Workbench.
Workbench es el cliente: también debe estar instalado e iniciado MySQL Server.

1. Descomprime el ZIP y abre `BookHub_mauricio_flores` en VS Code.
2. Abre una terminal en esa carpeta y ejecuta:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. En MySQL Workbench abre tu conexión local, abre `resources/bookhub.sql`
   y ejecuta el script completo con el botón del rayo. Se crea la base `bookhub`
   y sus tres tablas. El script no borra los datos existentes.
4. Copia la configuración de ejemplo:

   ```powershell
   Copy-Item .env.example .env
   .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
   ```

5. Abre `.env`: reemplaza `SECRET_KEY` por la clave generada y `DB_PASSWORD`
   por tu contraseña de MySQL. Ajusta `DB_USER`, `DB_PORT` o `DB_HOST` si tu
   conexión usa otros valores. No cambies el nombre `bookhub` si ejecutaste el SQL incluido.
6. Inicia Flask:

   ```powershell
   .\.venv\Scripts\python.exe server.py
   ```

7. Abre **http://localhost:5000/**. Registra una cuenta para comenzar.

La base entregada comienza vacía. Registra dos cuentas desde la aplicación y crea
libros en cada una para comprobar las secciones propias y de la comunidad.
Las cuentas que aparecen en las capturas son datos ficticios utilizados en la prueba.

En macOS/Linux usa `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`,
`cp .env.example .env` y `.venv/bin/python server.py`. La configuración de MySQL es la misma.

## Funciones y reglas del wireframe

- Registro: nombre y apellido de 2 a 45 caracteres, correo válido y único,
  contraseña y confirmación iguales. Se exige un mínimo de 8 caracteres y un
  máximo de 72 bytes por el límite de Bcrypt. Las contraseñas nunca se guardan en texto plano.
- Registro e inicio de sesión exitosos llevan a `/libros`.
- Mis Libros muestra solo los libros de la cuenta actual con Ver, Editar y Borrar.
- Libros de la Comunidad muestra libros publicados por otras cuentas, con su dueño
  y el total real de favoritos. Las cuentas autenticadas pueden verlos.
- Nuevo y Editar: todos los campos son obligatorios; título y autor mínimo 2 caracteres,
  género de la lista, descripción mínimo 10 caracteres y fecha válida.
- **La fecha no puede ser pasada**, tal como indica la nota del wireframe. Los títulos
  antiguos pueden ingresarse usando una fecha actual para el ejercicio. Al editar
  un registro cuya fecha ya pasó también debe actualizarse su fecha.
- El formulario de edición se carga con los valores guardados.
- Detalle muestra autor, género, dueño, fecha, descripción y usuarios que lo marcaron
  como favorito. Se usa una portada genérica como en el wireframe; no se requiere carga de imágenes.
- Agregar a favoritos crea una relación usuario–libro. El botón desaparece cuando
  el libro ya está marcado. La clave primaria compuesta impide duplicados.
- Mis Favoritos muestra solo los favoritos de la cuenta actual.
- Eliminar un libro elimina también sus favoritos mediante `ON DELETE CASCADE`.
- Las rutas privadas exigen una sesión válida. Se verifica el dueño tanto en el
  controlador como en el `WHERE` de las consultas de edición y eliminación.
- Los errores y éxitos se muestran con mensajes flash; los formularios inválidos
  conservan los campos de texto, pero nunca rellenan la contraseña.
- Crear, editar, borrar, agregar favoritos y cerrar sesión usan POST con token CSRF.

No se implementan funciones BONUS. El texto del encabezado sigue el wireframe;
no se agrega una función de comentarios porque no hay un flujo de comentarios indicado.

## Rutas

| Método | Ruta | Función |
|---|---|---|
| GET | `/` | Login y registro |
| POST | `/registro` | Crear cuenta |
| POST | `/login` | Iniciar sesión |
| POST | `/logout` | Cerrar sesión |
| GET | `/libros` | Libros propios y comunidad |
| GET | `/explorar` | Libros de la comunidad |
| GET / POST | `/libros/nuevo` | Formulario y creación |
| GET | `/libros/<id>` | Detalle del libro |
| GET / POST | `/libros/editar/<id>` | Formulario y actualización del dueño |
| POST | `/libros/eliminar/<id>` | Eliminación del dueño |
| GET | `/favoritos` | Favoritos del usuario |
| POST | `/favoritos/agregar/<id>` | Agregar un libro a favoritos |

## ERD y capturas

El ERD está en `resources/ERD.png`, con versiones SVG y Draw.io editables.
Puedes abrir `ERD.drawio` en diagrams.net o importar el SQL en MySQL Workbench
y usar **Database → Reverse Engineer** para crear un modelo de Workbench.
Consulta `resources/ERD.md` para las relaciones y `resources/capturas/README.md`
para la descripción de cada captura.

## Pruebas

Las pruebas usan MySQL real y una base independiente llamada `bookhub_pruebas`.
Nunca deben ejecutarse contra la base de uso normal.

1. Ejecuta en Workbench:

   ```sql
   CREATE DATABASE IF NOT EXISTS bookhub_pruebas
       CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Instala `requirements-dev.txt` y, con `.env` configurado, ejecuta:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
   .\.venv\Scripts\python.exe -m pytest -q
   ```

El usuario de MySQL debe tener permisos para crear tablas en `bookhub_pruebas`.
Las pruebas limpian únicamente los registros de esa base al comenzar cada caso.
El resultado de la verificación realizada para esta entrega está en `resources/VERIFICACION.md`.

## Problemas frecuentes

- **No module named flask:** instala los requisitos y ejecuta `server.py` con el
  mismo Python de `.venv`, usando los comandos de arriba.
- **Access denied:** revisa usuario y contraseña de MySQL en `.env`.
- **Unknown database:** ejecuta completo `resources/bookhub.sql` en Workbench.
- **Can't connect to MySQL:** inicia el servicio de MySQL y comprueba el puerto.
- **Configura SECRET_KEY:** genera una clave y reemplaza el valor de ejemplo en `.env`.

El archivo `.env`, las contraseñas locales y el entorno virtual no se incluyen en la entrega.
