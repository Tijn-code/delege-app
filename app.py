
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "delege_secret"

sports = ["hardlopen", "kracht_boven", "kracht_onder", "padel"]

def is_allowed(chosen, last_done):
    forbidden = {
        "hardlopen": ["kracht_onder", "padel", "hardlopen"],
        "kracht_boven": ["kracht_boven"],
        "kracht_onder": ["kracht_onder", "hardlopen"],
        "padel": ["padel", "kracht_onder", "hardlopen"]
    }
    for sport in forbidden.get(chosen, []):
        if last_done.get(sport, 3) <= 1:
            return False
    return True

def suggest_alternatives(chosen, last_done):
    allowed = []
    for sport in sports:
        if sport != chosen and is_allowed(sport, last_done):
            if sport != "padel":
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
    session["order"] = sports.copy()  # 4 vragen incl. gekozen sport
    return redirect(url_for("vraag", idx=0))

@app.route("/vraag/<int:idx>", methods=["GET", "POST"])
def vraag(idx):
    if request.method == "POST":
        antwoord = int(request.form["antwoord"])
        vorige_sport = session["order"][idx - 1]
        session["answers"][vorige_sport] = antwoord
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
