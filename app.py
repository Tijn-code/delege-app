
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "delege_secret"

sports = ["hardlopen", "kracht_boven", "kracht_onder", "padel"]

def is_allowed(chosen, last_done):
    if chosen == "hardlopen":
        if last_done.get("hardlopen", 3) <= 2:
            return False
        if last_done.get("kracht_onder", 3) <= 2:
            return False
        if last_done.get("padel", 3) <= 2:
            return False
        return True
    elif chosen == "kracht_boven":
        if last_done.get("kracht_boven", 3) <= 1:
            return False
        return True
    elif chosen == "kracht_onder":
        if last_done.get("kracht_onder", 3) <= 1:
            return False
        if last_done.get("hardlopen", 3) <= 1:
            return False
        if last_done.get("padel", 3) <= 1:
            return False
        return True
    elif chosen == "padel":
        return True
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

@app.route("/")
def index():
    return render_template("index_buttons.html", sports=sports)

@app.route("/start/<sport>")
def start(sport):
    session["chosen"] = sport
    return redirect(url_for("vragen"))

@app.route("/vragen", methods=["GET", "POST"])
def vragen():
    if request.method == "POST":
        antwoorden = {}
        for sport in sports:
            antwoorden[sport] = int(request.form.get(sport, 3))
        session["answers"] = antwoorden
        return redirect(url_for("resultaat"))

    return render_template("vragen_pagina.html", sports=sports)

@app.route("/resultaat")
def resultaat():
    gekozen = session.get("chosen", "onbekend")
    antwoorden = session.get("answers", {})
    toegestaan = is_allowed(gekozen, antwoorden)
    suggesties = suggest_alternatives(gekozen, antwoorden)
    return render_template("resultaat.html", gekozen=gekozen, toegestaan=toegestaan, suggesties=suggesties)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
