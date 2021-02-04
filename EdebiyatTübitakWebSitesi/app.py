from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.core import IntegerField
import email_validator
import pickle
import pandas as pd
from nltk.corpus import stopwords

stopwords = stopwords.words("turkish")

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "edebi-zeka"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
age_model = pickle.load(open("templates/models/donem-model.bin", "rb"))
century_model = pickle.load(open("templates/models/yuzyil-model.bin", "rb"))
poet_model = pickle.load(open("templates/models/sair-model.bin", "rb"))
class FeedbackForm(Form):
    name = StringField("Ad:", validators=[validators.Length(min=3, max=20, message="Girdiğiniz değer 3-20 arası karakter içermelidir.")])
    surname = StringField("Soyad:", validators=[validators.Length(min=3, max=30, message="Girdiğiniz değer 3-30 arası karakter içermelidir.")])
    email = StringField("E-posta Adresi:", validators=[validators.email(message="Lütfen geçerli bir e-posta adresi giriniz.")])
    rating = IntegerField("Edebi Zeka'ya 10 Üzerinden Kaç Puan Verirsiniz?", validators=[validators.NumberRange(min=0, max=10, message="Girdiğiniz değer 1-10 arasında olmalıdır.")])
    feature = StringField("Edebi Zeka'da Görmek İstediğiniz Özellik:", validators=[validators.Length(min=3, max=50, message="Girdiğiniz değer 3-50 arası karakter içermelidir.")])
    extra = StringField("Eklemek İstedikleriniz:", validators=[validators.Length(min=10, max=500, message="Girdiğiniz değer 10-500 arası karakter içermelidir.")])

class PredictForm(Form):
    dize = StringField("Dize:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])

class FailureFeedback(Form):
    dize = StringField("Girdiğiniz Dize:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalı.")])
    expected_output = StringField("Beklediğiniz Çıktı:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalı.")])
    real_output = StringField("Çıktı:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalı.")])


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rehber")
def main_page():
    return render_template("rehber.html")

@app.route("/siirde-donem-tahmini", methods=["GET", "POST"])
def siirde_donem_tahmini():
    predict_form = PredictForm(request.form)

    if request.method == "POST" and predict_form.validate():

        donem_kazanim = {"Tanzimat":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Servetifünun":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Fecri Ati":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Milli Edebiyat":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "1923-1960 Arası Toplumcu Serbest Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Hececiler":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Hisarcılar":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Maviciler":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Milli Edebiyat Anlayışını Yansıtan Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Cumhuriyet Dönemi Saf Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "1960 Sonrası Toplumcu Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "1980 Sonrası Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Garip Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "Metafizik Anlayışını Öne Çıkaran Şiir":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea.",
                        "İkinci Yeni":"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Natus tempore totam cum sapiente delectus odit quisquam quas repellendus dicta fugiat tempora, praesentium vero, ullam ratione quidem error iste veritatis. Similique. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iste nesciunt hic rerum pariatur ut voluptates possimus, aperiam autem nulla? Rem repudiandae dicta voluptatum officiis in consequuntur obcaecati alias quam saepe. Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum accusantium, recusandae repudiandae cumque veritatis, a eligendi molestias omnis id molestiae iusto facilis animi dolores est ducimus consectetur quo dolore ea."}

        dize = predict_form.dize.data
        dize_for_pred = dize
        for i in dize_for_pred:
            if i in stopwords:
                dize_for_pred.replace(i, "")

        dize_for_pred = dize_for_pred.lower()
        dize_for_pred = pd.DataFrame([dize_for_pred], columns=["Dize"])
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("[^\w\s]", "")
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("\d", "")
        output = age_model.predict(dize_for_pred)[0]
        kazanim = donem_kazanim[output]
        predictor = "dönem"
        cursor = mysql.connection.cursor()
        sorgu = "Insert into tahminler(input, output, predictor) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (dize, output, predictor))
        mysql.connection.commit()

        cursor.close()

        return render_template("siirde-donem-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, pred_headline=output + " Döneminin Özellikleri", form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", kazanim=kazanim)

    else:
        return render_template("siirde-donem-tahmini.html", form=predict_form)

@app.route("/siirde-yuzyil-tahmini", methods=["GET", "POST"])
def siirde_yuzyil_tahmini():

    predict_form = PredictForm(request.form)

    if request.method == "POST" and predict_form.validate(): 

        donem_cikarimi = {"19. yüzyıl":["Tanzimat"],
                        "20. yüzyılın 1. yarısı":["Cumhuriyet Dönemi Saf Şiir", "1923-1960 Arası Toplumcu Serbest Şiir", "Milli Edebiyat Anlayışını Yansıtan Şiir", "Servetifünun", "Fecri Ati", "Milli Edebiyat", "Hececiler", "Garip Şiir"],
                        "20. yüzyılın 2. yarısı":["1923-1960 Arası Toplumcu Serbest Şiir", "Maviciler", "İkinci Yeni", "Metafizik Anlayışını Öne Çıkaran Şiir", "Hisarcılar", "1960 Sonrası Toplumcu Şiir", "1980 Sonrası Şiir", "Garip Şiir"]}

        dize = predict_form.dize.data
        dize_for_pred = dize
        for i in dize_for_pred:
            if i in stopwords:
                dize_for_pred.replace(i, "")

        dize_for_pred = dize_for_pred.lower()
        dize_for_pred = pd.DataFrame([dize_for_pred], columns=["Dize"])
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("[^\w\s]", "")
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("\d", "")
        output = century_model.predict(dize_for_pred)[0]
        cikarim = donem_cikarimi[output]
        if cikarim == ["Tanzimat"]:
            cikarim = "Tanzimat"
        else:
            cikarim = ", ".join(cikarim).strip(",")
        predictor = "yüzyıl"
        cursor = mysql.connection.cursor()
        sorgu = "Insert into tahminler(input, output, predictor) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (dize, output, predictor))
        mysql.connection.commit()

        cursor.close()

        return render_template("siirde-yuzyil-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", cikarim=output + " ile kesişen edebi dönemler: " + cikarim) 
    
    else:
        return render_template("siirde-yuzyil-tahmini.html", form=predict_form)

@app.route("/siirde-sair-tahmini", methods=["GET", "POST"])
def siirde_sair_tahmini():

    predict_form = PredictForm(request.form)

    if request.method == "POST" and predict_form.validate(): 

        poet_info = {
            "Edip Cansever":["İkinci Yeni", "20. yüzyılın 2. yarısı"],
            "Turgut Uyar":["İkinci Yeni", "20. yüzyılın 2. yarısı"],
            "Cemal Süreya":["İkinci Yeni", "20. yüzyılın 2. yarısı"],
            "Ece Ayhan":["İkinci Yeni", "20. yüzyılın 2. yarısı"],
            "Sezai Karakoç":["İkinci Yeni", "20. yüzyılın 2. yarısı"],
            "Oktay Rıfat":["Garip Şiir", "20. yüzyılın 2. yarısı"],
            "Melih Cevdet Anday":["Garip Şiir", "20. yüzyılın 2. yarısı"],
            "Orhan Veli Kanık":["Garip Şiir", "20. yüzyılın 1. yarısı"],
            "Halit Fahri Ozansoy":["Hececiler", "20. yüzyılın 1. yarısı"], 
            "Faruk Nafiz Çamlıbel":["Hececiler", "20. yüzyılın 1. yarısı"],
            "Mehmet Akif Ersoy":["Milli Edebiyat", "20. yüzyılın 1. yarısı"],
            "Yahya Kemal":["Milli Edebiyat", "20. yüzyılın 1. yarısı"],
            "Mehmet Emin Yurdakul":["Milli Edebiyat", "20. yüzyılın 1. yarısı"],
            "Ziya Gökalp":["Milli Edebiyat", "20. yüzyılın 1. yarısı"],
            "Ahmet Haşim":["Fecri Ati", "20. yüzyılın 1. yarısı"],
            "Süleyman Nazif":["Servetifünun", "20. yüzyılın 1. yarısı"],
            "Cenap Şahabettin":["Servetifünun", "20. yüzyılın 1. yarısı"],
            "Tevfik Fikret":["Servetifünun", "20. yüzyılın 1. yarısı"],
            "Recaizade Mahmud Ekrem":["Tanzimat", "19. yüzyıl"],
            "Ziya Paşa":["Tanzimat", "19. yüzyıl"],
            "Abdülhak Hamit Tarhan":["Tanzimat", "19. yüzyıl"],
            "Namık Kemal":["Tanzimat", "19. yüzyıl"],
            "İbrahim Şinasi":["Tanzimat", "19. yüzyıl"],
            "Murathan Mungan":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı"],
            "Enis Batur":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı"],
            "Haydar Ergülen":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı"],
            "Ahmet Arif":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı"],
            "İsmet Özel":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı"],
            "Ataol Behramoğlu":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı"],
            "Yavuz Bülent Bakiler":["Hisarcılar", "20. yüzyılın 2. yarısı"],
            "Mehmet Çınarlı":["Hisarcılar", "20. yüzyılın 2. yarısı"],
            "Erdem Beyazıt":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı"],
            "Cahit Zarifoğlu":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı"],
            "Arif Nihat Asya":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı"],
            "Kemalettin Kamu":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı"],
            "Orhan Şaik Gökyay":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı"],
            "Ahmet Kutsi Tecer":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı"],
            "Attila İlhan":["Maviciler", "20. yüzyılın 2. yarısı"],
            "Ceyhun Atuf Kansu":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 2. yarısı"],
            "Nazım Hikmet":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 1. yarısı"],
            "Ziya Osman Saba":["Yedi Meşaleciler", "20. yüzyılın 1. yarısı"],
            "Özdemir Asaf":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 2. yarısı"],
            "Cahit Sıtkı Tarancı":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı"],
            "Ahmet Hamdi Tanpınar":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı"],
            "Necip Fazıl Kısakürek":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı"]
        }
        
        dize = predict_form.dize.data
        dize_for_pred = dize
        for i in dize_for_pred:
            if i in stopwords:
                dize_for_pred.replace(i, "")

        dize_for_pred = dize_for_pred.lower()
        dize_for_pred = pd.DataFrame([dize_for_pred], columns=["Dize"])
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("[^\w\s]", "")
        dize_for_pred["Dize"] = dize_for_pred["Dize"].str.replace("\d", "")
        output = poet_model.predict(dize_for_pred)[0]
        poet_age = poet_info[output][0]
        poet_century = poet_info[output][1]
        predictor = "şair"
        cursor = mysql.connection.cursor()
        sorgu = "Insert into tahminler(input, output, predictor) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (dize, output, predictor))
        mysql.connection.commit()

        cursor.close()

        return render_template("siirde-sair-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, pred_headline = "Şaire Ait Bilgiler", form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", poet_age="Şairin Eser Ürettiği Dönem: " + poet_age, poet_century="Şairin Eser Ürettiği Yüzyıl: " + poet_century) 
    
    else:
        return render_template("siirde-sair-tahmini.html", form=predict_form)

@app.route("/planlanan-ozellikler")
def planlanan_ozellikler():
    return render_template("planlanan-ozellikler.html")

@app.route("/veri-seti")
def veri_seti():
    return render_template("veri-seti.html")

@app.route("/algoritma-secimi")
def algoritma_secimi():
    return render_template("algoritma-secimi.html")

@app.route("/hakkimizda")
def about():
    return render_template("about.html")

@app.route("/iletisim")
def iletisim():
    return render_template("contact.html")

@app.route("/tesekkurler")
def tesekkurler():
    return render_template("thanks.html")

@app.route("/ticket", methods=["GET", "POST"])
def ticket():
    failure_form = FailureFeedback(request.form)

    if request.method == "POST" and failure_form.validate():
        dize = failure_form.dize.data
        expected_output = failure_form.expected_output.data
        real_output = failure_form.real_output.data

        cursor = mysql.connection.cursor()
        sorgu = "Insert into hata_bildirimleri(input, expected_output, real_output) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (dize, expected_output, real_output))
        mysql.connection.commit()

        cursor.close()

        return redirect(url_for("tesekkurler"))

    else:
        return render_template("ticket.html", form=failure_form)

@app.route("/geri-bildirim-formu", methods=["GET", "POST"])
def geri_bildirim_formu():
    form = FeedbackForm(request.form)

    if request.method == "POST" and form.validate():

        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        rating = form.rating.data
        feature = form.feature.data
        extra = form.extra.data

        cursor = mysql.connection.cursor()
        sorgu = "Insert into geri_bildirim_formu(name,surname,email,rating,feature,extra) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu, (name,surname,email,rating,feature,extra))
        mysql.connection.commit()

        cursor.close()
        return redirect(url_for("tesekkurler"))

    else:
        return render_template("geri-bildirim-formu.html", form = form)
if __name__ == "__main__":
    app.run(debug=True)