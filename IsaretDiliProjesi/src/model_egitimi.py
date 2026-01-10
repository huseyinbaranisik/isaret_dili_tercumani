import os
import numpy as np
import os
import numpy as np

class ModelEgitici:
    def __init__(self, veri_yolu='MP_Data'):
        self.veri_yolu = veri_yolu
        self.eylemler = np.array([])
        self.label_map = {}
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_yolu = os.path.join(self.base_dir, 'model', 'hareket_modeli.h5')
        self.log_yolu = os.path.join(self.base_dir, 'logs')

    def veri_yukle(self):
        from tensorflow.keras.utils import to_categorical
        
        if not os.path.exists(self.veri_yolu):
            print("Veri yolu bulunamadi.")
            return None, None
            
        self.eylemler = np.array([f for f in os.listdir(self.veri_yolu) if os.path.isdir(os.path.join(self.veri_yolu, f))])
        self.label_map = {label:num for num, label in enumerate(self.eylemler)}
        
        sequences, labels = [], []
        
        for action in self.eylemler:
            action_path = os.path.join(self.veri_yolu, action)
            video_files = [f for f in os.listdir(action_path) if f.endswith('.npy')]
            
            for video_file in video_files:
                window = np.load(os.path.join(action_path, video_file))
                sequences.append(window)
                labels.append(self.label_map[action])
                
        return np.array(sequences), to_categorical(labels).astype(int)

    def egit(self, epoch_sayisi=700):
        from sklearn.model_selection import train_test_split
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from tensorflow.keras.callbacks import TensorBoard

        print(">> egit() fonskiyonu başladı.")
        print(">> Veriler yükleniyor...")
        X, y = self.veri_yukle()
        
        if X is None or len(X) == 0:
            print(">> HATA: X verisi boş!")
            return "Egitilecek veri yok."
            
        print(f">> Veri yüklendi. Boyutlar: X={X.shape}, y={y.shape}")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
        
        tb_callback = TensorBoard(log_dir=self.log_yolu)
        
        model = Sequential()
        model.add(LSTM(128, return_sequences=True, activation='relu', input_shape=(X.shape[1], X.shape[2])))
        model.add(Dropout(0.3))
        model.add(LSTM(256, return_sequences=True, activation='relu'))
        model.add(Dropout(0.3))
        model.add(LSTM(128, return_sequences=False, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.eylemler.shape[0], activation='softmax'))
        
        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        
        print("Egitim basliyor...")
        model.fit(X_train, y_train, epochs=epoch_sayisi, callbacks=[])
        
        model.save(self.model_yolu)
        return f"Model egitildi ve '{self.model_yolu}' olarak kaydedildi."

if __name__ == "__main__":
    egitici = ModelEgitici()
    print(egitici.egit())
