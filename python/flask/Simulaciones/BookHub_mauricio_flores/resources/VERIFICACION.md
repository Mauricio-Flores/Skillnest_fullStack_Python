# Verificación de la entrega

Fecha: 1 de octubre de 2026.

## Entorno utilizado

- Python 3.12.
- Flask 3.1.2 y PyMySQL 1.1.2.
- Flask-Bcrypt 1.0.1 con Bcrypt 5.0.0.
- MySQL Server **8.0.46**, con tablas InnoDB y codificación utf8mb4.
- Chromium headless 154 para comprobar la interfaz.

La comprobación se realizó contra MySQL real. El script `bookhub.sql` se ejecutó
correctamente; la aplicación no utiliza SQLite ni datos simulados en memoria.

## Pruebas de integración

Resultado: **26 casos aprobados**.

```text
..........................                                               [100%]
26 passed in 6.62s
```

Los casos comprueban:

- Protección de seis rutas privadas cuando no hay sesión.
- Registro, sesión y hash Bcrypt verificable.
- Nombres, correo, confirmación y longitud de contraseña inválidos.
- Correo único, incluyendo diferencias de mayúsculas.
- Login correcto, contraseña incorrecta y cierre de sesión.
- Token CSRF obligatorio, incluidos tokens con caracteres no ASCII.
- Prohibición de borrar o cerrar sesión con una petición GET.
- Creación, lectura, edición precargada y eliminación de libros.
- Validaciones de título, autor, género, fechas y descripción en backend.
- Edición inválida sin cambios en la base.
- Acceso a libros de la comunidad sin permisos para editarlos o borrarlos.
- Protección contra un `usuario_id` falsificado en el formulario.
- Favoritos aislados por cuenta, conteo, usuarios relacionados y prevención de duplicados.
- Eliminación en cascada de favoritos al borrar el libro.
- Escape HTML de Jinja2 y consultas SQL parametrizadas.
- Limpieza de sesión cuando el usuario ya no existe.

Los archivos de prueba están en `tests/`. Usan exclusivamente `bookhub_pruebas`.

## Flujo de la interfaz

Se ejecutó la aplicación localmente y se usaron los formularios del navegador para
crear dos cuentas ficticias, publicar libros y verificar las acciones principales.
Se generaron **19 capturas reales**, disponibles en `resources/capturas/`.

- Registro inválido muestra mensajes del backend y conserva los textos ingresados.
- Registro exitoso e inicio de sesión redirigen a Mis Libros.
- La lista distingue los libros propios de los de la comunidad.
- Los formularios guardan y actualizan datos en MySQL.
- Borrar solicita confirmación y elimina el registro.
- El detalle muestra todos los campos y los usuarios que marcaron el libro.
- Agregar un favorito actualiza el contador y oculta el botón.
- Mis Favoritos muestra el libro de la cuenta actual.
- Acceder a la URL de edición de un libro ajeno devuelve HTTP 403.
- La creación inválida rechaza título corto, fecha pasada y descripción corta.
- El login inválido muestra el error; el válido recupera los registros guardados.
- La vista de 390 × 844 permite abrir el menú y desplazar las tablas dentro de su contenedor.
- El documento móvil mide 390 px de ancho: no desborda horizontalmente la página completa.
- No se detectaron errores de JavaScript en el flujo.

## Revisión visual y ejecución local

Se revisaron visualmente el ERD y las pantallas principales: acceso, listados,
detalle, edición, validaciones y celular. También se comprobó la sintaxis de los
módulos Python.

Para ejecutarlo en otro computador se debe instalar los requisitos, iniciar MySQL,
importar el SQL y configurar `.env` siguiendo el README. La entrega no incluye las
credenciales locales ni el entorno de pruebas utilizado para las capturas.
