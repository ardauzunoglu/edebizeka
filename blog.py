from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    sozluk = {"adi":"Tübitak Projesi", "gelistirici":"Arda Uzunoğlu", "konu":"Doğal Dil İşleme"}
    return render_template("index.html", dict=sozluk)

if __name__ == "__main__":
    app.run(debug=True)