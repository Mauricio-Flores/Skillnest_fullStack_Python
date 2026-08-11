from flask import Flask, render_template

# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route("/listas")
def renderizar_listas():
    # Lista de números
    numeros = [7, 15, 22]

    # Lista de diccionarios
    listado_estudiantes = [
        {
            "nombre": "Florencia",
            "edad": 25
        },
        {
            "nombre": "Valentina",
            "edad": 30
        },
        {
            "nombre": "José",
            "edad": 27
        },
        {
            "nombre": "Patricio",
            "edad": 21
        }
    ]

    return render_template(
        "listas.html",
        numeros=numeros,
        estudiantes=listado_estudiantes
    )

@app.route("/juegos")

def render_lista():
    lista_videojuego = [
        {
            "nombre":"Minecraft",
            "plataforma":"PC",
            "anio_lanzamiento":2011
        },
        {
            "nombre": "The Legend of Zelda: Breath of the Wild",
            "plataforma": "Nintendo Switch",
            "anio_lanzamiento": 2017
        },
        {
            "nombre": "God of War",
            "plataforma": "PlayStation 4",
            "anio_lanzamiento": 2018
        },
        {
            "nombre": "Elden Ring",
            "plataforma": "Multiplataforma",
            "anio_lanzamiento": 2022
        },
        {
            "nombre": "Halo: Combat Evolved",
            "plataforma": "Xbox",
            "anio_lanzamiento": 2001
        },
        {
            "nombre": "Red Dead Redemption 2",
            "plataforma": "PlayStation 4 / Xbox One",
            "anio_lanzamiento": 2018
        }
    ]
    return render_template(
        "index.html",
        juegos=lista_videojuego
    )

# Opcional: para ejecutar el servidor directamente desde este archivo
if __name__ == "__main__":
    app.run(debug=True)