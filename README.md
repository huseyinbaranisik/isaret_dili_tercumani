# <p align="center">🚀 DYNAMIC SIGN LANGUAGE TRANSLATOR</p>
## <p align="center">🤟 Eğitilebilir ve Gerçek Zamanlı İşaret Dili Tercümanı</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/MediaPipe-00C7B7?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
</p>

---

### 📝 PROJE HAKKINDA
Bu çalışma, **Sayısal Görüntü İşleme** dersi final ödevi kapsamında geliştirilmiştir. Projenin temel odağı; görüntü segmentasyonu, bilgisayarlı görü ve derin öğrenme tekniklerini kullanarak işaret dili hareketlerini gerçek zamanlı olarak anlamlandırmaktır.

Sabit veri setlerine bağlı kalmak yerine, kullanıcının kendi işaretlerini sisteme tanıtmasına ve modelini arayüz üzerinden eğitmesine olanak tanıyan **"Dinamik Eğitim Modülü"** projenin temelini oluşturur.

### 🌟 Temel Özellikler
* **📍 Hassas Takip:** **MediaPipe** aracılığıyla el ve vücut eklem noktalarının (landmarks) anlık takibi.
* **🧠 Hareket Analizi:** Zaman serisi verilerini işlemek ve hareket dizilerini sınıflandırmak için kullanılan **LSTM** mimarisi.
* **🖥️ Kullanıcı Arayüzü:** Veri toplama, model eğitimi ve tahmin süreçlerini yöneten **PyQt5** tabanlı kontrol paneli.
* **🔊 Seslendirme:** Algılanan ifadelerin **gTTS** ve **pyttsx3** kütüphaneleri ile anlık sese dönüştürülmesi.
* **📂 Esnek Veri Seti:** Kod yazmaya gerek kalmadan, doğrudan arayüz üzerinden yeni kelimeler ekleyebilme imkanı.

---

### 🛠️ TEKNOLOJİ YIĞINI

| Bileşen | Teknoloji | Kullanım Amacı |
| :--- | :--- | :--- |
| **Görüntü İşleme** | MediaPipe | Eklem Takibi ve Öznitelik Çıkarımı |
| **Derin Öğrenme** | TensorFlow / Keras | LSTM Tabanlı Hareket Tanıma |
| **Arayüz** | PyQt5 & Qt Designer | UI/UX ve Akış Yönetimi |
| **Ses** | gTTS & pyttsx3 | Metinden Sese Dönüştürme |
| **Dil** | Python | Çekirdek Mantık ve Betikleme |

---

### 🚀 KURULUM VE KULLANIM

> [!IMPORTANT]
> **Adımları Takip Edin:**
> 1. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt`
> 2. Ana uygulamayı başlatın: `python main.py`
> 3. "Veri Topla" sekmesinden yeni işaretler kaydedin veya mevcut modelle tahmine başlayın.

---

<p align="center">
  <i>Sayısal Görüntü İşleme Akademik Final Projesi - 2026</i>
</p>
