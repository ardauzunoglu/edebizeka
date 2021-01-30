from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ana-sayfa")
def main_page():
    return render_template("ana-sayfa.html")

@app.route("/hakkimizda")
def about():
    return render_template("about.html")

@app.route("/siir-tahlili")
def donem_tahmini():
    return render_template("donem-tahmini.html")

@app.route("/buyuk-unlu-uyumu-kontrolu")
def buyuk_unlu_uyumu_kontrolu():
    return render_template("buyuk-unlu-uyumu-kontrolu.html")

@app.route("/gelistirme-asamasinda-olan-ozellikler")
def gelistirme_asamasinda_olan_ozellikler():
    return render_template("gelistirme-asamasinda-olan-ozellikler.html")

@app.route("/iletisim")
def iletisim():
    return render_template("contact.html")

@app.route("/geri-bildirim-formu")
def geri_bildirim_formu():
    return render_template("geri-bildirim-formu.html")
if __name__ == "__main__":
    app.run(debug=True)