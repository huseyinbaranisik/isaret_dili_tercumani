import sys

try:
    import importlib
    import importlib.metadata
    if not hasattr(importlib.metadata, 'packages_distributions'):
        try:
            import importlib_metadata
            importlib.metadata.packages_distributions = importlib_metadata.packages_distributions
        except ImportError:
            pass
except ImportError:
    pass

import os
import json
import urllib.request
import urllib.error

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

 

import cv2
import numpy as np
import threading
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLabel, QPushButton, QRadioButton, QInputDialog, QLineEdit
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QImage, QPixmap
try:
    from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
    QT_MULTIMEDIA_VAR = True
except ImportError:
    QT_MULTIMEDIA_VAR = False

from arayuz import Ui_main_window
import isaret_dili_araclari as ida
from veri_toplama import VeriToplamaModulu
from model_egitimi import ModelEgitici



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERI_YOLU = os.path.join(BASE_DIR, 'data', 'MP_Data')
SEKANS_UZUNLUGU = 30

class IsaretDiliUygulamasi(QDialog):
    tahmin_sinyali = pyqtSignal(str, float)
    ai_sinyali = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        
        self.ui_ozellestir()
        
        print(">> AI Modülü (Yerel Kural Tabanlı) Hazır.")
        
        self.kamera = cv2.VideoCapture(0)
        
        self.zamanlayici = QTimer(self)
        self.zamanlayici.timeout.connect(self.kare_guncelle)
        self.zamanlayici.start(30)

        self.holistik = ida.mp_holistik.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.8)

        self.veri_toplayici = VeriToplamaModulu(VERI_YOLU, SEKANS_UZUNLUGU, hazirlik_suresi=30)
        self.egitici = ModelEgitici(VERI_YOLU)
        
        self.tahmin_modu = True
        self.model = None
        self.canli_tampon = []
        self.eylemler = []
        
        self.eklentileri_goster = True
        self.ai_modu = False
        self.goz_durum_tamponu = []
        self.son_kirpma_zamani = 0
        self.kirpma_bekleme_suresi = 0
        self.egitim_yapiliyor = False
        self.api_key = None
        self.sesli_oku_aktif = False
        self.son_okunan_metin_ai = ""
        
        self.son_okunan_metin_ai = ""
        
        
        self.medya_oynatici = QMediaPlayer() if QT_MULTIMEDIA_VAR else None
        if self.medya_oynatici:
             self.medya_oynatici.mediaStatusChanged.connect(self.muzik_bitti_kontrol)
        
        self.ui.rd_btn_eklenti_gizle.toggled.connect(self.eklentileri_goster_gizle)
        self.ui.rd_btn_ai_ceviri.toggled.connect(self.ai_modu_degis)
        self.ui.btn_sil.clicked.connect(self.metni_temizle)
        self.ui.rd_btn_sesli_oku.toggled.connect(self.sesli_oku_durum_degis)
        self.ui.btn_egitime_basla.clicked.connect(self.egitimi_baslat)
        self.ui.btn_egitime_basla.clicked.connect(self.egitimi_baslat)
        self.ui.btn_egitimi_durdur.clicked.connect(self.egitimi_durdur)
        
        self.tahmin_sinyali.connect(self.sonuc_guncelle_gui)
        self.ai_sinyali.connect(self.ui.metin_kutusu_ai.setPlainText)
        self.ai_sinyali.connect(self.ai_metnini_oku)
        
        if hasattr(self.ui, 'btn_veri_goster'):
            self.ui.btn_veri_goster.clicked.connect(self.veri_istatistiklerini_goster)
            
        self.tahmin_modelini_yukle()
    
    def ui_ozellestir(self):
        self.ui.metin_kutusu.setReadOnly(True)
        self.ui.metin_kutusu_ai.setReadOnly(True)
        
        self.ui.rd_btn_eklenti_gizle.setCheckable(True)
        self.ui.rd_btn_eklenti_gizle.setAutoExclusive(False)
        
        self.ui.rd_btn_ai_ceviri.setCheckable(True)
        self.ui.rd_btn_ai_ceviri.setAutoExclusive(False)
        
        self.ui.rd_btn_sesli_oku.setCheckable(True)
        self.ui.rd_btn_sesli_oku.setAutoExclusive(False)
        
        self.lbl_guven = QLabel(self.ui.gb_kamera)
        self.lbl_guven.setGeometry(10, 500, 450, 30)
        self.lbl_guven.setStyleSheet("color: #00FF00; font-weight: bold; font-size: 14px; background-color: rgba(0,0,0,100); padding: 5px;")
        self.lbl_guven.setText("")
        self.lbl_guven.setText("")
        self.lbl_guven.show()

    def sesli_oku_durum_degis(self, checked):
        self.sesli_oku_aktif = checked
        if checked:
            print("Sesli Oku: AÇIK")
            metin = self.ui.metin_kutusu_ai.toPlainText() if self.ai_modu else self.ui.metin_kutusu.toPlainText()
            if metin and metin.strip():
                self.metni_seslendir(metin)
                if self.ai_modu:
                    self.son_okunan_metin_ai = metin
        else:
             print("Sesli Oku: KAPALI")

    def metni_seslendir(self, metin):
        if not metin or not metin.strip(): return
        print(f"Seslendiriliyor: {metin}")

        try:
            from gtts import gTTS
            import tempfile
            
            tts = gTTS(text=metin, lang='tr', slow=False) 
            
            fd, path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            
            tts.save(path)
            
            if QT_MULTIMEDIA_VAR and self.medya_oynatici:
                url = QUrl.fromLocalFile(path)
                self.medya_oynatici.setMedia(QMediaContent(url))
                self.medya_oynatici.play()
            else:
                os.startfile(path)
            return

        except ImportError:
            pass
        except Exception as e:
            pass

        try:
            import pyttsx3
            motor = pyttsx3.init()
            
            motor.setProperty('rate', 125) 
            
            voices = motor.getProperty('voices')
            tr_voice_id = None
            
            for voice in voices:
                if "turkish" in voice.name.lower() or "tr" in voice.id.lower() or "tur" in voice.id.lower():
                    tr_voice_id = voice.id
                    break
            
            if tr_voice_id:
                motor.setProperty('voice', tr_voice_id)
            
            motor.say(metin)
            motor.runAndWait()
        except Exception as e:
             print(f"Ses Hatasi: {e}")

    def ai_metnini_oku(self, yeni_metin):
        if not self.sesli_oku_aktif: return
        
        okunacak = ""
        if yeni_metin.startswith(self.son_okunan_metin_ai):
             okunacak = yeni_metin[len(self.son_okunan_metin_ai):].strip()
        else:
             okunacak = yeni_metin
             
        if okunacak:
            self.metni_seslendir(okunacak)
            
        self.son_okunan_metin_ai = yeni_metin

    def api_anahtari_iste(self):
        if self.api_key: return True
        
        if os.environ.get("GOOGLE_API_KEY"):
            self.api_key = os.environ.get("GOOGLE_API_KEY")
            return True
        
        print(">> API Anahtarı eksik. Ortam değişkeni (GOOGLE_API_KEY) ayarlı değil.")
        return False

    def tahmin_modelini_yukle(self):
        model_path = os.path.join(BASE_DIR, 'model', 'hareket_modeli.h5')
        
        print(f"--------------------------------------------------")
        print(f"Model Dosyası Aranıyor: {model_path}")
        
        if os.path.exists(model_path):
            try:
                from tensorflow.keras.models import load_model
                import shutil
                import tempfile
                
                fd, temp_path = tempfile.mkstemp(suffix='.h5')
                os.close(fd)
                
                print(f"Dosya yolu karakter hatasını çözmek için geçici kopya oluşturuluyor...")
                shutil.copy(model_path, temp_path)
                
                try:
                    self.model = load_model(temp_path)
                    print(">> MODEL BAŞARIYLA YÜKLENDİ.")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                self.eylemleri_yukle()
                
            except Exception as e:
                print(f"!! MODEL YÜKLENİRKEN GENEL HATA: {e}")
                import traceback
                traceback.print_exc()
                self.model = None
        else:
            print(f"!! MODEL DOSYASI BULUNAMADI.")
            print("Mevcut dizindeki dosyalar:")
            try:
                print(os.listdir(os.path.join(BASE_DIR, 'model')))
            except: pass
        print(f"--------------------------------------------------")

    def eylemleri_yukle(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        veri_yolu_tam = os.path.join(script_dir, VERI_YOLU)
        
        if os.path.exists(veri_yolu_tam):
             self.eylemler = np.array([f for f in os.listdir(veri_yolu_tam) if os.path.isdir(os.path.join(veri_yolu_tam, f))])
             print(f"Tanımlı Hareketler: {self.eylemler}")
        else:
             print(f"Veri klasörü bulunamadı: {veri_yolu_tam}")
    
    def goz_kirpma_algila(self, sonuclar):
        kirpma = False
        durum = "Bilinmiyor"
        renk = (128, 128, 128)

        if not sonuclar.face_landmarks:
            return False, durum, renk
        
        sol_goz_idx = [33, 160, 158, 133, 153, 144]
        sag_goz_idx = [362, 385, 387, 263, 373, 380]
        
        def ear_hesapla(noktalar):
            A = ((noktalar[1].x - noktalar[5].x)**2 + (noktalar[1].y - noktalar[5].y)**2)**0.5
            B = ((noktalar[2].x - noktalar[4].x)**2 + (noktalar[2].y - noktalar[4].y)**2)**0.5
            C = ((noktalar[0].x - noktalar[3].x)**2 + (noktalar[0].y - noktalar[3].y)**2)**0.5
            return (A + B) / (2.0 * C) if C > 0 else 0
            
        sol_goz = [sonuclar.face_landmarks.landmark[i] for i in sol_goz_idx]
        sag_goz = [sonuclar.face_landmarks.landmark[i] for i in sag_goz_idx]
        
        ort_ear = (ear_hesapla(sol_goz) + ear_hesapla(sag_goz)) / 2.0
        
        self.goz_durum_tamponu.append(ort_ear)
        if len(self.goz_durum_tamponu) > 3:
            self.goz_durum_tamponu.pop(0)
            
        smooth_ear = sum(self.goz_durum_tamponu) / len(self.goz_durum_tamponu)
        
        ESIK_DEGER = 0.34 
        
        if smooth_ear < ESIK_DEGER:
            durum = "Kapali"
            renk = (0, 0, 255)
            if self.kirpma_bekleme_suresi == 0:
                kirpma = True
                print(">> GÖZ KIRPMA ALGILANDI! (Bekleme süresi başlatılıyor...)")
        else:
            durum = "Acik"
            renk = (0, 255, 0)
            
        return kirpma, durum, renk

    def kare_guncelle(self):
        ret, cerceve = self.kamera.read()
        if not ret: return

        if self.kirpma_bekleme_suresi > 0:
            self.kirpma_bekleme_suresi -= 1

        goruntu, sonuclar = ida.mediapipe_algilama(cerceve, self.holistik)
        
        if self.eklentileri_goster:
            ida.stil_ile_ciz(goruntu, sonuclar)
        
        if self.veri_toplayici.aktif:
            anahtar_noktalar = ida.anahtar_noktalari_cikar(sonuclar)
            self.veri_toplayici.isleme_adimi(anahtar_noktalar, goruntu)
            
        else:
            pass

            if not self.egitim_yapiliyor:
                anahtar_noktalar = ida.anahtar_noktalari_cikar(sonuclar)
                self.canli_tampon.append(anahtar_noktalar)
                if len(self.canli_tampon) > SEKANS_UZUNLUGU:
                    self.canli_tampon.pop(0)
                    
                kirpma, durum, renk = self.goz_kirpma_algila(sonuclar)
                
                ui_metin = f"Goz: {durum}"
                
                if self.kirpma_bekleme_suresi > 0:
                    if self.kirpma_bekleme_suresi > 40:
                         renk = (0, 0, 255)
                         ui_metin = "KIRPMA ALGILANDI"
                    else:
                         renk = (180, 180, 180)
                         ui_metin = "BEKLEME SURESI"

                if self.eklentileri_goster:
                    cv2.circle(goruntu, (30, 30), 10, renk, -1)
                    cv2.putText(goruntu, ui_metin, (50, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)
                    
                    if self.kirpma_bekleme_suresi > 0:
                        bar_x = 50
                        bar_y = 45
                        bar_w = 100
                        bar_h = 5
                        
                        cv2.rectangle(goruntu, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (100, 100, 100), -1)
                        
                        oran = self.kirpma_bekleme_suresi / 60.0
                        aktif_w = int(bar_w * oran)
                        
                        cv2.rectangle(goruntu, (bar_x, bar_y), (bar_x + aktif_w, bar_y + bar_h), (255, 255, 0), -1)

                if kirpma:

                    if not self.model:
                        print("UYARI: Model yüklenmemiş! Tahmin yapılamıyor.")
                        return

                    if self.kirpma_bekleme_suresi > 0:
                         pass
                    elif len(self.canli_tampon) < SEKANS_UZUNLUGU:
                        print(f"UYARI: Tampon henüz dolmadı ({len(self.canli_tampon)}/{SEKANS_UZUNLUGU}). Biraz daha bekleyin.")
                    else:
                        print("Tahmin başlatılıyor...")
                        self.kirpma_bekleme_suresi = 60
                        threading.Thread(target=self.tahmin_yap_ve_guncelle, args=(list(self.canli_tampon),)).start()

        if self.egitim_yapiliyor:
             cv2.putText(goruntu, "MODEL EGITILIYOR... LUTFEN BEKLEYIN", (50, int(goruntu.shape[0]/2)), 
                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Normal kamera görüntüsü
        h, w, ch = goruntu.shape
        bytes_per_line = ch * w
        qt_format = QImage(goruntu.data, w, h, bytes_per_line, QImage.Format_BGR888)
        p = qt_format.scaled(self.ui.label_kamera_ekrani.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.ui.label_kamera_ekrani.setPixmap(QPixmap.fromImage(p))

    GUVEN_ESIGI = 0.65

    def tahmin_yap_ve_guncelle(self, tampon_veri):
        girdi_np = np.array(tampon_veri)
        if np.max(np.abs(girdi_np)) < 0.01:
            self.tahmin_sinyali.emit("Hareket Tespit Edilemedi (Eller Yok)", 0.0)
            return

        if not self.model: return
        
        try:
            girdi = np.expand_dims(tampon_veri, axis=0)
            sonuc = self.model.predict(girdi)[0]
            
            en_iyi_indeksler = np.argsort(sonuc)[-3:][::-1]
            
            lider_idx = en_iyi_indeksler[0]
            lider_guven = sonuc[lider_idx]
            lider_eylem = self.eylemler[lider_idx]
            
            ikinci_idx = en_iyi_indeksler[1] if len(en_iyi_indeksler) > 1 else -1
            ikinci_guven = sonuc[ikinci_idx] if ikinci_idx != -1 else 0
            
            print(f"\n--- TAHMİN DETAYLARI ---")
            print(f"1. {lider_eylem}: {lider_guven:.4f}")
            if ikinci_idx != -1:
                print(f"2. {self.eylemler[ikinci_idx]}: {ikinci_guven:.4f}")
            
            if lider_guven < self.GUVEN_ESIGI:
                print(f">> REDDEDILDI: Güven skoru düşük ({lider_guven:.4f} < {self.GUVEN_ESIGI})")
                self.tahmin_sinyali.emit("Belirsiz Hareket", float(lider_guven))
                return

            fark = lider_guven - ikinci_guven
            if fark < 0.1:
                print(f">> REDDEDILDI: Kararsız tahmin (Fark: {fark:.4f})")
                self.tahmin_sinyali.emit("Kararsiz Hareket", float(lider_guven))
                return
                
            self.tahmin_sinyali.emit(lider_eylem, float(lider_guven))
            
        except Exception as e:
            print(f"Tahmin hatasi: {e}")

    def sonuc_guncelle_gui(self, eylem, guven):
        try:
            self.lbl_guven.setText(f"Algilanan: {eylem} | Dogruluk: %{guven*100:.1f}")
            
            if guven >= self.GUVEN_ESIGI: 
                mevcut_metin = self.ui.metin_kutusu.toPlainText().strip()
                kelimeler = mevcut_metin.split(" ")
                son_kelime = kelimeler[-1] if kelimeler else ""
                
                if eylem == son_kelime:
                    print(f">> Tekrarlanan kelime engellendi: {eylem}")
                    return

                self.hareketi_kaydet(eylem, guven)

                yeni_metin = mevcut_metin + " " + eylem if mevcut_metin else eylem
                self.ui.metin_kutusu.setPlainText(yeni_metin)
                
                if self.sesli_oku_aktif and not self.ai_modu:
                    threading.Thread(target=self.metni_seslendir, args=(eylem,)).start()
                
                if self.ai_modu:
                    threading.Thread(target=self.ai_ile_duzelt).start()
        except Exception as e:
            print(f"GUI Guncelleme hatasi: {e}")

    def hareketi_kaydet(self, kelime, dogruluk):
        import csv
        from datetime import datetime
        
        dosya_adi = os.path.join(BASE_DIR, 'data', 'Hareket_Gecmisi.csv')
        
        try:
            dosya_yoktu = not os.path.exists(dosya_adi)
            
            simdi = datetime.now()
            tarih_str = simdi.strftime("%d.%m.%Y")
            saat_str = simdi.strftime("%H:%M:%S")
            
            with open(dosya_adi, mode='a', newline='', encoding='utf-8-sig') as f:
                yazici = csv.writer(f, delimiter=';')
                
                if dosya_yoktu:
                    yazici.writerow(["Tarih", "Saat", "Algılanan Hareket", "Doğruluk Oranı"])
                
                yazici.writerow([tarih_str, saat_str, kelime, f"{dogruluk:.2f}"])
                
        except Exception as e:
            print(f"Dosya Kayit Hatasi: {e}")

    def ai_ile_duzelt(self):
        if not self.ai_modu: return

        try:
            metin = self.ui.metin_kutusu.toPlainText().strip()
            if not metin or len(metin) < 2: return
            
            ham_kelimeler = metin.split()
            
            temiz_kelimeler = []
            if ham_kelimeler:
                temiz_kelimeler.append(ham_kelimeler[0])
                for i in range(1, len(ham_kelimeler)):
                    k_onceki = ham_kelimeler[i-1].lower()
                    k_simdiki = ham_kelimeler[i].lower()
                    
                    if k_onceki != k_simdiki:
                        temiz_kelimeler.append(ham_kelimeler[i])
            
            yeni_metin = " ".join(temiz_kelimeler)
            yeni_metin_lower = yeni_metin.lower()
            
            if "ben iyi" in yeni_metin_lower or "ben İyi" in yeni_metin_lower:
                yeni_metin = "Ben iyiyim"
                
            elif "merhaba nasılsın" in yeni_metin_lower:
                yeni_metin = "Merhaba, nasılsın?"
                
            elif "teşekkürler" in yeni_metin_lower and "ederim" not in yeni_metin_lower:
                 yeni_metin = "Teşekkür ederim"

            elif "adın ne" in yeni_metin_lower:
                yeni_metin = "Adın ne?"

            elif "nasılsın" in yeni_metin_lower and len(temiz_kelimeler) == 1:
                 yeni_metin = "Nasılsın?"
            
            else:
                if len(yeni_metin) > 0:
                    yeni_metin = yeni_metin[0].upper() + yeni_metin[1:]

            if yeni_metin and yeni_metin[-1] not in ['.', '?', '!']:
                 yeni_metin += "."

            self.ai_sinyali.emit(yeni_metin)
                
        except Exception as e:
            print(f"Yerel İşleme Hatası: {e}")

    def api_anahtari_iste(self):
        if self.api_key: return True
        
        if os.environ.get("GOOGLE_API_KEY"):
            self.api_key = os.environ.get("GOOGLE_API_KEY")
            return True
            
        print(">> API Anahtarı eksik. 'API Anahtarı Gir' butonu ile anahtar ekleyin.")
        return False

    def gemini_api_cagir(self, metin):
        if not self.api_key: return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        
        prompt = f"""
        Aşağıdaki bozuk Türkçe işaret dili çıktılarını, dil bilgisi kurallarına uygun, anlamlı ve tam Türkçe cümlelere çevir.
        Girdi: "{metin}"
        Çıktı (Sadece cümleyi yaz):
        """
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                try:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    return text.strip()
                except (KeyError, IndexError):
                    return None
        except Exception as e:
            print(f"Gemini API Çağrısı Başarısız: {e}")
            return None

    def veri_istatistiklerini_goster(self):
        print("Butona basildi: VERILERI GOSTER VE TEMIZLE")
        yol = VERI_YOLU
        
        if not os.path.exists(yol):
             print("\n[HATA] Veri klasoru bulunamadi.")
             return
             
        print("\n" + "="*40)
        print("       VERI SETI TEMIZLIK VE ISTATISTIK")
        print("="*40)
        
        silinen_toplam = 0
        tum_dosyalar_listesi = []
        for root, dirs, files in os.walk(yol):
            for file in files:
                if file.endswith(".npy"):
                    tum_dosyalar_listesi.append(os.path.join(root, file))
        
        print(f"Toplam {len(tum_dosyalar_listesi)} dosya taranıyor...")
        
        for dosya_yolu in tum_dosyalar_listesi:
            try:
                data = np.load(dosya_yolu)
                non_zero_frames = np.sum(np.abs(data) > 0.001, axis=1)
                empty_frame_count = np.sum(non_zero_frames == 0)
                
                if empty_frame_count > 15:
                    os.remove(dosya_yolu)
                    print(f" [SILINDI] Yetersiz Veri ({empty_frame_count} boş frame): {os.path.basename(dosya_yolu)}")
                    silinen_toplam += 1
            except: pass
            
        print(f"\n>> Temizlik Bitti. Toplam {silinen_toplam} hatali dosya silindi.\n")
        print("-" * 40)
        
        toplam = 0
        klasorler = [f for f in os.listdir(yol) if os.path.isdir(os.path.join(yol, f))]
        if not klasorler:
             print("Hic veri sinifi bulunamadi.")
        else:
            for k in klasorler:
                 dosya_sayisi = len([f for f in os.listdir(os.path.join(yol, k)) if f.endswith('.npy')])
                 print(f" • {k:<20} : {dosya_sayisi} ornek")
                 toplam += dosya_sayisi
        print("-" * 40)
        print(f" TOPLAM VIDEO SAYISI     : {toplam}")
        print("="*40 + "\n")
        pass

    def eklentileri_goster_gizle(self, secili):
        print(f"Eklenti Gizleme Modu {'Acildi' if secili else 'Kapatildi'}.")
        self.eklentileri_goster = not secili
        
    def ai_modu_degis(self, secili):
        print(f"AI Ceviri Modu {'Acildi' if secili else 'Kapatildi'}.")
        self.ai_modu = secili
        
    def muzik_bitti_kontrol(self, durum):
        if durum == 7: 
            print(">> Müzik bitti.")
            
    def metni_temizle(self):
        print("Butona basildi: SIL (Metin Temizlendi)")
        self.ui.metin_kutusu.clear()
        self.ui.metin_kutusu_ai.clear()
        self.son_okunan_metin_ai = ""
        

    def egitimi_baslat(self):
        print("Butona basildi: EGITIME BASLA")
        etiket = self.ui.metin_kutusu_egitim.toPlainText().strip()
        if not etiket:
             self.goster_ozel_mesaj("uyari", "Uyari", "Lutfen bir hareket ismi girin.")
             return
        
        basarili = self.veri_toplayici.baslat(etiket)
        if basarili:
             print(f"Toplama Basladi: {etiket}")

    def goster_ozel_mesaj(self, tur, baslik, icerik):
        msg = QMessageBox(self)
        msg.setWindowTitle(baslik)
        msg.setText(icerik)
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
               background-color: #333333;
               color: white;
               padding: 5px 15px;
               border: 1px solid #555;
               border-radius: 4px;
            }
            QPushButton:hover {
               background-color: #444;
            }
        """)

        if tur == "uyari":
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return None
        elif tur == "soru":
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            return msg.exec_()
            
    def egitimi_durdur(self):
        print("Butona basildi: EGITIMI DURDUR")
        if self.veri_toplayici.aktif:
            self.veri_toplayici.durdur()
            
        q = self.goster_ozel_mesaj("soru", "Model Egitimi", "Veri toplama bitti. Model egitilsin mi?")
        if q == QMessageBox.Yes:
            self.egitim_yapiliyor = True
            print("Model eğitimi başlatılıyor... Arayüz bir süre donabilir.")
            threading.Thread(target=self.arka_planda_egit).start()
            
    def arka_planda_egit(self):
        try:
            print(">> Background thread: Eğitim metodu çağrılıyor...")
            sonuc = self.egitici.egit()
            print(f"Egitim Sonucu: {sonuc}")
            self.egitim_yapiliyor = False
            
            self.tahmin_modelini_yukle()
            print("Yeni model aktif!")
        except Exception as e:
            print(f"!!! EĞİTİM SIRASINDA HATA OLUŞTU: {e}")
            import traceback
            traceback.print_exc()
            self.egitim_yapiliyor = False

    def closeEvent(self, event):
        self.kamera.release()
        event.accept()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        pencere = IsaretDiliUygulamasi()
        pencere.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"\n\n!!! PROGRAM BAŞLATMA HATASI !!!")
        print(f"Hata: {e}")
        import traceback
        traceback.print_exc()
        input("\nHata detayları yukarıda. Kapatmak için Enter'a basın...")
