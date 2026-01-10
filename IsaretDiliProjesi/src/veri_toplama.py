import os
import cv2
import numpy as np
import time

class VeriToplamaModulu:
    def __init__(self, veri_yolu='MP_Data', sekans_uzunlugu=45, hazirlik_suresi=30):
        self.veri_yolu = veri_yolu
        self.sekans_uzunlugu = sekans_uzunlugu
        self.hazirlik_suresi = hazirlik_suresi
        
        self.aktif = False
        self.klasor_adi = ""
        self.video_sirasi = 0
        self.frame_sayaci = 0
        self.faz = "hazirlik"
        self.toplanan_veri = []
        
    def baslat(self, klasor_adi):
        if not klasor_adi: return False
        
        self.klasor_adi = klasor_adi
        self.aktif = True
        self.toplanan_veri = []
        self.frame_sayaci = 0
        self.faz = "hazirlik"
        
        yol = os.path.join(self.veri_yolu, klasor_adi)
        if os.path.exists(yol):
             dosyalar = [f for f in os.listdir(yol) if f.endswith('.npy')]
             self.video_sirasi = len(dosyalar)
        else:
             self.video_sirasi = 0
             
        print(f"Veri toplama basladi: {klasor_adi} (Video: {self.video_sirasi})")
        return True

    def durdur(self):
        self.aktif = False
        print("Veri toplama durduruldu.")

    def isleme_adimi(self, anahtar_noktalar, goruntu):
        if not self.aktif: return
        
        h, w = goruntu.shape[:2]
        
        cubuk_w = w - 40
        x, y = 20, h - 40
        
        if self.faz == "hazirlik":
            yuzde = self.frame_sayaci / self.hazirlik_suresi
            cv2.rectangle(goruntu, (x, y), (x + int(cubuk_w * yuzde), y + 20), (0, 255, 255), -1)
            
            yazi = f"HAZIRLAN: Video {self.video_sirasi + 1}"
            cv2.putText(goruntu, yazi, (int(w/4), int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            self.frame_sayaci += 1
            if self.frame_sayaci >= self.hazirlik_suresi:
                self.faz = "kayit"
                self.frame_sayaci = 0
                
        elif self.faz == "kayit":
            yuzde = self.frame_sayaci / self.sekans_uzunlugu
            cv2.rectangle(goruntu, (x, y), (x + int(cubuk_w * yuzde), y + 20), (0, 0, 255), -1)
            
            cv2.putText(goruntu, "KAYIT", (int(w/2)-50, int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            
            self.toplanan_veri.append(anahtar_noktalar)
            self.frame_sayaci += 1
            
            if self.frame_sayaci >= self.sekans_uzunlugu:
                self._kaydet()
                
    def _kaydet(self):
        yol = os.path.join(self.veri_yolu, self.klasor_adi)
        os.makedirs(yol, exist_ok=True)
        
        dosya_yolu = os.path.join(yol, str(self.video_sirasi))
        np.save(dosya_yolu, np.array(self.toplanan_veri))
        
        print(f"Video {self.video_sirasi} kaydedildi.")
        self.video_sirasi += 1
        
        self.toplanan_veri = []
        self.frame_sayaci = 0
        self.faz = "hazirlik"
