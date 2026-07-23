from flask import Flask, render_template

app = Flask(__name__)

pokedex = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta/Veneno", "imagen": "bulbasaur.png", "poder": 45, "altura": "0.7m", "peso": "6.9kg"},
    {"id": 4, "nombre": "Charmander", "tipo": "Fuego", "imagen": "charmander.png", "poder": 39, "altura": "0.6m", "peso": "8.5kg"},
    {"id": 7, "nombre": "Squirtle", "tipo": "Agua", "imagen": "squirtle.png", "poder": 44, "altura": "0.5m", "peso": "9.0kg"},
    {"id": 25, "nombre": "Pikachu", "tipo": "Eléctrico", "imagen": "pikachu.png", "poder": 35, "altura": "0.4m", "peso": "6.0kg"},
    {"id": 39, "nombre": "Jigglypuff", "tipo": "Normal/Hada", "imagen": "jigglypuff.png", "poder": 115, "altura": "0.5m", "peso": "5.5kg"},
    {"id": 52, "nombre": "Meowth", "tipo": "Normal", "imagen": "meowth.png", "poder": 40, "altura": "0.4m", "peso": "4.2kg"},
    {"id": 54, "nombre": "Psyduck", "tipo": "Agua", "imagen": "psyduck.png", "poder": 50, "altura": "0.8m", "peso": "19.6kg"},
    {"id": 94, "nombre": "Gengar", "tipo": "Fantasma/Veneno", "imagen": "gengar.png", "poder": 60, "altura": "1.5m", "peso": "40.5kg"},
    {"id": 95, "nombre": "Onix", "tipo": "Roca/Tierra", "imagen": "onix.png", "poder": 35, "altura": "8.8m", "peso": "210.0kg"},
    {"id": 143, "nombre": "Snorlax", "tipo": "Normal", "imagen": "snorlax.png", "poder": 160, "altura": "2.1m", "peso": "460.0kg"}
]

@app.route("/pokemon")
def mostrar_todos():
    return render_template("index.html", pokemons=pokedex, titulo="Todos los Pokémon")

@app.route("/pokemon/<int:numero>")
def mostrar_por_numero(numero):
    for p in pokedex:
        if p["id"] == numero:
            return render_template("index.html", pokemons=[p], titulo=p["nombre"])
    mensaje = f'No pudimos encontrar información sobre el Pokémon #{numero} en nuestra Pokédex'
    return pokemon_no_encontrado(mensaje)

@app.route("/pokemon/<nombre>")
def mostrar_por_nombre(nombre):
    for p in pokedex:
        if p["nombre"].lower() == nombre.lower():
            return render_template("index.html", pokemons=[p], titulo=p["nombre"])
    mensaje = f'No pudimos encontrar información sobre "{nombre}" en nuestra Pokédex'
    return pokemon_no_encontrado(mensaje)

@app.route("/pokemon/cantidad/<int:cantidad>")
def mostrar_cantidad(cantidad):
    seleccion = pokedex[:cantidad]
    return render_template("index.html", pokemons=seleccion, titulo=f"Primeros {cantidad} Pokémon")

def pokemon_no_encontrado(mensaje: str):
    """Función simple para renderizar la página 404 con un mensaje."""
    return render_template("404.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)