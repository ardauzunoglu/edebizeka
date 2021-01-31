from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rehber")
def main_page():
    return render_template("rehber.html")

@app.route("/hakkimizda")
def about():
    return render_template("about.html")

@app.route("/siir-tahlili")
def siir_tahlili():
    return render_template("donem-tahmini.html")

@app.route("/roman-tahlili")
def roman_tahlili():
    return render_template("roman-tahlili.html")

@app.route("/planlanan-ozellikler")
def planlanan_ozellikler():
    return render_template("planlanan-ozellikler.html")

@app.route("/iletisim")
def iletisim():
    return render_template("contact.html")

@app.route("/geri-bildirim-formu")
def geri_bildirim_formu():
    return render_template("geri-bildirim-formu.html")
if __name__ == "__main__":
    app.run(debug=True)