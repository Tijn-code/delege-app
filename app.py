
from flask import Flask, render_template, request

app = Flask(__name__)

hersteltijden = {
    "hardlopen":    {"hardlopen": 48, "kracht_boven": 12, "kracht_onder": 48, "padel": 36},
    "kracht_boven": {"hardlopen": 6, "kracht_boven": 48, "kracht_onder": 6, "padel": 12},
    "kracht_onder": {"hardlopen": 48, "kracht_boven": 6, "kracht_onder": 72, "padel": 24},
    "padel":        {"hardlopen": 12, "kracht_boven": 6, "kracht_onder": 24, "padel": 24}
}

categorie_naar_uren = {
    "0": 6,
    "1": 24,
    "2": 48
}

@app.route("/")
def index():
    return render_template("index_buttons.html")

@app.route("/vragen", methods=["POST"])
def vragen():
    keuze = request.form.get("keuze")
    return render_template("vragen_pagina.html", keuze=keuze)

@app.route("/resultaat", methods=["POST"])
def resultaat():
    keuze = request.form.get("keuze")
    advies_mogelijk = True

    for sport in ["hardlopen", "kracht_boven", "kracht_onder", "padel"]:
        tijd_cat = request.form.get(sport, "2")
        uren_geleden = categorie_naar_uren.get(tijd_cat, 48)
        vereist = hersteltijden[keuze][sport]
        if uren_geleden < vereist:
            advies_mogelijk = False
            break

    if keuze == "padel":
        advies = "Paddelen kan, maar plan dit altijd van tevoren."
    elif advies_mogelijk:
        advies = f"Je kunt vandaag {keuze.replace('_', ' ')} doen."
    else:
        advies = f"Beter geen {keuze.replace('_', ' ')} vandaag."

    return render_template("resultaat.html", advies=advies)
