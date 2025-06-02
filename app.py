
from flask import Flask, render_template, request

app = Flask(__name__)

# Hersteltijden in uren
hersteltijden = {
    "hardlopen":    {"hardlopen": 48, "kracht_boven": 12, "kracht_onder": 48, "padel": 36},
    "kracht_boven": {"hardlopen": 6, "kracht_boven": 48, "kracht_onder": 6, "padel": 12},
    "kracht_onder": {"hardlopen": 48, "kracht_boven": 6, "kracht_onder": 72, "padel": 24},
    "padel":        {"hardlopen": 12, "kracht_boven": 6, "kracht_onder": 24, "padel": 24}
}

# Categorie naar uren
categorie_naar_uren = {
    "0": 6,   # Vandaag
    "1": 24,  # Gisteren
    "2": 48   # Eergisteren of langer
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/advies", methods=["POST"])
def advies():
    gekozen = request.form["keuze"]
    advies_mogelijk = True

    for sport in ["hardlopen", "kracht_boven", "kracht_onder", "padel"]:
        tijd_cat = request.form.get(sport, "2")
        uren_geleden = categorie_naar_uren.get(tijd_cat, 48)
        vereiste_rust = hersteltijden[gekozen][sport]

        if uren_geleden < vereiste_rust:
            advies_mogelijk = False
            break

    if gekozen == "padel":
        advies = "Paddelen kan, maar plan dit altijd van tevoren."
    elif advies_mogelijk:
        advies = f"Je kunt vandaag {gekozen.replace('_', ' ')} doen."
    else:
        advies = f"Beter geen {gekozen.replace('_', ' ')} vandaag."

    return render_template("advies.html", advies=advies)
