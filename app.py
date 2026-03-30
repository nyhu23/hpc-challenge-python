from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

# Load dataset
with open("data.json") as f:
    data = json.load(f)

# HTML Template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Pest-Pesticide Finder</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input { padding: 8px; width: 300px; }
        button { padding: 8px; }
        .result { margin-top: 20px; background: #f0f0f0; padding: 15px; }
    </style>
</head>
<body>

<h2>🌱 Pest & Pesticide Recommendation System</h2>

<form method="post">
    <input type="text" name="query" placeholder="e.g. aphid on apple">
    <button type="submit">Search</button>
</form>

{% if result %}
<div class="result">
    <h3>Result:</h3>
    <p>{{ result }}</p>
</div>
{% endif %}

</body>
</html>
"""

# Matching function
def find_match(user_input):
    user_input = user_input.lower()

    matches = []

    for item in data:
        if item["crop"] in user_input and item["pest"] in user_input:
            matches.append(
                f"{item['pesticide']} (Dosage: {item['dosage']})"
            )

    if matches:
        return "<br>".join(matches)
    else:
        return "❌ No matching pesticide found."

# Route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        user_input = request.form["query"]
        result = find_match(user_input)

    return render_template_string(html, result=result)

if __name__ == "__main__":
    app.run(debug=True)