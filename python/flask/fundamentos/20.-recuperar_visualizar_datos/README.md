# Recuperar y visualizar mascotas

En este dispositivo el entorno y MySQL ya estan preparados. Consulta
[la guia local](../GUIA_MYSQL.md) para ejecutar el trabajo y abrir Workbench.

Ejercicio 20: MySQL devuelve diccionarios, los classmethods de `Mascota`
los convierten en objetos y Flask los envia como `todas_mascotas` a Jinja2.
Incluye solo el contenido principal (nombre, tipo y color) y la consolidacion
(ID, created_at y updated_at), sin desafio ni CSS. La plantilla usa HTML
sencillo en espanol con viewport, sin frameworks ni recursos externos.

## Preparacion (PowerShell)

Desde esta carpeta, con Python 3.9 o superior y MySQL instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con tu configuracion local. Nunca publiques ese archivo.
Las variables del entorno tienen prioridad sobre `.env`, que se carga desde
la carpeta de `mysqlconnection.py`. MYSQL_PORT debe ser un entero.
El usuario `skillnest` debe existir y tener permiso SELECT en `primera_flask`.
El script no crea usuarios ni configura claves.

En MySQL Workbench conecta con un usuario con permisos para crear la base,
abre `schema.sql` mediante File > Open SQL Script y ejecuta el script completo.
Usa UTF-8 para conservar el color de Firulais. El script crea `primera_flask`
y `mascotas` sin DROP y agrega Firulais, Michi, Luna, Nala y Coco solo si no
existe la combinacion nombre/tipo/color. Puedes ejecutarlo tres veces sin
duplicar estas filas; no sobrescribe datos existentes de los ejercicios 19/21.

```powershell
.\.venv\Scripts\python.exe app.py
```

## Rutas y pruebas

- `http://127.0.0.1:5000/`: todas las mascotas, ordenadas por ID.
- Las rutas desconocidas, incluida la antigua `/mascotas/perros`, devuelven 404.
- Sin filas se muestra un estado vacio; un error MySQL devuelve HTML con estado 503, no una lista vacia ni detalles sensibles.
- `query_db` devuelve lista para SELECT, ID para INSERT, None para otras consultas y False ante errores PyMySQL de consulta. Cierra la conexion despues de salir del cursor. Los errores al conectar se propagan al handler.

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Las pruebas simulan la conexion: no requieren servidor MySQL ni modifican datos.
Cubren ID, fechas, estados vacios, autoescaping y errores 503 genericos.
Verifican que la ruta eliminada responda 404 sin consultar MySQL y que no
exista `get_by_tipo`. Para la integracion real, usa Flask `test_client` con
el `.env` local y GET `/`, sin importar el schema ni modificar datos.
