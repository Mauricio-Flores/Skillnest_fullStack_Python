# Capturas de funcionamiento

Capturas reales tomadas durante la ejecución local con Flask y MySQL 8.0.46.
Los usuarios y registros son datos ficticios creados para la verificación.

| Archivo | Función demostrada |
|---|---|
| [01_login_registro.png](01_login_registro.png) | Pantalla de registro e inicio de sesión. |
| [02_validacion_registro.png](02_validacion_registro.png) | Validación real del backend: nombre, apellido, correo y contraseñas inválidos. |
| [03_registro_exitoso.png](03_registro_exitoso.png) | Registro correcto, sesión iniciada y redirección a Mis Libros. |
| [04_nuevo_libro.png](04_nuevo_libro.png) | Formulario completo para crear un libro, con fecha actual. |
| [05_libro_creado.png](05_libro_creado.png) | Mensaje flash de creación y libro guardado en Mis Libros. |
| [06_mis_libros_comunidad.png](06_mis_libros_comunidad.png) | Libros propios con Ver, Editar y Borrar; libros de Ana con solo Ver. |
| [07_detalle_libro.png](07_detalle_libro.png) | Detalle de un libro de la comunidad antes de agregarlo a favoritos. |
| [08_favorito_agregado.png](08_favorito_agregado.png) | Favorito guardado, usuario visible, contador actualizado y botón oculto. |
| [09_mis_favoritos.png](09_mis_favoritos.png) | Mis Favoritos muestra el libro marcado por la cuenta actual. |
| [10_editar_libro.png](10_editar_libro.png) | Formulario de edición precargado con los datos guardados. |
| [11_libro_actualizado.png](11_libro_actualizado.png) | Autor corregido y mensaje flash de actualización. |
| [12_libro_eliminado.png](12_libro_eliminado.png) | El libro eliminado desaparece y se confirma con un mensaje flash. |
| [13_permiso_denegado.png](13_permiso_denegado.png) | Acceso rechazado al intentar editar un libro de otra cuenta mediante su URL. |
| [14_validacion_libro.png](14_validacion_libro.png) | El backend rechaza título corto, fecha pasada y descripción corta. Conserva los datos. |
| [15_explorar.png](15_explorar.png) | Explorar muestra dueño y total de favoritos de los libros de la comunidad. |
| [16_cerrar_sesion.png](16_cerrar_sesion.png) | Cerrar sesión vuelve al inicio y confirma el cierre con un mensaje flash. |
| [17_login_incorrecto.png](17_login_incorrecto.png) | Inicio de sesión con contraseña incorrecta rechazado por el backend. |
| [18_login_exitoso.png](18_login_exitoso.png) | Inicio de sesión correcto recupera los libros guardados y los favoritos. |
| [19_vista_celular.png](19_vista_celular.png) | Vista móvil con menú desplegable y tablas con desplazamiento horizontal interno. |
