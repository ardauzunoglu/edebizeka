![Edebi Zeka](https://github.com/ardauzunoglu/edebizeka/blob/main/web-site/edebi-zeka-logo.png?raw=true)

Edebi Zeka, **modern Türk edebiyatı** sınırları içerisinde yer alan dönemleri, eğilimleri, şairleri ve zaman dilimlerini sınıflandıran, **doğal dil işleme** prensipleri ile geliştirilmiş bir çoklu metin sınıflandırma uygulamasıdır.

[edebizeka.herokuapp.com](https://edebizeka.herokuapp.com)

## Yöntem ve Kullanılan Kütüphaneler

Edebi Zeka, *Scikit-Learn*, *nltk*, *Pandas* ve *numpy* kullanılarak geliştirilmiştir. Geliştirilen yapay zekâ modelleri *Flask* kütüphanesi ile geliştirilen internet sayfasına entegre edilerek kullanıma açılmıştır.

Edebi Zeka'nın geliştirilmesinde kullanılan veri setleri 1839 - 2000 yılları arası modern Türk şiirini kapsamaktadır. Bu bağlamda veri setlerin 16 dönem ve eğilim, 93 şair ve 3 zaman dilimi yer almaktadır. 

[Veri Setine Dair Her Şey](https://edebizeka.herokuapp.com/veri-seti-turkiye)

Edebi Zeka geliştirilirken dört farklı algoritma (Lojistik Regresyon, KNN, Naive Bayes, Linear Support Vector Machines) test edilmiş ve her bir tahmin öznesi için en yüksek doğruluk oranını sağlayan algoritma kullanılarak yapay zeka modelleri eğitilmiştir.

[Algoritma Seçimi ve Algoritmaların Sağladıkları Doğruluk Oranları](https://edebizeka.herokuapp.com/algoritma-secimi)

Dönem ve eğilim tahmini için geliştirilen model %96.8, şair tahmini için geliştirilen model %98.3, yüzyıl tahmini için geliştirilen model %99'luk doğruluk oranları elde etmiştir.

[Modellerin Doğruluk Oranları ve Dağılımları](https://edebizeka.herokuapp.com/kullandigimiz-modeller-turkiye)

## Gereksinimler

> 'pip install -r requirements.txt' komutu ile yerel cihazınıza gerekli kütüphanelerin kurulumunu gerçekleştirebilirsiniz.

## Katılım Gösterilen Yarışmalar

TÜBİTAK 2204 - A Lise Öğrencileri Araştırma Projeleri Yarışması - Türk Dili ve Edebiyatı Bursa Bölge Birinciliği 🥇

TÜBİTAK 2204 - A Lise Öğrencileri Araştırma Projeleri Yarışması - Türk Dili ve Edebiyatı Türkiye Birinciliği 🥇


## Geliştirici
Github: [@ardauzunoglu](https://github.com/ardauzunoglu)
