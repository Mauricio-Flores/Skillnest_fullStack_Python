from flask import Flask, render_template, request

app = Flask(__name__)

datos = [
    {"nombre": "Spotify", "usuarios": "515M", "fundado": 2006, "pais": "Suecia", "imagen": "spotify.png"},
    {"nombre": "Netflix", "usuarios": "247M", "fundado": 1997, "pais": "EE.UU.", "imagen": "netflix.png"},
    {"nombre": "YouTube", "usuarios": "2.5B", "fundado": 2005, "pais": "EE.UU.", "imagen": "youtube.png"},
    {"nombre": "Twitch", "usuarios": "140M", "fundado": 2011, "pais": "EE.UU.", "imagen": "twitch.png"},
    {"nombre": "TikTok", "usuarios": "1.7B", "fundado": 2016, "pais": "China", "imagen": "tiktok.png"},
    {"nombre": "Instagram", "usuarios": "2.35B", "fundado": 2010, "pais": "EE.UU.", "imagen": "instagram.png"},
    {"nombre": "Discord", "usuarios": "250M", "fundado": 2015, "pais": "EE.UU.", "imagen": "discord.png"},
]


def convertir_usuarios(valor):
    """Convierte '515M' o '2.5B' en un número para poder ordenar."""
    valor = valor.upper()
    if valor.endswith("B"):
        return float(valor[:-1]) * 1000
    return float(valor[:-1])


@app.route("/tabla")
def tabla():
    pais = request.args.get("pais", "todos")
    orden = request.args.get("orden", "nombre")
    direccion = request.args.get("direccion", "asc")

    plataformas = datos
    if pais != "todos":
        plataformas = [p for p in datos if p["pais"] == pais]

    if orden == "usuarios":
        plataformas = sorted(plataformas, key=lambda p: convertir_usuarios(p["usuarios"]))
    elif orden == "fundado":
        plataformas = sorted(plataformas, key=lambda p: p["fundado"])
    elif orden == "pais":
        plataformas = sorted(plataformas, key=lambda p: p["pais"])
    else:
        plataformas = sorted(plataformas, key=lambda p: p["nombre"])

    if direccion == "desc":
        plataformas = list(reversed(plataformas))

    paises = sorted(set(p["pais"] for p in datos))

    return render_template(
        "index.html",
        plataformas=plataformas,
        paises=paises,
        pais=pais,
        orden=orden,
        direccion=direccion,
    )


if __name__ == "__main__":
    app.run(debug=True)
