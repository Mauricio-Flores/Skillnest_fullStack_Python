# Consultas con datos variables

En este dispositivo el entorno y MySQL ya estan preparados. Consulta
[la guia local](../GUIA_MYSQL.md) para ejecutar el trabajo y abrir Workbench.

Proyecto de solo lectura con Flask, POO y MySQL. Cada consulta variable usa
placeholders de PyMySQL y un diccionario separado, nunca concatenacion SQL.
No incluye CRUD adicional: UPDATE en el enunciado es un ejemplo educativo.
Incluye solo el contenido principal (`get_all` y `get_by_id`) y la consolidacion
(`get_by_name`), sin desafio ni CSS.

## Preparacion (PowerShell)

Desde esta carpeta, con Python y MySQL instalados:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con tu configuracion local. No publiques ese archivo. Las variables
del entorno tienen prioridad sobre `.env`; MYSQL_PORT debe ser un entero.
No se requiere activar el entorno virtual.

En MySQL Workbench abre la conexion local, usa **File > Open SQL Script** para
abrir `schema.sql` y ejecuta el script completo. Usa una cuenta con permisos para
crear la base/tabla e insertar el seed. Configura `skillnest` (o tu usuario) con
permiso SELECT sobre `primera_flask.mascotas` para ejecutar la aplicacion.
El script agrega cinco mascotas sin borrar ni sobrescribir registros: cada
insercion comprueba NOT EXISTS por nombre/tipo/color y se puede repetir.
Si eliges otra MYSQL_DATABASE, prepara alli la tabla; el schema usa primera_flask.

```powershell
.\.venv\Scripts\python.exe app.py
```

## Rutas y comprobaciones

- `http://127.0.0.1:5000/`: listado con enlaces a fichas.
- `/mascota/<int:id>`: todos los atributos; usa un ID real del listado.
- `/mascota/nombre/<path:nombre>`: ficha por nombre, admite barras. Si hay nombres repetidos, devuelve el menor ID.
- `/mascota/999999` y `/mascota/nombre/NoExiste`: 404 si no existen.
- Las rutas desconocidas, incluidas las antiguas `/mascotas/tipo/...`, devuelven 404.
- Sin MySQL disponible: 503 HTML con consejos, sin detalles sensibles.

Los IDs pueden variar si ya habia datos. Los valores de rutas se deben codificar
como URL. Jinja escapa los datos al generar HTML; no se utiliza el filtro safe.
Las plantillas usan HTML sencillo en espanol con viewport, sin estilos,
frameworks ni servicios externos.

## Pruebas sin MySQL

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Los tests simulan la conexion y verifican modelos, parametros, errores, cierre
de recursos y respuestas HTML. Tambien comprueban que las rutas por tipo
eliminadas respondan 404 sin consultar MySQL y que no exista `get_by_tipo`.
Para la integracion real, usa Flask `test_client` con el `.env` local y GET
al listado, a una ficha por ID y a una ficha por nombre. No requiere importar
el schema ni modificar datos.
