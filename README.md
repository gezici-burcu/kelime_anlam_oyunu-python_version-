# 🧠 Kelime Anlam Oyunu (Python Versiyonu)

Bu proje, kullanıcıların kelime anlamlarını tahmin ederek öğrenmesini sağlayan bir **Python tabanlı konsol + Kivy** uygulamasıdır.

## 🎯 Amaç

Rastgele gösterilen bir kelimenin anlamını tahmin ederek doğru cevaplar toplamak. Doğru/yanlış cevaplarda sesli bildirim verir. Skorlar `scores.txt` dosyasına kaydedilir.

---

## 🛠️ Kullanılan Teknolojiler

- 🐍 Python 3
- 🎛️ Kivy (görsel arayüz için)
- 🔊 Ses dosyası oynatımı (WAV formatında)
- 📄 Dosya işlemleri (kelime listesi, skor kaydı)

---

## 📂 Dosya Yapısı

```plaintext
kelime_anlam_oyunu-python_version/
├── main.py             # Ana uygulama dosyası
├── kelime.kv           # Kivy arayüz tanımı
├── scores.txt          # Skorlar burada tutulur
├── dogru.wav           # Doğru cevap sesi
├── yanlis.wav          # Yanlış cevap sesi
