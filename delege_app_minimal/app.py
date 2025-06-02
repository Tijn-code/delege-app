
from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        sport = request.form.get("sport")
        # Vereenvoudigd: altijd zelfde advies tonen
        result = {
            "advies": f"Je hebt gekozen voor: {sport}",
            "alternatief": "Vandaag kun je ook een andere sport kiezen die minder belastend is."
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
