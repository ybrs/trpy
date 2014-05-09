
TRPY
================
Türkçe programlama dili denemesidir.

Nedir ?
================
Özellikle okumayı yeni öğrenen çocukların programlamaya girişmesi için oldukça basit bir programlama dilidir. Trpy, python programlama diline çevrim yapar. Aynı zamanda python kütüphanelerini kullanabilir, ve python içinden trpy kütüphaneleri de kullanılabilir.

Beklentimiz, çocuğun 'baba if miydi def miydi' diye sormak yerine, 'burada neden hata çıkıyor' diye sormasıdır.

Velhasılı çocuk __if__ yerine __eger, X ve A ise__ yazıp programlamaya girişirse, programlama mantığını daha hızlı oturtacak, sonrasında zaten bir şekilde __if__ tir, __elif__ tir öğrenmeye başlayacak zamanla diye umuyoruz.

En olmadı basit bir programlama dili nasıl yazılır, pythonın importerı nasıl genişletilir vs. konularında bir örnek olur.


Kurulum
================
```pip install trpy```

Kullanım
================

trpy dosyasini calistirmak icin,

```trpy f.trpy```

sadece python cevrimini gormek icin:

```trpy_cevir f.trpy```

Dilin Özellikleri
================

Değişken tanımları
-------------------
Python ile ayni

```
    a = 1
    b = 2
```

Koşullar
------------------
Trpy:
```
    eger, x > 10 ve x < 20 ise
       yazdir "10 ile 20 arasinda"
    ya da, x > 30 veya y < 10
        yazdir "x 10 dan buyuk"
    ya da,
        yazdir "x 10 dan kucuk"
```

Bu Python a su sekilde tercume edilecektir:
```
    if x > 10 and x < 20:
       print "10 ile 20 arasinda"
    elif x > 30 or y < 10:
        print "x 10 dan buyuk"
    else:
        print "x 10 dan kucuk"
```

Iterasyon/Döngüler
-------------------
Trpy:
```
a = [1,2,3]

her bir, a icin x
    yazdir x
```

Python
```
a = [1,2,3]

for x in  a:
    print x
```

Uzun Koşullar (while)
----------------------

Trpy:

```
c = 1
durum, c < 10 iken
    yazdir c
    c += 1
```

Python:

```
c = 1
while c < 10:
    print c
    c += 1
```

Fonksiyonlar
--------------------

Trpy:
```
kac_tane(i)->
    <- len(i)

toplami(i)->
    c = 0
    her bir, i icin x
        c += x
    <- c

ortalamasi(i)->
    <- toplami(i) / kac_tane(i)
```

Python:

```
def kac_tane(i):
    return len(i)

def toplami(i):
    c = 0
    for x in  i:
        c += x
    return c

def ortalamasi(i):
    return toplami(i) / kac_tane(i)
```

Kütüphane kullanımı (import)
--------------------------------------

Her iki yonlu importu destekliyoruz, pythondan trpy dosyasini direk import edebiliriz,
ornegin std.trpy dosyasi soyle olsun

```
kac_tane(i)->
    <- len(i)
```

Pythondan

```
from std import kac_tane
```

diyebiliriz, ayni seyi trpy de

```
# import
yukle, os

# from collections import OrderedDict
yukle, collections icinden OrderedDict
yukle, trpy.std icinden *
```

Ornekler
-----------
Kod ornekleri, yazim.trpy ve ornekler dizinlerinde bulunuyor.

Yapılacaklar
===================

İlk ayakta eksik kalanlar:

- range, xrange vs. için türkçe karşılık bulmak
- Exceptionlar, stack trace basarken araya girip türkçeye çevrim yapmak
- Object Oriented Programlama için türkçe karşılık bulmak
