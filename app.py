from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Hersteltijden per sportcombinatie in uren
# Hersteltijden per sportcombinatie in uren volgens de opgegeven tabel
#    Sport vandaag \ Laatste keer   Hardlopen  Kracht boven  Kracht onder  Padel
#    -----------------------------------------------------------------------------
#    Hardlopen                       48           12             48          36
#    Kracht boven                    6            48             6           12
#    Kracht onder                    48           6              72          24
#    Padel                           12           6              24          24

hersteluren = {
    "hardlopen": {"hardlopen": 48, "kracht_boven": 24, "kracht_onder": 48, "padel": 24},
    "kracht_boven": {"hardlopen": 24, "kracht_boven": 48, "kracht_onder": 24, "padel": 24},
    "kracht_onder": {"hardlopen": 48, "kracht_boven": 24, "kracht_onder": 48, "padel": 24},
    "padel": {"hardlopen": 24, "kracht_boven": 24, "kracht_onder": 24, "padel": 24},
    "hardlopen":    {"hardlopen": 48, "kracht_boven": 12, "kracht_onder": 48, "padel": 36},
    "kracht_boven": {"hardlopen": 6,  "kracht_boven": 48, "kracht_onder": 6,  "padel": 12},
    "kracht_onder": {"hardlopen": 48, "kracht_boven": 6,  "kracht_onder": 72, "padel": 24},
    "padel":        {"hardlopen": 12, "kracht_boven": 6,  "kracht_onder": 24, "padel": 24},
}

def is_toegestaan(gekozen, antwoorden):
    for sport, antwoord in antwoorden.items():
        verschil = 0 if antwoord == '0' else 24 if antwoord == '1' else 48
    """Check of de gekozen sport mag worden uitgevoerd.

    `antwoorden` bevat het aantal uur sinds de gebruiker elke sport voor het
    laatst heeft gedaan.
    """
    for sport, uren_str in antwoorden.items():
        try:
            verschil = int(uren_str)
        except (TypeError, ValueError):
            verschil = 0

        vereist = hersteluren[gekozen][sport]
        if verschil < vereist:
            return False
    return True

def suggesties(gekozen, antwoorden):
    """Bepaal welke andere sporten wel kunnen op basis van de antwoorden."""
    mogelijke = []
    for sport in hersteluren:
        if sport == gekozen:
            continue
        toegestaan = True
        for ander, antwoord in antwoorden.items():
            verschil = 0 if antwoord == '0' else 24 if antwoord == '1' else 48
        for ander, uren_str in antwoorden.items():
            try:
                verschil = int(uren_str)
            except (TypeError, ValueError):
                verschil = 0
            if verschil < hersteluren[sport][ander]:
                toegestaan = False
                break
        if toegestaan:
            mogelijke.append(sport)
    return mogelijke

@app.route("/")
def index():
    return render_template("index_buttons.html")

@app.route("/vragen", methods=["GET", "POST"])
def vragen():
    keuze = request.values.get("keuze", "")
    return render_template("vragen_pagina.html", keuze=keuze)

@app.route("/resultaat", methods=["POST"])
def resultaat():
    try:
        gekozen = request.form.get("keuze", "")
        if gekozen not in hersteluren:
            return render_template("resultaat.html", advies="Ongeldige sportkeuze."), 400

        antwoorden = {
            "hardlopen": request.form.get("hardlopen", "2"),
            "kracht_boven": request.form.get("kracht_boven", "2"),
            "kracht_onder": request.form.get("kracht_onder", "2"),
            "padel": request.form.get("padel", "2"),
            "hardlopen": request.form.get("hardlopen", "0"),
            "kracht_boven": request.form.get("kracht_boven", "0"),
            "kracht_onder": request.form.get("kracht_onder", "0"),
            "padel": request.form.get("padel", "0"),
        }

        toegestaan = is_toegestaan(gekozen, antwoorden)
        alternatieven = suggesties(gekozen, antwoorden)

        if toegestaan:
            advies = f"Je kunt vandaag {gekozen.replace('_', ' ')} doen."
        elif alternatieven:
            opties = ", ".join(a.replace('_', ' ') for a in alternatieven)
            advies = f"Geen {gekozen.replace('_', ' ')} vandaag. Kies eventueel: {opties}."
        else:
            advies = f"Geen {gekozen.replace('_', ' ')} vandaag. Rust nog even uit."

        return render_template("resultaat.html", advies=advies)
    except Exception as e:
        return f"Er trad een fout op: {str(e)}", 500

# Voor Render.com of lokaal draaien
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
