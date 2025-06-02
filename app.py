
from flask import Flask, render_template, request
import os

app = Flask(__name__)

hersteluren = {
    "hardlopen": {"hardlopen": 48, "kracht_boven": 24, "kracht_onder": 48, "padel": 24},
    "kracht_boven": {"hardlopen": 24, "kracht_boven": 48, "kracht_onder": 24, "padel": 24},
    "kracht_onder": {"hardlopen": 48, "kracht_boven": 24, "kracht_onder": 48, "padel": 24},
    "padel": {"hardlopen": 24, "kracht_boven": 24, "kracht_onder": 24, "padel": 24}
}

def is_toegestaan(gekozen, antwoorden):
    for sport, antwoord in antwoorden.items():
        verschil = 0 if antwoord == '0' else 24 if antwoord == '1' else 48
        vereist = hersteluren[gekozen][sport]
        if verschil < vereist:
            return False
    return True

def suggesties(gekozen, antwoorden):
    mogelijke = []
    for sport in hersteluren:
        if sport == "padel" and gekozen != "padel":
            continue
        if sport == gekozen:
            continue
        toegestaan = True
        for ander, antwoord in antwoorden.items():
            verschil = 0 if antwoord == '0' else 24 if antwoord == '1' else 48
            if verschil < hersteluren[sport][ander]:
                toegestaan = False
                break
        if toegestaan:
            mogelijke.append(sport)
    return mogelijke

@app.route("/")
def index():
    return render_template("index_buttons.html")

@app.route("/vragen")
def vragen():
    keuze = request.args.get("keuze", "")
    return render_template("vragen_pagina.html", keuze=keuze)

@app.route("/resultaat", methods=["POST"])
def resultaat():
    try:
        gekozen = request.form.get("keuze", "")
        antwoorden = {
            "hardlopen": request.form.get("hardlopen", "2"),
            "kracht_boven": request.form.get("kracht_boven", "2"),
            "kracht_onder": request.form.get("kracht_onder", "2"),
            "padel": request.form.get("padel", "2")
        }

        toegestaan = is_toegestaan(gekozen, antwoorden)
        alternatieven = suggesties(gekozen, antwoorden)
        return render_template("resultaat.html", gekozen=gekozen, toegestaan=toegestaan, suggesties=alternatieven)
    except Exception as e:
        return f"Er trad een fout op: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
