from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("unati2.html")

@app.route("/health")
def health():
    return render_template("health.html")

@app.route("/healthpredict")
def healthpredict():
    return render_template("healthpredict.html")

if __name__ == "__main__":
    app.run(debug=True)
