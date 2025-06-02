
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

sports = ["hardlopen", "kracht_boven", "kracht_onder", "padel"]

def is_allowed(chosen, last_done):
    # Verbodslijst per sport
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
    # Sorteer op hoe lang geleden (hoogst eerst)
    allowed.sort(key=lambda x: -x[1])
    beste_score = allowed[0][1]
    beste_opties = [sport for sport, dagen in allowed if dagen == beste_score]
    return beste_opties

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gekozen = request.form.get("sport")
        return redirect(url_for('vragen', sport=gekozen))
    return render_template("index.html", sports=sports)

@app.route("/vragen/<sport>", methods=["GET", "POST"])
def vragen(sport):
    andere = [s for s in sports if s != sport]
    vragenlijst = [f"Wanneer heb je voor het laatst {s.replace('_', ' ')} gedaan?" for s in andere]
    if request.method == "POST":
        last_done = {}
        for s in andere:
            value = int(request.form.get(s))
            last_done[s] = value
        toegestaan = is_allowed(sport, last_done)
        suggesties = suggest_alternatives(sport, last_done)
        return render_template("resultaat.html", gekozen=sport, toegestaan=toegestaan, suggesties=suggesties)
    return render_template("vragen.html", sport=sport, vragen=zip(andere, vragenlijst))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
