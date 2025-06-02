
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "delege_secret"

sports = ["hardlopen", "kracht_boven", "kracht_onder", "padel"]

def is_allowed(chosen, last_done):
    tijd = last_done

    if chosen == "hardlopen":
        if tijd.get("hardlopen", 3) <= 2:
            return False
        if tijd.get("kracht_onder", 3) <= 2:
            return False
        if tijd.get("padel", 3) <= 2:
            return False
        return True

    elif chosen == "kracht_boven":
        if tijd.get("kracht_boven", 3) <= 1:
            return False
        return True

    elif chosen == "kracht_onder":
        if tijd.get("kracht_onder", 3) <= 1:
            return False
        if tijd.get("hardlopen", 3) <= 1:
            return False
        if tijd.get("padel", 3) <= 1:
            return False
        return True

    elif chosen == "padel":
        return True  # Padel mag altijd

    return False

def suggest_alternatives(chosen, last_done):
    allowed = []
    for sport in sports:
        if sport != chosen and sport != "padel" and is_allowed(sport, last_done):
            allowed.append((sport, last_done.get(sport, 3)))
    if not allowed:
        return []
    allowed.sort(key=lambda x: -x[1])
    best_score = allowed[0][1]
    best_options = [sport for sport, score in allowed if score == best_score]
    return best_options

@app.route("/", methods=["GET"])
def index():
    return render_template("index_buttons.html", sports=sports)

@app.route("/start/<sport>")
def start(sport):
    session["chosen"] = sport
    session["answers"] = {}
    session["order"] = sports.copy()
    return redirect(url_for("vraag", idx=0))

@app.route("/vraag/<int:idx>", methods=["GET", "POST"])
def vraag(idx):
    if request.method == "POST":
        antwoord = int(request.form["antwoord"])
        if idx > 0:
            vorige_sport = session["order"][idx - 1]
            session["answers"][vorige_sport] = antwoord
        return redirect(url_for("vraag", idx=idx + 1))

    if idx >= len(session["order"]):
        return redirect(url_for("resultaat"))

    huidige_sport = session["order"][idx]
    vraagtekst = f"Wanneer heb je voor het laatst {huidige_sport.replace('_', ' ')} gedaan?"
    return render_template("vraag_enkel.html", sport=huidige_sport, vraagtekst=vraagtekst, idx=idx)

@app.route("/resultaat")
def resultaat():
    gekozen = session["chosen"]
    antwoorden = session["answers"]
    toegestaan = is_allowed(gekozen, antwoorden)
    suggesties = suggest_alternatives(gekozen, antwoorden)
    return render_template("resultaat.html", gekozen=gekozen, toegestaan=toegestaan, suggesties=suggesties)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
