 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
index 1b34f0a429164539522a940ab753a8f10dddfdcf..fb34c90de4ccecf2fba108e4a2d24728dcb3a7af 100644
--- a/app.py
+++ b/app.py
@@ -1,67 +1,82 @@
 
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
-        if sport == "padel" and gekozen != "padel":
-            continue
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
 
-@app.route("/vragen")
+@app.route("/vragen", methods=["GET", "POST"])
 def vragen():
-    keuze = request.args.get("keuze", "")
+    # Accept both query parameters and form data so the page works
+    # whether the keuze is submitted via GET or POST
+    keuze = request.values.get("keuze", "")
     return render_template("vragen_pagina.html", keuze=keuze)
 
 @app.route("/resultaat", methods=["POST"])
 def resultaat():
     try:
         gekozen = request.form.get("keuze", "")
+        if gekozen not in hersteluren:
+            return render_template("resultaat.html", advies="Ongeldige sportkeuze."), 400
         antwoorden = {
             "hardlopen": request.form.get("hardlopen", "2"),
             "kracht_boven": request.form.get("kracht_boven", "2"),
             "kracht_onder": request.form.get("kracht_onder", "2"),
             "padel": request.form.get("padel", "2")
         }
 
         toegestaan = is_toegestaan(gekozen, antwoorden)
         alternatieven = suggesties(gekozen, antwoorden)
-        return render_template("resultaat.html", gekozen=gekozen, toegestaan=toegestaan, suggesties=alternatieven)
+
+        # Bouw een adviesstring op basis van de berekende waarden
+        if toegestaan:
+            advies = f"Je kunt vandaag {gekozen.replace('_', ' ')} doen."
+        else:
+            if alternatieven:
+                opties = ", ".join(a.replace('_', ' ') for a in alternatieven)
+                advies = (f"Geen {gekozen.replace('_', ' ')} vandaag. "
+                          f"Kies eventueel: {opties}.")
+            else:
+                advies = (f"Geen {gekozen.replace('_', ' ')} vandaag. "
+                          "Rust nog even uit.")
+
+        return render_template("resultaat.html", advies=advies)
     except Exception as e:
         return f"Er trad een fout op: {str(e)}"
 
 if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port)
 
EOF
)
