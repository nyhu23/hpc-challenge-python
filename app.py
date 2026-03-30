from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "pesticides.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def extract_pest_crop(user_input):
    user_input = user_input.lower()
    found_pest = ""
    found_crop = ""

    for item in data:
        if item["pest"] in user_input:
            found_pest = item["pest"]
        if item["crop"] in user_input:
            found_crop = item["crop"]

    return found_pest, found_crop

def find_match(user_input):
    pest, crop = extract_pest_crop(user_input)
    results = []

    if pest and crop:
        for item in data:
            if item["pest"] == pest and item["crop"] == crop:
                results.append(item["pesticide"])

    if not results and pest:
        for item in data:
            if item["pest"] == pest:
                results.append(item["pesticide"])

    return pest, crop, list(set(results))

html = """
<!DOCTYPE html>
<html>
<head>
<title>Plant Protection Database</title>
<style>
body { font-family: Arial; margin:0; background:#f3f3f3; }

.top-bar {
    background:#a6b91a;
    padding:15px;
    font-size:24px;
    color:white;
}

.nav {
    background:#6b2e1f;
    color:white;
    padding:10px;
}

.container {
    width:80%;
    margin:20px auto;
    background:white;
    padding:20px;
}

.search-box {
    display:flex;
    gap:10px;
    margin-bottom:20px;
}

input {
    flex:1;
    padding:10px;
    font-size:16px;
}

button {
    padding:10px;
    background:#6b2e1f;
    color:white;
    border:none;
    cursor:pointer;
}

button:hover {
    background:#4e2116;
}

.result-row {
    padding:10px;
    border-bottom:1px solid #ddd;
}

.no-result {
    color:red;
    margin-top:10px;
}
</style>
</head>

<body>

<div class="top-bar">Plant Protection Database</div>
<div class="nav">Home > Authorisations</div>

<div class="container">

<form method="post">
<div class="search-box">
<input type="text" name="query" placeholder="e.g. aphids on apple" required>
<button type="submit">Search</button>
</div>
</form>

{% if results %}
{% for item in results %}
<div class="result-row">
<b>Pest:</b> {{ pest }} <br>
<b>Crop:</b> {{ crop if crop else "Not specified" }} <br>
<b>Pesticide:</b> {{ item }}
</div>
{% endfor %}
{% elif searched %}
<div class="no-result">No match found</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    pest = ""
    crop = ""
    searched = False

    if request.method == "POST":
        user_input = request.form["query"]
        pest, crop, results = find_match(user_input)
        searched = True

    return render_template_string(
        html,
        results=results,
        pest=pest,
        crop=crop,
        searched=searched
    )
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)