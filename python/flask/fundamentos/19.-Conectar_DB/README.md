# 19. Conectar Flask con MySQL

En este dispositivo el entorno y MySQL ya estan preparados. Consulta
[la guia local](../GUIA_MYSQL.md) para ejecutar el trabajo y abrir Workbench.

Proyecto de lectura con POO: Flask llama a `Mascota` y `Usuario`; sus
classmethods consultan MySQL mediante `MySQLConnection` y convierten filas
DictCursor en objetos. Incluye solo el contenido principal (`Mascota.get_all`)
y la consolidacion (`Usuario.get_all`), sin desafio ni CSS. Jinja muestra
HTML sencillo en espanol, con viewport y autoescaping, sin frameworks.

## Preparacion (PowerShell)

Desde esta carpeta, con Python 3.9+ instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

No hace falta activar el entorno: los comandos usan su Python directamente.
Las instrucciones permiten preparar otra maquina desde cero.
El `.env` real es local y no se versiona. No sobrescribas uno ya configurado.

En MySQL Workbench, conecta como administrador, abre `schema.sql` mediante
**File > Open SQL Script** y ejecuta el archivo completo. Crea
`primera_flask`, `mascotas` y `usuarios` sin borrar ni actualizar datos.
Incluye cinco mascotas exactas del enunciado y tres usuarios ficticios.
El script usa UTF-8 para conservar el color de Firulais tal como en el enunciado.
Puedes ejecutar el script tres veces: `NOT EXISTS` evita repetir mascotas
por nombre/tipo/color y usuarios por email. No elimina duplicados previos;
ejecuta los schemas secuencialmente, no al mismo tiempo.

Configura en Workbench el usuario MySQL `skillnest` (el schema no crea cuentas)
y concede al menos SELECT sobre `primera_flask.*`. En `.env`, ajusta
`MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE`.
Los valores por defecto son los de `.env.example`, con clave vacia.
Las variables del proceso tienen prioridad sobre `.env`, que se busca junto
a `mysqlconnection.py`. Un argumento `db` explicito prevalece sobre
`MYSQL_DATABASE`. Si cambias la base, debes preparar sus tablas tambien.

## Ejecutar

```powershell
.\.venv\Scripts\python.exe app.py
```

- `http://127.0.0.1:5000/`: listado de mascotas o estado vacio.
- `http://127.0.0.1:5000/usuarios`: consolidacion del modelo Usuario.
- Ruta desconocida (incluida la antigua `/mascotas/1`): pagina HTML 404.
- Fallo de conexion/consulta: pagina HTML 503 con consejos, sin secretos.

El servidor de desarrollo se inicia sin debug; no es un servidor de produccion.
Cada consulta cierra primero el cursor y luego la conexion. `query_db`
devuelve lista para SELECT, lastrowid para INSERT, None para otros comandos
y False ante errores PyMySQL de consulta. Los modelos distinguen False de
una lista vacia y lanzan MySQLError; Flask lo maneja como 503.
No se registran SQL, parametros ni detalles de excepciones.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Las pruebas usan mocks, no necesitan servidor MySQL ni credenciales.
Cubren listados, estados vacios, usuarios, errores/503, autoescaping,
modelos y contrato/cierre de la conexion. Verifican que las rutas de detalle
eliminadas respondan 404 sin consultar MySQL y que no exista `get_by_id`.
Con el `.env` local y MySQL disponible, comprueba mediante GET `/` y `/usuarios`
con Flask `test_client`, sin importar el schema ni modificar datos.
