import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="library"
)

cursor = conexion.cursor()

sql = """
INSERT INTO usuarios(nombre, correo)
VALUES(%s, %s)
"""

valores = ("Prueba", "prueba@gmail.com")

cursor.execute(sql, valores)

conexion.commit()

print("Usuario insertado correctamente")