# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'arayuz.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Manual conversion due to missing pyuic5
#

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1830, 600)
        main_window.setFixedSize(1830, 600) # Pencere boyutunu sabitle
        main_window.setStyleSheet("/* Arka plan rengi (Koyu Siyah) */\n"
"background-color: #121212;\n"
"QMessageBox {\n"
"    background-color: #121212;\n"
"}\n"
"QMessageBox QLabel {\n"
"    color: white;\n"
"}")
        self.gb_kamera = QtWidgets.QGroupBox(main_window)
        self.gb_kamera.setGeometry(QtCore.QRect(10, 10, 711, 571))
        self.gb_kamera.setStyleSheet("QGroupBox {\n"
"    border: 2px solid #555555; \n"
"    border-radius: 12px;\n"
"    margin-top: 1.5ex; \n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; \n"
"    padding: 0 15px;\n"
"}")
        self.gb_kamera.setObjectName("gb_kamera")
        self.label_kamera_ekrani = QtWidgets.QLabel(self.gb_kamera)
        self.label_kamera_ekrani.setGeometry(QtCore.QRect(10, 20, 691, 541))
        self.label_kamera_ekrani.setMinimumSize(QtCore.QSize(640, 480))
        self.label_kamera_ekrani.setAutoFillBackground(False)
        self.label_kamera_ekrani.setStyleSheet("background-color: black;\n"
"border: 2px solid greY;")
        self.label_kamera_ekrani.setText("")
        self.label_kamera_ekrani.setObjectName("label_kamera_ekrani")
        
        # --- Butonlar GroupBox ---
        self.gb_butonlar = QtWidgets.QGroupBox(main_window)
        self.gb_butonlar.setGeometry(QtCore.QRect(740, 10, 261, 571))
        self.gb_butonlar.setStyleSheet("QGroupBox {\n"
"    border: 2px solid #555555; \n"
"    border-radius: 12px;\n"
"    margin-top: 1.5ex; \n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; \n"
"    padding: 0 15px;\n"
"}")
        self.gb_butonlar.setObjectName("gb_butonlar")

        # Sesli Oku GroupBox Wrapper
        self.gb_sesli_wrapper = QtWidgets.QGroupBox(self.gb_butonlar)
        self.gb_sesli_wrapper.setGeometry(QtCore.QRect(10, 20, 241, 61))
        self.gb_sesli_wrapper.setStyleSheet("QGroupBox {\n"
"    border: none;\n"
"    background: transparent;\n"
"}")
        self.gb_sesli_wrapper.setTitle("")
        self.gb_sesli_wrapper.setObjectName("gb_sesli_wrapper")

        # Sesli Oku Radio Button
        self.rd_btn_sesli_oku = QtWidgets.QRadioButton(self.gb_sesli_wrapper)
        self.rd_btn_sesli_oku.setGeometry(QtCore.QRect(10, 10, 221, 41))
        self.rd_btn_sesli_oku.setStyleSheet("QRadioButton {\n"
"    background-color: #6A1B9A;\n"
"    color: white;   \n"
"    font-weight: bold;      \n"
"    font-size: 20px;        \n"
"    border-radius: 15px;      \n"
"    border: none;            \n"
"    padding: 0px;           \n"
"    text-align: center;     \n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"}\n"
"\n"
"QRadioButton:hover {\n"
"    background-color: #8E24AA;\n"
"}\n"
"\n"
"QRadioButton:checked {\n"
"    background-color: #4A148C;  \n"
"}\n"
"\n"
"QRadioButton:pressed {\n"
"    background-color: #4A148C;  \n"
"}")
        self.rd_btn_sesli_oku.setObjectName("rd_btn_sesli_oku")

        # Sil
        self.btn_sil = QtWidgets.QPushButton(self.gb_butonlar)
        self.btn_sil.setGeometry(QtCore.QRect(20, 80, 221, 41))
        self.btn_sil.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: #6A1B9A; \n"
"    color: white;          \n"
"    font-weight: bold;    \n"
"    font-size: 20px;          \n"
"    border-radius: 15px;    \n"
"    border: none;           \n"
"    padding: 10px;          \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8E24AA; \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4A148C;\n"
"    padding-top: 12px;      \n"
"    padding-left: 12px;       \n"
"}")
        self.btn_sil.setObjectName("btn_sil")

        # Eklenti Gizle
        self.rd_btn_eklenti_gizle = QtWidgets.QRadioButton(self.gb_butonlar)
        self.rd_btn_eklenti_gizle.setGeometry(QtCore.QRect(20, 130, 221, 41))
        self.rd_btn_eklenti_gizle.setStyleSheet("QRadioButton {\n"
"    background-color: #6A1B9A;\n"
"    color: white;   \n"
"    font-weight: bold;      \n"
"    font-size: 20px;        \n"
"    border-radius: 15px;      \n"
"    border: none;            \n"
"    padding: 0px;           \n"
"    text-align: center;     \n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"}\n"
"\n"
"QRadioButton:hover {\n" # New Hover
"    background-color: #8E24AA;\n"
"}\n"
"\n"
"QRadioButton:checked {\n"
"    background-color: #4A148C;  \n"
"}\n"
"\n"
"QRadioButton:pressed {\n"
"    background-color: #4A148C;  \n"
"}")
        self.rd_btn_eklenti_gizle.setObjectName("rd_btn_eklenti_gizle")

        # GroupBox (AI Ceviri)
        self.groupBox = QtWidgets.QGroupBox(self.gb_butonlar)
        self.groupBox.setGeometry(QtCore.QRect(10, 170, 241, 61))
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    border: none;\n"
"    background: transparent;\n"
"}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        self.rd_btn_ai_ceviri = QtWidgets.QRadioButton(self.groupBox)
        self.rd_btn_ai_ceviri.setGeometry(QtCore.QRect(10, 10, 221, 41))
        self.rd_btn_ai_ceviri.setStyleSheet("QRadioButton {\n"
"    background-color: #6A1B9A;\n"
"    color: white;   \n"
"    font-weight: bold;      \n"
"    font-size: 20px;        \n"
"    border-radius: 15px;      \n"
"    border: none;            \n"
"    padding: 0px;           \n"
"    text-align: center;     \n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"}\n"
"\n"
"QRadioButton:hover {\n" # New Hover
"    background-color: #8E24AA;\n"
"}\n"
"\n"
"QRadioButton:checked {\n"
"    background-color: #4A148C;  \n"
"}\n"
"\n"
"QRadioButton:pressed {\n"
"    background-color: #4A148C;  \n"
"}")
        self.rd_btn_ai_ceviri.setObjectName("rd_btn_ai_ceviri")

        # Veri Göster (NEW)
        self.btn_veri_goster = QtWidgets.QPushButton(self.gb_butonlar)
        self.btn_veri_goster.setGeometry(QtCore.QRect(20, 230, 221, 41))
        self.btn_veri_goster.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: #6A1B9A; \n"
"    color: white;          \n"
"    font-weight: bold;    \n"
"    font-size: 20px;          \n"
"    border-radius: 15px;    \n"
"    border: none;           \n"
"    padding: 10px;          \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8E24AA; \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4A148C;\n"
"    padding-top: 12px;      \n"
"    padding-left: 12px;       \n"
"}")
        self.btn_veri_goster.setObjectName("btn_veri_goster")

        # gb_butonlar_2 (Egitim)
        self.gb_butonlar_2 = QtWidgets.QGroupBox(self.gb_butonlar)
        self.gb_butonlar_2.setGeometry(QtCore.QRect(10, 330, 241, 231))
        self.gb_butonlar_2.setStyleSheet("QGroupBox {\n"
"    border: 2px solid #555555; \n"
"    border-radius: 12px;\n"
"    margin-top: 1.5ex; \n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; \n"
"    padding: 0 15px;\n"
"}")
        self.gb_butonlar_2.setTitle("Eğitim ")
        self.gb_butonlar_2.setObjectName("gb_butonlar_2")

        # Egitime Basla
        self.btn_egitime_basla = QtWidgets.QPushButton(self.gb_butonlar_2)
        self.btn_egitime_basla.setGeometry(QtCore.QRect(10, 20, 221, 61))
        self.btn_egitime_basla.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: #6A1B9A; \n"
"    color: white;      \n"
"    font-weight: bold;\n"
"    font-size: 20px;          \n"
"    border-radius: 15px;     \n"
"    border: none;           \n"
"    padding: 10px;             \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8E24AA; \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4A148C;\n"
"    padding-top: 12px;\n"
"    padding-left: 12px;\n"
"}")
        self.btn_egitime_basla.setObjectName("btn_egitime_basla")

        # Egitimi Durdur
        self.btn_egitimi_durdur = QtWidgets.QPushButton(self.gb_butonlar_2)
        self.btn_egitimi_durdur.setGeometry(QtCore.QRect(10, 90, 221, 61))
        self.btn_egitimi_durdur.setStyleSheet("QPushButton {\n"
"    background-color: #6A1B9A;\n"
"    color: white;         \n"
"    font-weight: bold;   \n"
"    font-size: 20px;        \n"
"    border-radius: 15px;      \n"
"    border: none;           \n"
"    padding: 10px;             \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8E24AA; \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4A148C;\n"
"    padding-top: 12px;         \n"
"    padding-left: 12px;  \n"
"}")
        self.btn_egitimi_durdur.setObjectName("btn_egitimi_durdur")

        # Metin Kutusu Egitim
        self.metin_kutusu_egitim = QtWidgets.QTextEdit(self.gb_butonlar_2)
        self.metin_kutusu_egitim.setGeometry(QtCore.QRect(10, 160, 221, 61))
        self.metin_kutusu_egitim.setStyleSheet("/* Arka plan rengi (Koyu Gri) */\n"
"background-color: #2C2C2C;\n"
"color: white;\n"
"border-radius: 15px;")
        self.metin_kutusu_egitim.setObjectName("metin_kutusu_egitim")
        
        # --- Metin Kutusu Egitim Ozel Ayarlar ---
        # Ortala
        self.metin_kutusu_egitim.document().setDefaultTextOption(QtGui.QTextOption(QtCore.Qt.AlignCenter))
        # Buyuk Font
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.metin_kutusu_egitim.setFont(font)
        # Otomatik Boyutlandirma Baglantisi
        self.metin_kutusu_egitim.textChanged.connect(lambda: self.font_boyutunu_ayarla(self.metin_kutusu_egitim, 26))



        # --- Metinler GroupBox ---
        self.gb_metinler = QtWidgets.QGroupBox(main_window)
        self.gb_metinler.setGeometry(QtCore.QRect(1020, 10, 801, 571))
        self.gb_metinler.setStyleSheet("QGroupBox {\n"
"    border: 2px solid #555555; \n"
"    border-radius: 12px;\n"
"    margin-top: 1.5ex; \n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; \n"
"    padding: 0 15px;\n"
"}")
        self.gb_metinler.setObjectName("gb_metinler")
        self.metin_kutusu = QtWidgets.QTextEdit(self.gb_metinler)
        self.metin_kutusu.setGeometry(QtCore.QRect(10, 20, 781, 251))
        self.metin_kutusu.setStyleSheet("/* Arka plan rengi (Koyu Gri) */\n"
"background-color: #2C2C2C;\n"
"color: white;\n"
"border-radius: 15px;")
        
        self.metin_kutusu.setObjectName("metin_kutusu")
        
        # --- Metin Kutusu Ozel Ayarlar ---
        self.metin_kutusu.document().setDefaultTextOption(QtGui.QTextOption(QtCore.Qt.AlignCenter))
        f_mk = QtGui.QFont()
        f_mk.setPointSize(20)
        f_mk.setBold(True)
        self.metin_kutusu.setFont(f_mk)
        self.metin_kutusu.textChanged.connect(lambda: self.font_boyutunu_ayarla(self.metin_kutusu, 20))
        self.metin_kutusu_ai = QtWidgets.QTextEdit(self.gb_metinler)
        self.metin_kutusu_ai.setGeometry(QtCore.QRect(10, 310, 781, 251))
        self.metin_kutusu_ai.setStyleSheet("/* Arka plan rengi (Koyu Gri) */\n"
"background-color: #2C2C2C;\n"
"color: white;\n"
"border-radius: 15px;")
        self.metin_kutusu_ai.setObjectName("metin_kutusu_ai")
        # --- Metin Kutusu AI Ozel Ayarlar ---
        self.metin_kutusu_ai.document().setDefaultTextOption(QtGui.QTextOption(QtCore.Qt.AlignCenter))
        f_ai = QtGui.QFont()
        f_ai.setPointSize(20)
        f_ai.setBold(True)
        self.metin_kutusu_ai.setFont(f_ai)
        self.metin_kutusu_ai.textChanged.connect(lambda: self.font_boyutunu_ayarla(self.metin_kutusu_ai, 20))
        self.line = QtWidgets.QFrame(self.gb_metinler)
        self.line.setGeometry(QtCore.QRect(0, 290, 821, 2))
        self.line.setStyleSheet("QFrame {\n"
"    background-color: #555555;\n"
"    \n"
"    min-height: 1.5px;\n"
"    max-height: 1.5px;\n"
" \n"
"    border: none;\n"
"}")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def font_boyutunu_ayarla(self, text_edit, max_font_size):
        try:
            # Sinyalleri gecici olarak durdur
            text_edit.blockSignals(True)
            
            # Scrollbarlari tamamen kapat
            text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            text_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            text = text_edit.toPlainText()
            
            # Bos metin kontrolu
            if not text.strip():
                font = text_edit.font()
                font.setPointSize(max_font_size)
                text_edit.setFont(font)
                text_edit.blockSignals(False)
                return

            # Viewport alanini al (metnin goruntulendigi alan)
            rect = text_edit.viewport().rect()
            # Kenar bosluklari icin padding birakiyoruz
            target_width = rect.width() - 20 
            target_height = rect.height()

            font = text_edit.font()
            found_size = 6 # Varsayilan minimum boyut
            
            # Max boyuttan baslayip kuculterek deneme yap
            for size in range(max_font_size, 5, -1):
                font.setPointSize(size)
                fm = QtGui.QFontMetrics(font)
                
                # Metnin bu fontla kaplayacagi alani hesapla
                # TextWordWrap bayragi coklu satiri hesaba katar
                bounding_rect = fm.boundingRect(
                    QtCore.QRect(0, 0, target_width, 0), 
                    QtCore.Qt.TextWordWrap, 
                    text
                )
                
                # Eger yukseklik sigiyorsa bu boyutu kullan ve donguden cik
                if bounding_rect.height() <= target_height:
                    found_size = size
                    break
            
            # Bulunan (veya min) boyutu uygula
            font.setPointSize(found_size)
            text_edit.setFont(font)
            
        except Exception as e:
            print(f"Font hatasi: {e}")
        finally:
            # Sinyalleri tekrar ac
            if text_edit.signalsBlocked():
                text_edit.blockSignals(False)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "İşaret dili çevirici"))
        self.gb_kamera.setTitle(_translate("main_window", "Canlı kamera"))
        self.gb_butonlar.setTitle(_translate("main_window", "Butonlar"))
        self.rd_btn_sesli_oku.setText(_translate("main_window", "         SESLİ OKU"))
        self.btn_sil.setText(_translate("main_window", "SİL"))
        self.rd_btn_eklenti_gizle.setText(_translate("main_window", "     EKLENTİ GİZLE"))
        self.rd_btn_ai_ceviri.setText(_translate("main_window", "         AI ÇEVİRİ"))
        self.btn_veri_goster.setText(_translate("main_window", "VERİLERİ GÖSTER"))
        # gb_butonlar_2 title set in object init
        self.btn_egitime_basla.setText(_translate("main_window", "EĞİTİME BAŞLA"))
        self.btn_egitimi_durdur.setText(_translate("main_window", "EĞİTİMİ DURDUR"))
        self.gb_metinler.setTitle(_translate("main_window", "Metinler"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QDialog()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
