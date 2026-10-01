# Relaciones de BookHub

| Relación | Cardinalidad | Implementación |
|---|---|---|
| usuarios → libros | 1 a 0..N | Un usuario publica libros; cada libro tiene un único dueño. `libros.usuario_id` referencia `usuarios.id`. |
| usuarios → favoritos | 1 a 0..N | Cada favorito corresponde a un usuario. `favoritos.usuario_id` referencia `usuarios.id`. |
| libros → favoritos | 1 a 0..N | Un libro puede tener favoritos de muchas cuentas. `favoritos.libro_id` referencia `libros.id`. |
| usuarios ↔ libros (favoritos) | N a M | La tabla intermedia `favoritos` tiene clave primaria compuesta `(usuario_id, libro_id)`. |

Todas las claves foráneas usan `ON DELETE CASCADE` y `ON UPDATE CASCADE`.
El correo de usuario es único. El total de favoritos se calcula a partir de la tabla
intermedia; no se guarda como un contador separado.

## Archivos

- `ERD.png`: imagen del diagrama.
- `ERD.svg`: diagrama vectorial.
- `ERD.drawio`: versión editable en diagrams.net.
- `bookhub.sql`: script fuente de la estructura de MySQL.

La clave `password` guarda exclusivamente el hash Bcrypt. `fecha` es el campo
de fecha del formulario; `created_at` y `updated_at` son marcas de tiempo de auditoría.
