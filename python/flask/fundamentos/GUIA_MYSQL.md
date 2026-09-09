# Trabajos 19, 20 y 21: ejecucion local

## Estado de este dispositivo

- MySQL Community Server 8.4.9 instalado y configurado.
- Servicio Windows `SkillnestMySQL`, con inicio automatico.
- Servidor accesible solo desde `127.0.0.1:3306`, no desde la red local.
- Base compartida `primera_flask`: cinco mascotas y tres usuarios ficticios.
- Cada trabajo tiene su propio `.venv` con las dependencias instaladas.
- Cada trabajo tiene un `.env` local, excluido de Git, con su conexion.
- Usuario de las aplicaciones: `skillnest`, con permisos de lectura y escritura
  solo sobre `primera_flask`. No se utiliza root desde Flask.

Las tres carpetas son aplicaciones independientes que comparten la misma base,
tal como indican las lecciones. Los cambios hechos desde Workbench aparecen al
recargar la pagina; no hay que modificar las listas de Python.

## Iniciar un trabajo

Abre una terminal dentro de cualquiera de estas carpetas:

| Carpeta | Funcionalidad |
| --- | --- |
| `19.-Conectar_DB` | Listado de mascotas y listado de usuarios |
| `20.-recuperar_visualizar_datos` | Listado con ID y fechas |
| `21.-consultas_datos` | Consultas por ID y nombre mediante parametros |

Se conserva la parte principal y las actividades de consolidacion de los MD.
No se incluyen los desafios ni CSS: las paginas usan HTML sin estilos.

Ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre `http://127.0.0.1:5000/`. Deten el servidor con `Ctrl+C` antes de ejecutar
otro trabajo en el mismo puerto. No es necesario activar el entorno virtual.

Para ejecutar los tres simultaneamente, utiliza un puerto distinto por trabajo:

```powershell
# Desde 19.-Conectar_DB
.\.venv\Scripts\python.exe -m flask --app app run --port 5019
# Desde 20.-recuperar_visualizar_datos
.\.venv\Scripts\python.exe -m flask --app app run --port 5020
# Desde 21.-consultas_datos
.\.venv\Scripts\python.exe -m flask --app app run --port 5021
```

## Ejecutar desde VS Code

Abre en VS Code la carpeta raiz `Skillnest_fullStack_Python`, no solamente un
archivo. Python, Pylance y Python Debugger ya estan instalados en este equipo.

1. Abre **Ejecutar y depurar** con `Ctrl+Shift+D`.
2. Elige **Flask 19**, **Flask 20** o **Flask 21** en el selector superior.
3. Pulsa `F5` para depurar o `Ctrl+F5` para ejecutar sin depurar.
4. Abre la direccion correspondiente en el navegador.

| Trabajo | Direccion al ejecutar desde VS Code |
| --- | --- |
| 19 | `http://127.0.0.1:5019/` |
| 20 | `http://127.0.0.1:5020/` |
| 21 | `http://127.0.0.1:5021/` |

Cada configuracion usa el Python de su propio `.venv`, la carpeta del trabajo
y su `.env`. No necesita activar entornos ni modificar la politica de PowerShell.
Deten la ejecucion con `Shift+F5`.

Otra opcion es **Terminal > Ejecutar tarea**, y elegir **Flask 19 - Ejecutar**,
**Flask 20 - Ejecutar** o **Flask 21 - Ejecutar**. Estas tareas usan los mismos
puertos de la tabla. No ejecutes la tarea y el depurador del mismo trabajo a la
vez porque intentarian usar el mismo puerto.

Tambien puedes abrir una terminal integrada: haz clic derecho en la carpeta del
trabajo, elige **Abrir en terminal integrada**, y ejecuta
`.\.venv\Scripts\python.exe app.py`. En ese caso el puerto es **5000**.
Usa `Ctrl+C` para detenerlo.

No uses **Live Server / Go Live** para estas aplicaciones: requieren Flask y
MySQL, no solo abrir un archivo HTML. Los cambios realizados en el repositorio
son los mismos que ves en VS Code; no hay otra copia del proyecto.

## MySQL Workbench

Workbench ya estaba instalado en
`E:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe`.

Abre la conexion **Skillnest - primera_flask**. La clave esta guardada en el
almacen de credenciales de Workbench, no en `connections.xml` ni en Git.
Puedes consultar:

```sql
USE primera_flask;
SELECT * FROM mascotas;
SELECT * FROM usuarios;
```

Workbench 8.0 puede advertir que algunas herramientas administrativas no estan
certificadas para MySQL 8.4. Las aplicaciones usan PyMySQL y no dependen de
Workbench para funcionar.

## Servicio y archivos privados

Para comprobar el servidor desde PowerShell:

```powershell
Get-Service SkillnestMySQL
```

Si estuviera detenido, ejecuta en una terminal como administrador:

```powershell
Start-Service SkillnestMySQL
```

La configuracion y los datos de esta instancia estan fuera del repositorio, en
`%LOCALAPPDATA%\SkillnestMySQL`. La carpeta tiene permisos restringidos.
`my.ini` configura el servidor; `data/` contiene los datos;
`admin.cnf` contiene las credenciales administrativas locales y `app.env`
las del usuario de las aplicaciones. No publiques ni compartas estos archivos.
No borres `data/` ni reinicialices la instancia para repetir un ejercicio.

## Pruebas y otra maquina

Dentro de cada trabajo:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Estas pruebas usan mocks y no necesitan MySQL. Tras quitar los desafios y CSS,
pasaron 48 pruebas unitarias y se comprobaron las rutas restantes contra MySQL
real. Las rutas de los desafios eliminados y el antiguo CSS devuelven 404.
La base conserva las cinco mascotas y los tres usuarios; no se borraron datos
para simplificar las aplicaciones.

Para preparar otra maquina, sigue el README de cada trabajo: crea el entorno,
instala `requirements.txt`, configura tu propio `.env` desde `.env.example` e
importa `schema.sql` con una cuenta administradora. Los schemas no borran datos
y evitan duplicar las semillas al ejecutarlos secuencialmente.

Los `.venv` y las claves locales no se suben a GitHub. La configuracion de
Windows y Workbench tampoco viaja con el repositorio.
