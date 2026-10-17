from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/result", methods=["POST"])
def result():
    name = request.form["username"]
    mood = request.form["mood"]
    language = request.form["language"]

    try:
        age = int(request.form["age"])
    except (ValueError, KeyError):
        age = None

    return render_template(
        "result.html",
        name=name,
        mood=mood,
        language=language,
        age=age,
    )


if __name__ == "__main__":
    app.run(debug=True)
