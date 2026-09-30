# Registro e inicio de sesión seguro

Aplicación Flask con arquitectura MVC para registrar cuentas, autenticar usuarios y proteger el panel. Las contraseñas se almacenan exclusivamente como hashes de Bcrypt.

## Requisitos

- Python 3.11
- MySQL
- Dependencias de `requirements.txt`

## Instalación

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Asigna en `.env` valores reales para MySQL y una clave aleatoria larga en `SECRET_KEY`. Importa `schema.sql` en MySQL y ejecuta `py server.py`.

También puede instalarse con Pipenv usando `pipenv install`; el bloqueo se genera con `pipenv lock` cuando Pipenv esté disponible.

## Estructura

- `flask_app/controllers/usuarios.py`: rutas, CSRF, sesión y flujo de autenticación.
- `flask_app/models/usuario.py`: validación y consultas parametrizadas.
- `flask_app/config/mysqlconnection.py`: conexión PyMySQL.
- `flask_app/templates/`: vistas Bootstrap/Jinja.
- `schema.sql`: base de datos y tabla con email único.
- `resources/ERD/esquema_loginreg.svg`: diagrama de la tabla.

## Seguridad

- Bcrypt genera y comprueba hashes, incluido el salt.
- Las consultas usan parámetros enlazados.
- La sesión conserva solamente `account_id`, usa cookie HttpOnly y SameSite=Lax.
- Los formularios que modifican estado incluyen un token CSRF.
- El cierre de sesión exige `POST` y el panel exige una sesión válida.

## Respuestas de comprensión

1. El hashing es unidireccional; el cifrado se puede revertir con una clave.
2. Una contraseña en texto plano expone la cuenta si se filtra la base de datos.
3. Bcrypt es un algoritmo lento y adaptativo para hashear contraseñas.
4. `generate_password_hash()` produce un hash con salt.
5. `check_password_hash()` compara una contraseña con su hash.
6. Bcrypt incorpora el salt dentro del hash resultante.
7. `.env` separa la configuración sensible del código.
8. Evita publicar credenciales y claves privadas.
9. Se guarda únicamente el identificador de la cuenta autenticada.
10. Se redirige al inicio de sesión con un mensaje.
11. Impide que dos cuentas compartan el mismo correo.
12. El modelo valida datos y accede a persistencia.
13. El controlador coordina solicitudes, modelo, sesión y respuestas.
14. La plantilla presenta los datos HTML al usuario.
