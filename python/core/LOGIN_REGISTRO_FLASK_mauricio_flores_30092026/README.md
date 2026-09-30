# Registro e inicio de sesión con Flask

Aplicación Flask conectada a MySQL que permite registrar usuarios, iniciar sesión,
mostrar una página protegida y cerrar la sesión.

## Instalación

1. Abre MySQL Workbench y ejecuta el archivo `base_de_datos.sql`.
2. Revisa los datos de conexión en `flask_app/config/mysqlconnection.py`.
   El proyecto usa el usuario `root` y la contraseña `root`.
3. Abre una terminal dentro de la carpeta del proyecto.
4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta la aplicación:

   ```bash
   python server.py
   ```

6. Abre `http://127.0.0.1:5000` en el navegador.

## Validaciones incluidas

- Nombre y apellido: solo letras y mínimo 2 caracteres.
- Correo electrónico: formato válido y sin registros repetidos.
- Contraseña: mínimo 8 caracteres, una mayúscula y un número.
- Confirmación de contraseña igual a la contraseña.
- Inicio de sesión con correo y contraseña válidos.
- Página de éxito protegida mediante sesión.
- Cierre de sesión y bloqueo de acceso luego de salir.
