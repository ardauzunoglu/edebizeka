from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.core import IntegerField
import email_validator
import joblib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hupddegoewnnjl:1c3347df1576691bbf0f62229def1424a255337b6ee7236661a4e495a5401013@ec2-34-247-118-233.eu-west-1.compute.amazonaws.com:5432/dcvppo5ei1tbsq"
db = SQLAlchemy(app)

class PredictionData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dize = db.Column(db.String(100))
    output = db.Column(db.String(100))
    predictor = db.Column(db.String(20))

class FeedbackData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(150))
    rating = db.Column(db.Integer)
    feature = db.Column(db.String(50))
    extra = db.Column(db.String(500))

class FailureFeedbackData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dize = db.Column(db.String(150))
    expected_output = db.Column(db.String(50))
    real_output = db.Column(db.String(50))

class RhymeData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dize1 = db.Column(db.String(150))
    dize2 = db.Column(db.String(150))
    dize3 = db.Column(db.String(150))
    dize4 = db.Column(db.String(150))
    orgu_turu = db.Column(db.String(25))

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
    age_model = joblib.load(open("templates/models/ez-donem.pkl", "rb"))
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
                        "1980 Sonrası Şiir":"1980 sonrası şairleri, şiirde geleneksel birikimin önemini vurgulamışlar ve Halk, Divan, saf şiir, II. Yeni gibi ayrımlara girmeden en eski örneklerden en yenilere kadar Türk şiiri şairlerinin hepsine önem vermişlerdir. Hepsi “şiire saygı” düşüncesinden yana olmuşlardır. 1980 sonrası şiiri için ortak bir şiir anlayışından çok grupların ve kişilerin ayrı ayrı şiir anlayışından söz edilebilir. Yazko Edebiyat, Üç Çiçek, Şiiratı, Sombahar gibi dergiler bu dönemde çıkarılmıştır. Özellikle büyük metropollerde yaşayan kişilerin şehre ve insana yabancılaşması, gelenek ve teknoloji arasında sıkışıp kalmaları, geçmişte var olan ama kendilerini ifade edemeyen alt kültür gruplarının bir kimlikle ortaya çıkmaları en belirgin temaları oluşturmaktadır.",
                        "Garip Şiir":"Akımın temelleri Varlık dergisinde yayınlanan şiirlerle atılmıştır. Orhan Veli Kanık,  Melih Cevdet Anday, Oktay Rıfat Horozcu  Varlık dergisinde ölçüsüz, uyaksız, günlük dile dayalı kısa şiirler yayınlamışlardır. 1941 yılında ise ortak kitapları olan “Garip” yayımlanmıştır. Bu eser Orhan Veli’nin yazdığı önsözle başlar. Orhan Veli’nin ölümünden sonra bu topluluk etkisini kaybetmiştir. “Geleneksel şiirimizle alakalı her şeye karşı olma” anlayışındadırlar. Şiirde anlam kapalılığı, mecazlı söylem dışlanmıştır. Hece ve aruza karşı çıkmışlar serbest ölçüyü benimsemişlerdir. Günlük konuşma dilinden yararlanmışlardır, espriyi, nükteyi kullanmışlardır. Günlük hayattaki her konunun şiirde yer alması gerektiğini savunmuşlardır. Şiirde ideolojiye yer vermemişlerdir.",
                        "Metafizik Anlayışını Öne Çıkaran Şiir":"Millî – manevi değerlere dayalı bir şiir anlayışı görülür. Şiirin kaynakları Anadolu coğrafyası, insanları, İslam duyarlılığı gibi konulardır. Mistik bir duyarlıkla öte dünya – bu dünya sorgulamaları yapılmıştır. Bu anlayışa sahip şairlerin birçoğu gelenekten beslenmekle birlikte geleneksel olanla moderni birleştirme çabasındadırlar. Necip Fazıl Kısakürek, Mehmet Akif Ersoy, Yahya Kemal Beyatlı gibi sanatçılardan etkilenmeler görülür. Tasavvuf inanışı, bu şairlerin beslendiği en önemli kaynaklardan biridir. İslam estetiğinin birleştirdiği bir sanat anlayışı birçok şairde görülür. İslam beldelerinin sahipsizliği, bölünüp parçalanmışlığı bu anlayışa sahip şairlerin birçoğunun ortak derdi olmuştur.",
                        "İkinci Yeni":"Garip akımına bir tepki olarak ortaya çıkmıştır. Bu topluluğun adını ilk kez Muzaffer Erdost kullanmıştır. Topluluk şairlerin bir araya gelerek, bildiri yayınlayarak oluşturdukları bir topluluk değildir. Bireysel olarak çeşitli dergilerde yazdıkları şiirler sonucunda ortak bir sanat anlayışı oluşturan kişilerce oluşturulmuş bir anlayıştır. Dadaizm, egzistansiyalizm ve özellikle sürrealizmden etkilenmişlerdir. Somut şiir yerine soyut şiire yönelmişlerdir. Kapalı ve anlaşılmaz şiirler yazmışlardır. Garipçilere karşı olduklarından şiirde mecazları kullanmışlardır. Halka değil, aydınlara yöneliktir. Şiirlerde Yunan mitolojisinden alınan sembolik tiplere de yer vermişlerdir. “Folklorik şiire düşman” sloganını ortaya atmışlardır. Şiirde ideolojiyi kullanmamışlardır."}

        dize = predict_form.dize.data
        dize_for_pred = [dize]
        output = age_model.predict(dize_for_pred)[0]
        kazanim = donem_kazanim[output]
        predictor = "dönem"
        if output == "Garip Şiir":
            output = "Garip Şiiri"

        new_insert = PredictionData(dize=dize, output=output, predictor=predictor)
        db.session.add(new_insert)
        db.session.commit()

        return render_template("siirde-donem-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, pred_headline=output + " Döneminin Özellikleri", form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", kazanim=kazanim)

    else:
        return render_template("siirde-donem-tahmini.html", form=predict_form)

@app.route("/siirde-yuzyil-tahmini", methods=["GET", "POST"])
def siirde_yuzyil_tahmini():
    predict_form = PredictForm(request.form)
    century_model = joblib.load(open("templates/models/ez-yuzyil.pkl", "rb"))
    if request.method == "POST" and predict_form.validate(): 

        donem_cikarimi = {"19. yüzyıl":["Tanzimat"],
                        "20. yüzyılın 1. yarısı":["Cumhuriyet Dönemi Saf Şiir", "1923-1960 Arası Toplumcu Serbest Şiir", "Milli Edebiyat Anlayışını Yansıtan Şiir", "Servetifünun", "Fecri Ati", "Milli Edebiyat", "Hececiler", "Garip Şiiri"],
                        "20. yüzyılın 2. yarısı":["1923-1960 Arası Toplumcu Serbest Şiir", "Maviciler", "İkinci Yeni", "Metafizik Anlayışını Öne Çıkaran Şiir", "Hisarcılar", "1960 Sonrası Toplumcu Şiir", "1980 Sonrası Şiir", "Garip Şiiri"]}

        dize = predict_form.dize.data
        dize_for_pred = [dize]
        output = century_model.predict(dize_for_pred)[0]
        cikarim = donem_cikarimi[output]
        if cikarim == ["Tanzimat"]:
            cikarim = "Tanzimat"
        else:
            cikarim = ", ".join(cikarim).strip(",")
        predictor = "yüzyıl"
        new_insert = PredictionData(dize=dize, output=output, predictor=predictor)
        db.session.add(new_insert)
        db.session.commit()

        return render_template("siirde-yuzyil-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", cikarim=output + " ile kesişen edebi dönemler: " + cikarim) 
    
    else:
        return render_template("siirde-yuzyil-tahmini.html", form=predict_form)

@app.route("/siirde-sair-tahmini", methods=["GET", "POST"])
def siirde_sair_tahmini():
    predict_form = PredictForm(request.form)
    poet_model = joblib.load(open("templates/models/ez-sair.pkl", "rb"))
    if request.method == "POST" and predict_form.validate(): 

        poet_info = {
            "Edip Cansever":["İkinci Yeni", "20. yüzyılın 2. yarısı", "(D. 8 Ağustos 1928, İstanbul - ö. 28 Mayıs 1986, İstanbul), Bu topluluk içinde en uzun süre şiir yazan kişidir. Çok değişik şiirler kaleme alıp ortak bir başarı yakalayamadığı için “çok arayıp az bulan şair” olarak nitelendirilmiştir.", "İkindi Üstü, Dirlik Düzenlik, Yerçekimli Karanfil, Umutsuzluk Parkı, Petrol, Nerde Antigone, Çağırılmayan Yakup, Tragedyalar, Kirli Ağustos, Ben Ruhi Bey Nasılım, Sevda ile Sevgi, Şairin Seyir Defteri, Yeniden, Bezik Oynayan Kadınlar, İlkyaz Şikayetçileri, Oteller Kenti, Gül Dönüyor Avucumda"],
            "Turgut Uyar":["İkinci Yeni", "20. yüzyılın 2. yarısı", "(D. 4 Ağustos 1927, Ankara - Ö. 22 Ağustos 1985, İstanbul), Aşk, ayrılık, ölüm temalarını işlediği bu dönem şiirlerinde Garip akımının izleri görülür. Daha sonra yoğun imgelerin ve simgeci bir söyleyişin etkili olduğu şiirleriyle İkinci Yeni'nin başlıca şairlerinden biri olmuştur.", "Arz-ı Hal, Türkiyem, “Dünyanın En Güzel Arabistanı”, Tütünler Islak, Her Pazartesi, Toplu Şiirler, Divan, Kayayı Delen İncir, Dün Yok Mu, Büyük Saat, Evrenin Yapısı"],
            "Cemal Süreya":["İkinci Yeni", "20. yüzyılın 2. yarısı", "(1931, Erzincan - 9 Ocak 1990, İstanbul), Asıl adı Cemalettin Seber’dir. Bu anlayışın en tanınmış sanatçılarından ayrıca kurucularından kabul edilir.", "Üvercinka, Göçebe, Beni Öp Sonra Doğur Beni, Sevda Sözleri, Sıcak Nal, Güz Bitiği"],
            "Ece Ayhan":["İkinci Yeni", "20. yüzyılın 2. yarısı", "(10 Eylül 1931, Datça - 12 Temmuz 2002, İzmir), İkinci Yeni olarak benimsediği bu anlayışa “Sivil Şiir” adını koymuştur. Kendine özgü bir dili, biçim ve anlam kaygısından uzak bir üslubu vardır.", "Kınar Hanımın Denizleri, Bakışsız Bir Kedi Kara, Ortadokslular, Yort Savul, Zambaklı Padişah, “Devlet ve Tabiat ya da Orta İkiden Ayrılan Çocuklar İçin Şiirler”, Sivil Şiirler, Bütün Yort Savular"],
            "Sezai Karakoç":["İkinci Yeni", "20. yüzyılın 2. yarısı", "(D. 22 Ocak 1933, Ergani, Diyarbakır), Din ve inanç yoluyla fizikötesi kaygıları yenebilmiş, mistik bir şairdir.", "Mona Roza, Körfez, Hızırla Kırk Saat, Taha’nın Kitabı, Kıyamet Aşısı, Gül Muştusu, Zamana Adanmış Sözler, Şahdamar"],
            "Oktay Rıfat":["Garip Şiiri", "20. yüzyılın 2. yarısı", "(10 Haziran 1914 - 18 Nisan 1988) Oktay Rıfat kimdir, Türk şair, roman ve oyun yazarı, avukat. Cumhuriyet sonrası Türk edebiyat tarihinin gelişmesinde ve şiirinin yenilenmesinde büyük etkisi olan “Birinci Yeni Akımı“nın (Garip) kuramcılarından, “İkinci Yeni Akımı“nın ise öncülerinden biridir.", "Yaşayıp Ölmek, Aşk ve Avarelik Üstüne Şiirler (1945) Güzelleme (1945), Aşağı Yukarı (1952), Karga ile Tilki (1954), Perçemli Sokak (1956), Aşık Merdiveni (1958), Elleri Var Özgürlüğün (1966), Şiirler (1969), Yeni Şiirler (1973)"],
            "Melih Cevdet Anday":["Garip Şiiri", "20. yüzyılın 2. yarısı", "(13 Mart 1915, Çanakkale – 28 Kasım 2002, İstanbul), Yalın bir dil kullanmıştır, şiirlerinde güzel günlere özlem vardır.", "Garip, Rahatı Kaçan Ağaç, Telgrafhane, Kolları Bağlı Odysseus, Yan Yana, Göçebe Denizin Üstünde, Teknenin Ölümü, Ölümsüzlük Ardında Gılgamış, Tanıdık dünya, Yağmurun Altında"],
            "Orhan Veli Kanık":["Garip Şiiri", "20. yüzyılın 1. yarısı", "(13 Nisan 1914 – 14 Kasım 1950), Garip akımının öncüsüdür. Eski şiir geleneğini yıkmıştır. Sokaktaki sade vatandaşı, onların dilini kullanarak anlatmıştır.", "Garip, Vazgeçemediğim, Destan Gibi, Yenisi, Karşı Nasrettin Hoca Hikayeleri"],
            "Halit Fahri Ozansoy":["Hececiler", "20. yüzyılın 1. yarısı", "(12 Temmuz 1891, İstanbul - 23 Şubat 1971, İstanbul), Türk şair, gazeteci, oyun yazarı, öğretmendir. Hecenin Beş Şairinden biridir. 40 yıl edebiyat öğretmenliği yapan Ozansoy, başta şiir olmak üzere tiyatro ve roman türlerinde pek çok eser vermiş bir edebiyat ve kültür adamıdır.", "Cenk Duyguları, Hep Onun İçin, Gülistan ve Harabeler, Bulutlara Yakın, Zakkum"], 
            "Faruk Nafiz Çamlıbel":["Hececiler", "20. yüzyılın 1. yarısı", "(18 Mayıs 1898, İstanbul – 8 Kasım 1973, İstanbul), Türk şair, siyasetçi, öğretmen. Hecenin Beş Şairinden biridir. En ünlü eseri, Han Duvarları adlı şiiridir. Behçet Kemal Çağlar ile birlikte Onuncu Yıl Marşı’nın sözlerini yazmıştır. “Sanat” şiiri Milli Edebiyatın manifestosudur.", "Han Duvarları, Şarkın Sultanları, Dinle Neyden, Gönülden Gönüle, Çoban Çeşmesi, Bir Ömür Böyle Geçti, Elimle Seçtiklerim"],
            "Mehmet Akif Ersoy":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "(1873 – 1936), 20. yüzyılda Türk-İslam milliyetçiliğinin en büyük sanatçısıdır.", "Safahat, Süleymaniye Kürsüsünde, Hakkın Sesleri, Fatih Kürsüsünde, Hatıralar, Asım, Gölgeler” adlı yedi bölümden oluşmaktadır."],
            "Yahya Kemal":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "(1884 – 1958), Batı şiiri ile eski Türk şiirini birleştiren ilk sanatçımızdır. Şiirde iç ahenge son derece önem vermiştir ve “şiirin musikiden başka bir musiki” olduğunu söylemiştir.", "Kendi Gök Kubbemiz, Eski Şiirin Rüzgarıyla, Rubailer, Hayam Rubailerini Türkçe Söyleyiş, Bitmemiş Şiirler"],
            "Mehmet Emin Yurdakul":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "( 1869- 1944 ), Türkçülük düşüncesini şiir alanında ilk kez sanat haline getiren kişidir. “Cenge Giderken” adlı şiiri Türklük heyecanını dile getiren ilk meşhur şiir olmuştur.", "Türkçe Şiirler, Türk Sazı, Ey Türk Uyan, Tan Sesleri, Ordunun Destanı, Dicle Önünde, Turana Doğru, Zafer Yolunda, İsyan ve Dua, Aydın Kızları, Mustafa Kemal, Ankara"],
            "Ziya Gökalp":["Milli Edebiyat", "20. yüzyılın 1. yarısı", "(1876 - 1824), Türk milliyetçiliğinin esaslarını belirleyen ve Türkçülüğü  sistemleştiren kişidir.", "Kızıl Elma, Yeni Hayat, Altın Işık"],
            "Ahmet Haşim":["Fecri Ati", "20. yüzyılın 1. yarısı", "(1887, Bağdat - 4 Haziran 1933, Kadıköy, İstanbul), sembolizmin öncülerinden Türk şairidir.", "Göl Saatleri, Piyale"],
            "Süleyman Nazif":["Servetifünun", "20. yüzyılın 1. yarısı", "Şair ve yazar, devlet adamı (D. 29 Ocak 1870, Diyarbakır - Ö. 4 Ocak 1927, İstanbul).", "Cenk Türküsü (1917), Daüs-Sıla, Kübalılar, Türk İlahisi (1926)"],
            "Cenap Şahabettin":["Servetifünun", "20. yüzyılın 1. yarısı", "(1870-1934) Asıl mesleği doktorluk olan sanatçı, Servet-i Fünun edebiyatında Tevfik Fikret’ten sonra gelen en önemli şairdir.", "Elhân-ı Şitâ, Senin İçin, Güzel Sözler, Bitmemiş Bir Gül, Hakikat-i Sevda, On Ölüm Şarkısı, Benim Kalbim Şair"],
            "Tevfik Fikret":["Servetifünun", "20. yüzyılın 1. yarısı", "(24 Aralık 1867 - 19 Ağustos 1915), Osmanlı şair ve öğretmen. Osmanlı İmparatorluğu'nun dağılma sürecinde yetişti. Servet-i Fünûn topluluğunun lideri olan Tevfik Fikret, Türk edebiyatının Batılılaşmasında öne çıkan isimlerden biridir.", "Rübabı Şikeste, Rübabın Cevabı, Haluk’un Defteri, Şermin."],
            "Recaizade Mahmud Ekrem":["Tanzimat", "19. yüzyıl", "Recaizade Mahmud Ekrem (d. 1 Mart 1847, İstanbul, Osmanlı İmparatorluğu - ö. 31 Ocak 1914, İstanbul, Osmanlı İmparatorluğu), Türk şair ve yazar.", "Ah Nijad!, Şevki Yok, Güzelim, Yâd Et"],
            "Ziya Paşa":["Tanzimat", "19. yüzyıl", "Ziya Paşa (d. 1829, İstanbul - ö. 17 Mayıs 1880, Adana), Türk yazar, şair ve devlet adamı.", "Âsâf'ın Mikdârını Bilmez Süleyman Olmayan, Deneme, Terci-i Bend, Renc-i Hâtır Vermesin Feryâd Ü Efganlar Saña, Gazel"],
            "Abdülhak Hamit Tarhan":["Tanzimat", "19. yüzyıl", "(2 Ocak 1852, Beşiktaş - 12 Nisan 1937, İstanbul), Türk şair, oyun yazarı, diplomat.", "Sahra (1878), Makber (1885), Ölü (1886), Hacle (1887), Bir Sefilenin Hasbihali (1886), Bâlâ’dan Bir Ses (1911), Validem (1913), İlham-ı Vatan (1918), Tayflar Geçidi (1919), Garâm (1923), Kürsî-i İstiğrak, Bunlar O'dur (1885), Divaneliklerim yahut Belde (1885), Külbe-i İştiyak,Elveda Diyemedik"],
            "Namık Kemal":["Tanzimat", "19. yüzyıl", "(d. 21 Aralık 1840, Tekirdağ - ö. 2 Aralık 1888, Sakız Adası), Türk milliyetçiliğine ilham kaynağı olmuş, Genç Osmanlı hareketi mensubu yazar, gazeteci, devlet adamı ve şairdir.", "Vatan Şarkısı, Hırraname, Vaveyla, Yoktur, Hürriyet Kasidesi, Beyitler, Murabba"],
            "İbrahim Şinasi":["Tanzimat", "19. yüzyıl", "(5 Ağustos 1826, İstanbul – 13 Eylül 1871, İstanbul), Türk gazeteci, yayımcı, şair ve oyun yazarı.", "Tercüme-i Manzume (1859), Müntehabât-ı Eş‘âr (Dîvân-ı Şinâsî) (1862), Müntehabat-ı Tasvîr-i Efkâr (1885–1886)"],
            "Murathan Mungan":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "(D. 21 Nisan 1955, İstanbul), Türk yazar, oyun yazarı ve şairdir.", "Osmanlıya dair Hikâyat, Kum Saati, Sahtiyan, Yaz Sinemaları, Eski 45'likler, Mırıldandıklarım, Yaz Geçer, Omayra, Oda, Poster ve Şeylerin Kederi, Metal, Oyunlar İntiharlar Şarkılar, Mürekkep Balığı, Başkalarının Gecesi, Doğduğum Yüzyıla Veda, Erkekler için Divan, Timsah Sokak Şiirleri, Eteğimdeki Taşlar, Dağ, Bazı Yazlar Uzaktan Geçer, İkinci Hayvan, Gelecek"],
            "Enis Batur":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "(D. 28 Haziran 1952, Eskişehir), Türk şair, deneme yazarı, yayıncıdır.", "Tuğralar, Perişey , Kanat Hareketleri, Ağlayan Kadınlar Lahdi , Darb ve Mesel - Arka Şiirler , Neyin Nesisin Sen , Saga , A Capella , Tuğralar – Perişey , Kanat Hareketleri – Neyin Nesisin Sen, Karanlık Oda Şarkıları"],
            "Haydar Ergülen":["1980 Sonrası Şiir", "20. yüzyılın 2. yarısı", "(D. 14 Ekim 1956 Eskişehir), 1983’te arkadaşlarıyla birlikte “Üç Çiçek” dergisini çıkarmıştır, ayrıca “Şiiratı” dergisine de emeği geçmiştir.", "Karşılığını Bulamamış Sorular, Sokak Prensesi, Eskiden Terzi, Kabareden Emekli Bir Kız Kardeş, 40 Şiir ve Bir, Karton Valiz, Ölüm Bir Skandal, Keder Gibi Ödünç, Üzgün Kediler Gazeli, Nar (Bütün şiirleri I), Hafız ile Semender (Bütün şiirleri II)"],
            "Ahmet Arif":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "(23 Nisan 1927, Diyarbakır - 2 Haziran 1991, Ankara),  1940-1955 yılları arasında değişik dergilerde yayınladığı şiirlerinde kullandığı kendine has lirizmi ve hayal gücüyle Türk edebiyatındaki yerini aldı. Türkçeyi en iyi kullanan şairlerdendir.", "Akşam Erken İner Mahpushaneye, Anadolu, Ay Karanlık, Bu Zindan Bu Kırgın Bu Can Pazarı, Diyarbekir Kalesinden Notlar ve Adiloş Bebenin Ninnisi, Hani Kurşun Sıksan Geçmez Geceden"],
            "İsmet Özel":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "(19 Eylül 1944, Kayseri), Ataol Behramoğlu ile birlikte “Halkın Dostları” dergisini çıkarmıştır. İkinci Yeni esintisiyle başlayan şiir serüveninde, 1960 ve1970’li yıllarda, toplumcu şiirin unutulmaz şiirlerini yazmıştır.", "Geceleyin Bir Koşu, Evet İsyan, Cinayetler Kitabı, Cellâdıma Gülümserken, Erbain (4 kitabındaki şiirleri bir arada), Bir Yusuf Masalı,  Of Not Being A Jew"],
            "Ataol Behramoğlu":["1960 Sonrası Toplumcu Şiir", "20. yüzyılın 2. yarısı", "(D. 13 Nisan 1942, Çatalca), İsmet Özel’le “Halkın Dostları”, Nihat Behram’la “Militan” dergilerini çıkarmış ve bu dergilerin yöneticiliğini yapmıştır.", "Bir Ermeni General, Bir Gün Mutlaka (Bütün şiirleri- 1), Yaşadıklarımdan Öğrendiğim Bir Şey Var (Bütün şiirleri- 2), Kızıma Mektuplar (Bütün şiirleri- 3), Yolculuk Özlem Cesaret ve Kavga Şiirleri, Kuşatmada, Mustafa Suphi Destanı, Dörtlükler, Ne Yağmur... Ne Şiirler."],
            "Yavuz Bülent Bakiler":["Hisarcılar", "20. yüzyılın 2. yarısı", "(D. 23 Nisan 1936, Sivas), Türk şair ve yazar. Gazetecilik, yöneticilik aynı zamanda avukatlık da yaptı.", "Yalnızlık, Duvak, Seninle, Harman, Bir Gün Baksam Ki Gelmişsin, Sen Sen Sen"],
            "Mehmet Çınarlı":["Hisarcılar", "20. yüzyılın 2. yarısı", "(D. 1925 - Ö. 19 Ağustos 1999), Cumhuriyet Dönemi Türk Edebiyatı Türk yazar, şair, denemeci, eleştirmen. Hisarcılar akımının kurucusudur.", "Güneş Rengi Kadehlerle, Gerçek Hayali Aştı, Bir Yeni Dünya Kurmuşum"],
            "Erdem Beyazıt":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı", "(1939, Kahramanmaraş - 5 Temmuz 2008, İstanbul), Şiirlerinde İslami bir duyarlılık bulunan şair, tasavvuftan çokça yararlanmıştır. En ünlü şiiri olan “Sebep Ey” adlı şiirinde her şeyin tek ve mutlak sebebinin Allah olduğunu dile getirir.", "Sebep Ey, Risaleler, Gelecek Zaman Risalesi"],
            "Cahit Zarifoğlu":["Metafizik Anlayışını Öne Çıkaran Şiir", "20. yüzyılın 2. yarısı", "(1 Temmuz 1940, Ankara - 7 Haziran 1987İstanbul) Şiirleri “zor şiir” olarak nitelendiren sanatçı, kapalı anlatımının gerisinde İslami bir anlayışı bulunmaktadır.", "İşaret Çocukları, Yedi Güzel Adam, Menziller, Korku ve Yaraşır"],
            "Arif Nihat Asya":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "(7 Şubat 1904, Çatalca, İstanbul - 5 Ocak 1975, Ankara), “Bayrak Şairi” olarak tanınır. Önce aruzu kullanmış daha sonra heceye geçmiş, serbest şiirler de yazmıştır. Dini, milli duyguları, kahramanlıkları şiirleştirmiştir.", "Bir Bayrak Rüzgar Bekliyor, Heykeltıraş, Yastığımın Rüyası, Kıbrıs Rubaileri, Rubaiyatt-ı Arif, Avrupa’dan Rubailer, Ses ve Toprak, Köprü, Kökler ve Dallar, Dualar ve Aminler, Aynalarda Kalan"],
            "Kemalettin Kamu":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "(D. 15 Eylül 1901, Bayburt - Ö. 6 Mart 1948, Ankara), Vatan ve gurbet şiirlerine yönelmiştir. İlk şiirlerinde aruzu da kullanmış, daha sonra hece ile sade şiirler yazmıştır.", "Gurbet, Gurbet Geceleri, Gurbette Renkler, Bingöl Çobanları, Kimsesizlik, Güz, İrşad, Hazan Yolcusunda, Söğüt"],
            "Orhan Şaik Gökyay":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "Eğitimci, şair ve yazar, çevirmen (D. 16 Temmuz 1902, İnebolu / Kastamonu - Ö. 2 Aralık 1994, İstanbul).", "Birkaç Şiir (1976)"],
            "Ahmet Kutsi Tecer":["Milli Edebiyat Anlayışını Yansıtan Şiir", "20. yüzyılın 1. yarısı", "(4 Eylül 1901, Kudüs - 23 Temmuz 1967, İstanbul), Faruk Nafiz’in açtığı yolla memleket edebiyatına yönelmiştir. Şiirleri türküler, destanlar, efsaneler, gelenek- göreneklerden etkilenmiştir. 'Orada Bir Köy Var Uzakta' adlı şiiriyle meşhur olmuştur.", "Şiirler, Tüm Şiirleri"],
            "Attila İlhan":["Maviciler", "20. yüzyılın 2. yarısı", "15 Haziran 1925 - 10 Ekim 2005), Şair, romancı, senarist, düşünce adamıdır. Garip ve İkinci Yeni anlayışına karşı çıkmıştır.", "Duvar, Sisler Bulvarı, Yağmur Kaçağı, Ben Sana Mecburum, Yasak Sevişmek, Bela Çiçeği, Tutkunun Günlüğü, Böyle Bir Sevmek, Elde Var Hüzün, Korkunun Krallığı, Ayrılık Sevdaya Dahil, Kimi Sevsem Sensin"],
            "Ceyhun Atuf Kansu":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 2. yarısı", "(D. 7 Aralık 1919, İstanbul - Ö. 17 Mart 1978, Ankara), Türk yazar, şair ve doktor.", "Bir Çocuk Bahçesinde, Bağbozumu Sofrası, Çocuklar Gemisi, Yanık Hava, Haziran Defteri, Yurdumdan Bağımsızlık Gülü, Sakarya Meydan Savaşı, Buğday, Kadın, Gül ve Gökyüzü, Tüm Şiirleri (1978, iki cilt ölümünden sonra), Dünyanın bütün çiçekleri"],
            "Nazım Hikmet":["1923-1960 Arası Toplumcu Serbest Şiir", "20. yüzyılın 1. yarısı", "(15 Ocak 1902; Selanik - 3 Haziran 1963; Moskova, SSCB), Türk şair ve yazardır. Toplumcu gerçekçi edebiyatın öncüsüdür. İlk şiirlerini ölçü ve uyaklı yazmıştır. Rusya’daki eğitimi esnasında Mayakovski’den etkilenmiştir.", "835 Satır, Jakond ile Si-Ya-U, Benerci Kendini Niçin Öldürdü, Taranta Babu’ya Mektuplar, Simavna Kadısı Oğlu Şeyh Bedrettin Destanı, Memleketimden İnsan Manzaraları, Kuvayı Milliye Destanı, Saat 21-22 Şiirleri"],
            "Ziya Osman Saba":["Yedi Meşaleciler", "20. yüzyılın 1. yarısı", "(30 Mart 1910, İstanbul - 29 Ocak 1957, İstanbul), Yedi Meşaleciler Hareketi'nin kurucularındandır. Şair olarak ün kazanan edebiyatçı, küçük hikâye türünde de eserler verdi.", "Sebil ve Güvercinler,  Geçen Zaman, Nefes Almak"],
            "Özdemir Asaf":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 2. yarısı", "(11 Haziran 1923, Ankara - 28 Ocak 1981, İstanbul), Özgün ve etkileyici bir dil kullandığı şiirlerinde 'ikinci kişi' sorununu ele aldı.  Özellikle son dönem şiirlerinde dize sayısını azaltarak duygu ve zekâ pırıltılarının kaynaştığı kısa şiirler yazmıştır.", "Dünya Kaçtı Gözüme, Sen Sen Sen, Bir Kapı Önünde, Yumuşaklıklar Değil, To Go To, Yalnızlık Paylaşılmaz"],
            "Cahit Sıtkı Tarancı":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "(4 Ekim 1910, Diyarbakır - 12 Ekim 1956, Viyana) , “Otuz Beş Yaş” şiiri ile tanınmıştır. Hece ölçüsüne son derece önem vermiş, kafiyeye bağlı kalmıştır.", "Ömrümde Sükut, Otuz Beş Yaş, Düşten Güzel, Sonrası, Bütün Şiirleri"],
            "Ahmet Hamdi Tanpınar":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "(23 Haziran 1901, İstanbul - 24 Ocak 1962, İstanbul), Hem sezgicilik akımından hem de sembolizm akımından etkilenmiştir. Eserlerin Doğu- Batı Çatışması, “rüya”, “zaman” kavramları ve “geçmişe özlem”, “mimari”, “musiki” öne çıkar.", "Bütün Şiirleri"],
            "Necip Fazıl Kısakürek":["Cumhuriyet Dönemi Saf Şiir", "20. yüzyılın 1. yarısı", "(26 Mayıs 1904, İstanbul - 25 Mayıs 1983, İstanbul), Din, tasavvuf, politika, öykü, roman, tiyatro, şiir gibi alanlarda eser vermiştir. Sanat hayatı iki dönemden oluşmaktadır. 1943’ten itibaren tasavvufa, mistik anlayışa ve ideolojiye yönelmiştir.", "Örümcek Ağı, Kaldırımlar, Ben ve Ötesi, Sonsuzluk Kervanı, Çile, Şiirlerim"]
        }
        
        dize = predict_form.dize.data
        dize_for_pred = [dize]
        output = poet_model.predict(dize_for_pred)[0]
        poet_age = poet_info[output][0]
        poet_century = poet_info[output][1]
        poet_bio = poet_info[output][2]
        poems = poet_info[output][3]
        predictor = "şair"
        new_insert = PredictionData(dize=dize, output=output, predictor=predictor)
        db.session.add(new_insert)
        db.session.commit()

        return render_template("siirde-sair-tahmini.html", pred="Edebi Zeka'nın Tahmini: " + output, pred_headline = "Şaire Ait Bilgiler", form=predict_form, not_sure="Edebi Zeka'nın hatalı tahminde bulunduğunu mu düşünüyorsun? Bize bildir!", poet_age="Şairin Eser Ürettiği Dönem: " + poet_age, poet_century="Şairin Eser Ürettiği Yüzyıl: " + poet_century, poet_bio="Şairin Kısa Biyografisi: " + poet_bio, poems="Şairin Önemli Şiirleri: " + poems) 
    
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

        new_insert = RhymeData(dize1=dize1, dize2=dize2, dize3=dize3, dize4=dize4, orgu_turu=orgu_turu)
        db.session.add(new_insert)
        db.session.commit()

        orgu_turu = "Edebi Zeka'nın Kafiye Örgüsü Tespiti: " + " ".join(orgu_turu)

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

        new_insert = FailureFeedbackData(dize=dize, expected_output=expected_output, real_output=real_output)
        db.session.add(new_insert)
        db.session.commit()

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

        new_insert = FeedbackData(name=name, surname=surname, email=email, rating=rating, feature=feature, extra=extra)
        db.session.add(new_insert)
        db.session.commit()

        return redirect(url_for("tesekkurler"))

    else:
        return render_template("geri-bildirim-formu.html", form = form)
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
