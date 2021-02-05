from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.core import IntegerField
import email_validator
import joblib
import pandas as pd
from nltk.corpus import stopwords
import joblib

stopwords = stopwords.words("turkish")
age_model = joblib.load(open("templates/models/ez-donem.pkl", "rb"))
century_model = joblib.load(open("templates/models/ez-yuzyil.pkl", "rb"))
poet_model = joblib.load(open("templates/models/ez-sair.pkl", "rb"))
app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "edebi-zeka"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

class FeedbackForm(Form):
    name = StringField("Ad:", validators=[validators.Length(min=3, max=20, message="Girdiğiniz değer 3-20 arası karakter içermelidir.")])
    surname = StringField("Soyad:", validators=[validators.Length(min=3, max=30, message="Girdiğiniz değer 3-30 arası karakter içermelidir.")])
    email = StringField("E-posta Adresi:", validators=[validators.email(message="Lütfen geçerli bir e-posta adresi giriniz.")])
    rating = IntegerField("Edebi Zeka'ya 10 Üzerinden Kaç Puan Verirsiniz?", validators=[validators.NumberRange(min=0, max=10, message="Girdiğiniz değer 1-10 arasında olmalıdır.")])
    feature = StringField("Edebi Zeka'da Görmek İstediğiniz Özellik:", validators=[validators.Length(min=3, max=50, message="Girdiğiniz değer 3-50 arası karakter içermelidir.")])
    extra = StringField("Eklemek İstedikleriniz:", validators=[validators.Length(min=10, max=500, message="Girdiğiniz değer 10-500 arası karakter içermelidir.")])

class PredictForm(Form):
    dize = StringField("Dize:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])

class RhymeForm(Form):
    dize1 = StringField("Dize 1:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])
    dize2 = StringField("Dize 2:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])
    dize3 = StringField("Dize 3:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])
    dize4 = StringField("Dize 4:", validators=[validators.Length(min=3, message="Girdiğiniz değer 3 karakterden uzun olmalıdır.")])

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
        donem_kazanim = {"Tanzimat":"Osmanlı Devleti, Batı’nın Rönesans’la başlayıp çeşitli alanlardaki reform hareketleriyle ilerleyişine ayak uyduramamış ve 17.yy.dan sonra gerilemeye başlamıştır. Siyasi ve toplumsal hayatta ortaya çıkan bu gerileme edebiyatta da kendini göstermiştir. 3 Kasım 1839 tarihinde Mustafa Reşit Paşa tarafından Gülhane Parkı’nda okunan Tanzimat Fermanı (Gülhane Hatt-ı Humayunu) ile hem siyasi hem de edebiyat alanında yeni bir dönem başlamıştır. Tanzimat Edebiyatı, Tercüman-ı Ahval gazetesinin 1860’ta yayınlanması ile başlar. Tanzimat ile birlikte Türk edebiyatına yeni edebi türler girmiştir yine bu dönemde Batı’dan çeviriler yapılmış ve ilk örnekler verilmiştir. ",
                        "Servetifünun":"“Sanat, sanat içindir.” görüşünü benimseyen seçkin zümre edebiyatıdır. Konuşma dilinden tamamen uzaklaşılmıştır. Arapça ve Farsça dil kurallarına fazlaca yer  verilmiştir. Ayrıca eserlere, dilimizde o zamana kadar olmayan Farsça ve Arapça kelimeler de girmiştir. Din dışı konularda eser vermişlerdir. Baskı nedeniyle Tanzimatçıların kullandığı kavramları kullanmamışlar, suya sabuna dokunmayan kavramlar üzerinde dolaşmışlardır. Fransız edebiyatından etkilenmenin bir sonucu olarak batıdan “Sone”, “Terza-rima”  ve “serbest müztezat” biçimleri alınmış ve kullanılmıştır. Aruz ölçüsü kullanılmıştır, hece ölçüsü hiçbir zaman ciddiye alınmamıştır. (Hece ölçüsüyle sadece çocuk şiirleri yazılmıştır. / Tevfik Fikret – Şermin ) “Göz için kafiye” yerine “kulak için kafiye” anlayışı kabul edilmiştir.",
                        "Fecri Ati":"Servet-i Fünun dergisi 1901 yılında kapatılınca bu dergi etrafında toplanan Servet-i Fünun edebiyatçıları artık bir daha bir araya gelme imkanına sahip olamamışlardır.  Hatta basına uygulanan sansürden dolayı sanatçılar şiirlerini bile rahatça yayınlayamamışlardır. 1908 yılına kadar süren, edebiyatın bu fetret devri bu tarihte meşrutiyetin ilan edilmesiyle sona ermiştir.  Edebiyat aşığı gençler tarafından “Hilal Matbaası”nda bir toplantı yapılmıştır. 	Fecr-i Ati gerçekte bir edebi topluluk ya da bir edebi akım değildir. Bu hareket yukarıda adı geçen gençlerin birkaç toplantısıyla sınırlı kalmıştır. Gençlerin yetenekli olması, edebiyat dünyasının bu toplantıdan haberdar olmasını sağlamıştır",
                        "Milli Edebiyat":"Dönemin siyasi koşullarına paralel olarak  “Osmanlıcılık, Batıcılık, İslamcılık, Türkçülük … “ gibi bazı ideolojiler ortaya çıkmıştır. “Türkçülük”  en baskın ideoloji olmuştur. Milli Edebiyat diye adlandırılan dönemi aslında 'Milliyetçi edebiyat' olarak nitelemek daha uygundur. Tanzimat'la başlayarak birçok şair, yazar ve bilim insanı Avrupa'da esmeye başlayan milliyetçilik akımından etkilenmiş ve Osmanlı coğrafyasında bu akımın yayılmasına önayak olmuştur. Ayrıca Balkan Savaşları ve II. Meşrutiyet’in ilanı ile Osmanlıcılık fikrinin kaybolmasını ve Türkçülük fikrinin gelişmesini sağlamıştır.",
                        "1923-1960 Arası Toplumcu Serbest Şiir":"Serbest Nazım: Divan, halk ve Batı nazım şekillerinin ölçü, kafiye, mısra kümelenişi gibi kurallarını dikkate almayan, Tanzimat’tan sonra kullanılmaya başlanan, Batı’dan alınmış bir nazım şeklidir. Bu edebiyat akımının merkezinde “insan, toplum ve onun üretim ilişkileri” vardır. Grubun öncüsü Nazım Hikmet’tir. Nazım Hikmet, dize kırılışlarına, basamaklı dizilişe, görselliğe, serbest şiir örneklerine, ilk olarak Fütürist Rus şair Mayakovski’den etkilenerek başlamıştır. Toplumcu şiirde, bir düşünceye ve ideolojiye bağlı kalarak halkın çektiği sıkıntılara - kimi zaman çözüm göstererek – yer verilir. Şiirlerde hitabetçi bir eda vardır. Geniş kitlelere hitap etmek ve onları harekete geçirmek amacıyla yazılmıştır. Sanat toplum içindir.",
                        "Hececiler":"Hecenin beş şairi adıyla da anılan bu sanatçılar milli edebiyat akımından etkilenmiş ve şiirlerinde hece veznini kullanmışlardır. Şiirde sade ve özentisiz olmayı ve süsten uzak olmayı tercih etmişlerdir. Beş hececiler şiire birinci dünya savaşı ve milli mücadele döneminde başlamışlardır. Beş hececiler ilk şiirlerinde aruz veznini kullanmışlar daha sonra heceye geçmişlerdir. Şiirde memleket sevgisi, yurdun güzellikleri, kahramanlıklar ve yiğitlik gibi temaları işlemişlerdir. Hece vezni ile serbest müstezat yazmayı da denediler. Mısra kümelerinde dörtlük esasına bağlı kalmadılar yeni yeni biçimler aradılar. Nesir cümlesini şiire aktardılar ve düzyazıdaki söz dizimini şiirlerde de görülmesi beş hececiler de çok rastlanan bir özelliktir.",
                        "Hisarcılar":"Garip akımına karşı çıkan bir grup şair şiirlerini Çınaraltı Dergisi'nde yayımladılar. Daha sonra 1950 yılında çıkmaya başlayan Hisar Dergisi etrafında toplanan şu isimler bu dergide sıkça yazmışlardır: Mehmet Çınarlı, İlhan Geçer, Mustafa Necati Karaer, Nüzhet Erman, Munis Faik Ozansoy, Turgut Özakman, Halide Nusret Zorlutuna, Bekir Sıtkı Erdoğan, Yavuz Bülent Bâkiler, Sevinç Çokum, Oyhan Hasan Bıldırki, Gültekin Samanoğlu, M. Necati Özsu, Ayla Oral, Şevket Bulut, M. Fahri Oğuz, Arif Nihat Asya, Tarık Buğra, Mehmet Kaplan, Cemil Meriç, Faik Baysal, Metin And, Hilmi Ziya Ülken, Talat Sait Halman, Rüştü Şardağ. Hisar’da 500'ü aşkın şair ve yazarın eserleri yayımlanmıştır. Bu kadar kalabalık bir kadronun, belli ilkeler etrafında kenetlenmiş bir topluluk meydana getirmesi gerçekten zordur.",
                        "Maviciler":"1952’de Ankara’da yayımlanan Mavi adlı derginin etrafında toplanan sanatçıların oluşturduğu bir topluluktur. Önce Anadolu’yu tüm yönleriyle edebiyatta yansıtacakları iddiasıyla ortaya çıkmışlar, “ulusal sanattan” yana olmuşlardır; ancak Attila İlhan’ın bu dergide yayımladığı yazılardan sonra bu anlayıştan sapmışlardır. Dergi, Attila İlhan’ın toplumcu gerçekçilikle ilgili yazılarıyla dikkat çekmiştir. Derginin yönetiminde hiçbir zaman yer almasa da “Mavi” adı Attila İlhan ile özdeşleşmiştir. Garip anlayışına karşı duran, toplumcu gerçekçi edebiyata yakın olan bir topluluktur. Toplumcu gerçekçilerden farklı olarak bireyselliğin de yansıtılması gerektiğini savunmuşlardır. Şiirin basit olamayacağını zengin benzetmeli, içli, derin olması gerektiğini savunmuşlardır.",
                        "Milli Edebiyat Anlayışını Yansıtan Şiir":"Memleket edebiyatının ilk örnekleri II. Meşrutiyet sonrası verilmeye başlanmıştır. Memleket konuları işlenmiştir, şiirlerde ise halk şiiri şekilleri kullanılmış, hece ölçüsü tercih edilmiştir. Dil sadedir, mahalli söyleyişler vardır. Şiirler didaktik ve lirik türdedir. Şiirlerde geçmişin kahramanlıklarına övgü ve vatanın kurtuluşundan duyulan “gurur” teması işlenmiştir.",
                        "Cumhuriyet Dönemi Saf Şiir":"Memleket edebiyatında görülen didaktik tarza tepki göstererek şiiri, şiir yapan estetik unsurların ön plana çıkarılmasını savunmuşlardır. Paul Valery’nin  “şiirde dili her şeyden önemli tutan görüşü”ne bağlı kalmışlardır. Verlaine, Valery, Baudelaire, Mallarme ibi Fransız sembolist sanatçılardan etkilenmişlerdir.  Şiirde sembolizm akımının izleri görülür. Önemli olan iyi ve güzel şiir yazabilmektir. Bu nedenle şiirde sözcüklere yeni anlamlar yüklenmiştir. Saf şiirde ideoloji yoktur. Estetik haz önemlidir. Günlük dilden farklı bir dille şiirler yazmışlardır. Onlara göre “Şiir anlaşılmak için değil, duyulmak içindir.”  Gizemselcilik, bireyselcilik, ruh, ölüm, masal, mit temaları yoğun olarak işlenir. İçsel bir yaklaşımla insan anlatılır.",
                        "1960 Sonrası Toplumcu Şiir":"1960 kuşağı şairleri, 1961 anayasasının sağladığı özgürlükle birlikte, Nazım Hikmet’in kitaplarının yayımlanmasının serbestleştiği, siyasal ve güncel dergilerin yoğun olarak okunduğu ve gündemi belirlediği bir ortamın etkisindedirler. “Yeni Gerçek”, “And”, “Halkın Dostları”, “Militan” gibi dergiler etrafında toplanan şairler, şiir anlayışlarını ve ideolojilerini bu dergilerde açıklamaya çalışmışlardır. Marksist felsefeyi benimseyen toplumcu gerçekçi şairler, daha çok sosyal ve güncel politikayı konu edinmişler, halkın ve işçi sınıfının sorunlarını politik bir bakışla ortaya koymaya çalışan şiirler yazmışlardır. Önemli temsilcileri Ataol Behramoğlu, İsmet Özel, Süreyya Berfe, Özkan Mert, Refik Durbaş ve Nihat Behram’dır.",
                        "1980 Sonrası Şiir":"	1980 sonrası şairleri, şiirde geleneksel birikimin önemini vurgulamışlar ve Halk, Divan, saf şiir, II. Yeni gibi ayrımlara girmeden en eski örneklerden en yenilere kadar Türk şiiri şairlerinin hepsine önem vermişlerdir. Hepsi “şiire saygı” düşüncesinden yana olmuşlardır. 1980 sonrası şiiri için ortak bir şiir anlayışından çok grupların ve kişilerin ayrı ayrı şiir anlayışından söz edilebilir. Yazko Edebiyat, Üç Çiçek, Şiiratı, Sombahar gibi dergiler bu dönemde çıkarılmıştır. Özellikle büyük metropollerde yaşayan kişilerin şehre ve insana yabancılaşması, gelenek ve teknoloji arasında sıkışıp kalmaları, geçmişte var olan ama kendilerini ifade edemeyen alt kültür gruplarının bir kimlikle ortaya çıkmaları en belirgin temaları oluşturmaktadır.",
                        "Garip Şiir":" Akımın temelleri Varlık dergisinde yayınlanan şiirlerle atılmıştır. Orhan Veli Kanık,  Melih Cevdet Anday, Oktay Rıfat Horozcu  Varlık dergisinde ölçüsüz, uyaksız, günlük dile dayalı kısa şiirler yayınlamışlardır. 1941 yılında ise ortak kitapları olan “Garip” yayımlanmıştır. Bu eser Orhan Veli’nin yazdığı önsözle başlar. Orhan Veli’nin ölümünden sonra bu topluluk etkisini kaybetmiştir. “Geleneksel şiirimizle alakalı her şeye karşı olma” anlayışındadırlar. Şiirde anlam kapalılığı, mecazlı söylem dışlanmıştır. Hece ve aruza karşı çıkmışlar serbest ölçüyü benimsemişlerdir. Günlük konuşma dilinden yararlanmışlardır, espriyi, nükteyi kullanmışlardır. Günlük hayattaki her konunun şiirde yer alması gerektiğini savunmuşlardır. Şiirde ideolojiye yer vermemişlerdir.",
                        "Metafizik Anlayışını Öne Çıkaran Şiir":"Millî – manevi değerlere dayalı bir şiir anlayışı görülür. Şiirin kaynakları Anadolu coğrafyası, insanları, İslam duyarlılığı gibi konulardır. Mistik bir duyarlıkla öte dünya – bu dünya sorgulamaları yapılmıştır. Bu anlayışa sahip şairlerin birçoğu gelenekten beslenmekle birlikte geleneksel olanla moderni birleştirme çabasındadırlar. Necip Fazıl Kısakürek, Mehmet Akif Ersoy, Yahya Kemal Beyatlı gibi sanatçılardan etkilenmeler görülür. Tasavvuf inanışı, bu şairlerin beslendiği en önemli kaynaklardan biridir. İslam estetiğinin birleştirdiği bir sanat anlayışı birçok şairde görülür. İslam beldelerinin sahipsizliği, bölünüp parçalanmışlığı bu anlayışa sahip şairlerin birçoğunun ortak derdi olmuştur.",
                        "İkinci Yeni":"Garip akımına bir tepki olarak ortaya çıkmıştır. Bu topluluğun adını ilk kez Muzaffer Erdost kullanmıştır. Topluluk şairlerin bir araya gelerek, bildiri yayınlayarak oluşturdukları bir topluluk değildir. Bireysel olarak çeşitli dergilerde yazdıkları şiirler sonucunda ortak bir sanat anlayışı oluşturan kişilerce oluşturulmuş bir anlayıştır. Dadaizm, egzistansiyalizm ve özellikle sürrealizmden etkilenmişlerdir. Somut şiir yerine soyut şiire yönelmişlerdir. Kapalı ve anlaşılmaz şiirler yazmışlardır. Garipçilere karşı olduklarından şiirde mecazları kullanmışlardır. Halka değil, aydınlara yöneliktir. Şiirlerde Yunan mitolojisinden alınan sembolik tiplere de yer vermişlerdir. “Folklorik şiire düşman” sloganını ortaya atmışlardır. Şiirde ideolojiyi kullanmamışlardır."}

        dize = predict_form.dize.data
        dize_for_pred = [dize]
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
        dize_for_pred = [dize]
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
            "Edip Cansever":["İkinci Yeni", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio amet eveniet obcaecati pariatur esse qui nulla unde debitis veniam dolorem at sapiente provident earum ea architecto, maxime aut, veritatis cupiditate. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro architecto aliquam culpa! Quae provident non, repellendus in ad sed rerum."],
            "Turgut Uyar":["İkinci Yeni", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Cemal Süreya":["İkinci Yeni", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio amet eveniet obcaecati pariatur esse qui nulla unde debitis veniam dolorem at sapiente provident earum ea architecto, maxime aut, veritatis cupiditate. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro architecto aliquam culpa! Quae provident non, repellendus in ad sed rerum."],
            "Ece Ayhan":["İkinci Yeni", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Sezai Karakoç":["İkinci Yeni", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Oktay Rıfat":["Garip Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Melih Cevdet Anday":["Garip Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Orhan Veli Kanık":["Garip Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Halit Fahri Ozansoy":["Hececiler", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."], 
            "Faruk Nafiz Çamlıbel":["Hececiler", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Mehmet Akif Ersoy":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Yahya Kemal":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Mehmet Emin Yurdakul":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ziya Gökalp":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ahmet Haşim":["Fecri Ati", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Süleyman Nazif":["Servetifünun", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Cenap Şahabettin":["Servetifünun", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Tevfik Fikret":["Servetifünun", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Recaizade Mahmud Ekrem":["Tanzimat", "19. yüzyıl", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ziya Paşa":["Tanzimat", "19. yüzyıl", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Abdülhak Hamit Tarhan":["Tanzimat", "19. yüzyıl", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Namık Kemal":["Tanzimat", "19. yüzyıl", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "İbrahim Şinasi":["Tanzimat", "19. yüzyıl", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Murathan Mungan":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Enis Batur":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Haydar Ergülen":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ahmet Arif":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "İsmet Özel":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ataol Behramoğlu":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Yavuz Bülent Bakiler":["Hisarcılar", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Mehmet Çınarlı":["Hisarcılar", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Erdem Beyazıt":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Cahit Zarifoğlu":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Arif Nihat Asya":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Kemalettin Kamu":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Orhan Şaik Gökyay":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ahmet Kutsi Tecer":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Attila İlhan":["Maviciler", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ceyhun Atuf Kansu":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Nazım Hikmet":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ziya Osman Saba":["Yedi Meşaleciler", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Özdemir Asaf":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 2. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Cahit Sıtkı Tarancı":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Ahmet Hamdi Tanpınar":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."],
            "Necip Fazıl Kısakürek":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "Lorem ipsum dolor sit amet consectetur adipisicing elit."]
        }
        
        dize = predict_form.dize.data
        dize_for_pred = [dize]
        output = poet_model.predict(dize_for_pred)[0]
        poet_age = poet_info[output][0]
        poet_century = poet_info[output][1]
        poet_bio = poet_info[output][2]
        predictor = "şair"
        cursor = mysql.connection.cursor()
        sorgu = "Insert into tahminler(input, output, predictor) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (dize, output, predictor))
        mysql.connection.commit()

        cursor.close()

        return render_template("siirde-sair-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, pred_headline = "Şaire Ait Bilgiler", form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", poet_age="Şairin Eser Ürettiği Dönem: " + poet_age, poet_century="Şairin Eser Ürettiği Yüzyıl: " + poet_century, poet_bio="Şairin Kısa Biyografisi: " + poet_bio) 
    
    else:
        return render_template("siirde-sair-tahmini.html", form=predict_form)

@app.route("/siirde-kafiye-orgusu-tespiti", methods=["GET", "POST"])
def siirde_kafiye_orgusu_tespiti():

    def tunc_check(dizes):
        i = 1
        x = 0
        while x < len(dizes) - 1:
            a = i
            while (dizes[x][-a] in dizes[x+1][-a]):
                a += 1
                    
            a = (a - 1) * -1
            if ((dizes[x][a:] in dizes[x+1].split()[-1]) or (dizes[x+1][a:] in dizes[x].split()[-1])) and ((len(dizes[x].split()[-1]) < len(dizes[x+1].split()[-1])) or (len(dizes[x+1].split()[-1]) < len(dizes[x].split()[-1]))) and ((len(dizes[x].split()[-1]) >= 3) and (len(dizes[x+1].split()[-1]) >= 3)):
                return True
                    
            x += 1
            
    def cinas_check(dizes):
        i = 1
        x = 0
        while (i <= min(len(dizes[x]), len(dizes[x+2]))):
                a = 1
                while dizes[x].replace(" ", "")[-a:] == dizes[x+2].replace(" ", "")[-a:]:
                    a+=1  
                    
                a = (a-1) * -1
                conditions = [(dizes[x][a-2] == " " and dizes[x+2][a-2] == " "), (dizes[x][a-1] == " " and dizes[x+2][a-2] == " "), (dizes[x][a-2] == " " and dizes[x+2][a-1] == " ")]
                if (dizes[x].replace(" ", "")[a:] == dizes[x+2].replace(" ", "")[a:]):
                    for condition in conditions:
                        if condition == True:
                            return True
                        
                x += 1
                i = a
                if x+2 > len(dizes) - 1:
                    break

    def capraz_check(dizes):
        i = 1
        j = 1
        x = 0

        while (i <= min(map(len, dizes))):
            while dizes[x][-i:] == dizes[x+2][-i:]:
                i += 1
                    
            i = (i-1) * -1
            
            while dizes[x+1][-j] == dizes[x+3][-j]:
                j += 1
            
            j = (j-1) * -1
                
            dize_sonu1 = dizes[x][i:].replace(" ", "")
            dize_sonu2 = dizes[x+1][j:].replace(" ", "")
            dize_sonu3 = dizes[x+2][i:].replace(" ", "")
            dize_sonu4 = dizes[x+3][j:].replace(" ", "")
                
            if ((dize_sonu1 != dize_sonu2) & (dize_sonu3 != dize_sonu4)) & ((dize_sonu1 == dize_sonu3) & (dize_sonu2 == dize_sonu4)):
                return True
                break
                
            break

    def duz1_check(dizes):
        i = 1
        j = 1
        x = 0

        while (i <= min(map(len, dizes))):
            while (dizes[x][-i] == dizes[x+1][-i]):
                i += 1
                
            i = (i-1) * -1
            
            while (dizes[x+2][-j] == dizes[x+3][-j]):
                j += 1
                
            j = (j-1) * -1
            
            dize_sonu1 = dizes[x][i:].replace(" ", "")
            dize_sonu2 = dizes[x+1][i:].replace(" ", "")
            dize_sonu3 = dizes[x+2][j:].replace(" ", "")
            dize_sonu4 = dizes[x+3][j:].replace(" ", "")
            
            if ((dize_sonu1 != dize_sonu3) & (dize_sonu2 != dize_sonu4) & ((dize_sonu1 == dize_sonu2) & (dize_sonu3 == dize_sonu4))):
                return True
            break

    def duz2_check(dizes):
        i = 1
        x = 0        

        while (i <= min(map(len, dizes))):
            while dizes[x][-i] == dizes[x+1][-i] == dizes[x+2][-i]:
                i += 1
                
            i = (i-1) * -1
            
            dize_sonu1 = dizes[x][i:].replace(" ", "")
            dize_sonu2 = dizes[x+1][i:].replace(" ", "")
            dize_sonu3 = dizes[x+2][i:].replace(" ", "")
            
            if (dize_sonu1 == dize_sonu2 == dize_sonu3):
                return True
            break

    def sarma_check(dizes):
        i = 1
        j = 1
        x = 0        

        while (i <= min(map(len, dizes))):
            while (dizes[x][-i] == dizes[x+3][-i]):
                i += 1
                
            i = (i-1) * -1
            
            while (dizes[x+1][-j] == dizes[x+2][-j]):
                j += 1
                
            j = (j-1) * -1
            
            dize_sonu1 = dizes[x][i:].replace(" ", "")
            dize_sonu2 = dizes[x+1][j:].replace(" ", "")
            dize_sonu3 = dizes[x+2][j:].replace(" ", "")
            dize_sonu4 = dizes[x+3][i:].replace(" ", "")
            
            if ((dize_sonu1 == dize_sonu4) & (dize_sonu2 == dize_sonu3)) & ((dize_sonu1 != dize_sonu2) & (dize_sonu4 != dize_sonu3)):
                return True

            break

    rhyme_form = RhymeForm(request.form)

    orgu_info = {
        "Tunç Uyak":"Birbiri ile uyaklı sözcüklerden biri, diğerinin için­de aynen yer alırsa tunç kafiye oluşur. Yine unutulmamalıdır ki tunç kafiye (tunç uyak) bir zengin uyak türüdür. Yani ses benzerlikleri en az üç harften meydana gelmeli.",
        "Cinaslı Uyak":"Bu kafiye türü zengin uyak benzeri bir uyak çeşitidir. Dize sonlarında an­lamları farklı, sesleri aynı (sesteş sözcükler ya da eşsesli sözcükler) sözcükler, cinaslı uyak (cinaslı kafiye) oluşturur. Aynı zamanda söz sanatlarında cinas sanatı diye bir edebi sanat vardır.",
        "Çapraz Uyak":"Bir dörtlükte birinci ve üçüncü dize ile ikinci ve dördüncü dizenin uyaklı olmasına çapraz uyak (çapraz kafiye) denir. Başka bir ifadeyle tek numaralı dizelerin kendi aralarında; çift numaralı dizelerin de kendi aralarında uyaklı olmalarına denir. Çapraz uyak türü sadece dörtlüklerde görülür. Uyak düzeni 'abab' şeklinde gösterilir.",
        "Düz Uyak":"Bu uyak türüne  mesnevi kafiyesi de denir. Dizelerin ikişerli olarak, art arda kendi aralarında uyaklanışına düz uyak (düz kafiye) adı verilir.",
        "Sarmal Uyak":"Şiirlerdeki bir dörtlükte birinci dize ile dördüncü dizenin, ikinci dize ile üçüncü dizenin uyaklı olmasına sarma uyak (sarmal kafiye) adı verilir.",
        "Kafiye örgüsü tespit edilemedi.":"Kafiye örgüsü tespit edilemedi."
    }

    if request.method == "POST" and rhyme_form.validate():
        dize1 = rhyme_form.dize1.data.lower()
        dize2 = rhyme_form.dize2.data.lower()
        dize3 = rhyme_form.dize3.data.lower()
        dize4 = rhyme_form.dize4.data.lower()

        dizes = [dize1, dize2, dize3, dize4]
        punctuations = '''!()-[]{;:'}"\,<>./?@#$%^&*_~'''
        for dize in dizes:
            for char in dize:
                if char in punctuations:
                    index_of_dize = dizes.index(dize)
                    dize = dize.replace(char, "")
                    dizes[index_of_dize] = dize
        orgu_turu = None

        isTunc = tunc_check(dizes)
        isCinas = cinas_check(dizes)
        isCapraz = capraz_check(dizes)
        isDuz = duz1_check(dizes) or duz2_check(dizes)
        isSarma = sarma_check(dizes)

        orgu_turu = []

        if isDuz:
            orgu_turu.append("Düz Uyak")

        elif isSarma:
            orgu_turu.append("Sarmal Uyak")

        elif isCapraz:
            orgu_turu.append("Çapraz Uyak")

        elif isTunc:
            orgu_turu.append("Tunç Uyak")
        
        elif isCinas:
            orgu_turu.append("Cinaslı Uyak")

        if orgu_turu == []:
            orgu_turu = ["Kafiye örgüsü tespit edilemedi."]

        orgu_info_list = []
        for i in orgu_turu:
            if i != "Kafiye örgüsü tespit edilemedi.":
                orgu_info_list.append(i + " bilgi köşesi: " + orgu_info[i])

            else:
                orgu_info_list.append("Kafiye örgüsü tespit edilemedi.")

        orgu_info = " ".join(orgu_info_list)

        orgu_turu = "Edebi Zeka'nın Kafiye Örgüsü Tespiti: " + " ".join(orgu_turu)

        cursor = mysql.connection.cursor()
        sorgu = "Insert into kafiye_orgusu_tespiti(dize1, dize2, dize3, dize4, tespit) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sorgu, (dize1, dize2, dize3, dize4, orgu_turu))
        mysql.connection.commit()

        cursor.close()

        return render_template("siirde-kafiye-orgusu-tespiti.html", form=rhyme_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", tespit=orgu_turu, orgu_info=orgu_info)

    else:
        return render_template("siirde-kafiye-orgusu-tespiti.html", form=rhyme_form)

@app.route("/planlanan-ozellikler")
def planlanan_ozellikler():
    return render_template("planlanan-ozellikler.html")

@app.route("/veri-seti")
def veri_seti():
    return render_template("veri-seti.html")

@app.route("/algoritma-secimi")
def algoritma_secimi():
    return render_template("algoritma-secimi.html")

@app.route("/detayli-accuracy-oranlari")
def detayli_accuracy_oranlari():
    return render_template("detayli-accuracy-oranlari.html")

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