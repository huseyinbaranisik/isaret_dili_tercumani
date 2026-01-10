import cv2
import numpy as np

class SahteHolistik:
    def process(self, image):
        class Sonuclar:
            left_hand_landmarks = None
            right_hand_landmarks = None
            face_landmarks = None
        return Sonuclar()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

try:
    import mediapipe as mp
    mp_holistik = mp.solutions.holistic
    mp_cizim = mp.solutions.drawing_utils
    MEDIAPIPE_VAR = True
except (ImportError, AttributeError) as e:
    print(f"UYARI: MediaPipe yuklenemedi: {e}")
    MEDIAPIPE_VAR = False
    
    class SahteCozumler:
        Holistic = SahteHolistik
        HAND_CONNECTIONS = []
        
    mp_holistik = SahteCozumler
    mp_cizim = None


def mediapipe_algilama(goruntu, model):
    if not MEDIAPIPE_VAR:
        return goruntu, SahteHolistik().process(goruntu)
        
    goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB) 
    goruntu.flags.writeable = False                  
    sonuclar = model.process(goruntu)                 
    goruntu.flags.writeable = True                   
    goruntu = cv2.cvtColor(goruntu, cv2.COLOR_RGB2BGR) 
    return goruntu, sonuclar

def stil_ile_ciz(goruntu, sonuclar):
    if not MEDIAPIPE_VAR: return

    mp_cizim.draw_landmarks(
        goruntu, sonuclar.left_hand_landmarks, mp_holistik.HAND_CONNECTIONS,
        mp_cizim.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
        mp_cizim.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
    )
    mp_cizim.draw_landmarks(
        goruntu, sonuclar.right_hand_landmarks, mp_holistik.HAND_CONNECTIONS,
        mp_cizim.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
        mp_cizim.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
    )

def anahtar_noktalari_cikar(sonuclar):
    if not sonuclar:
        return np.zeros(21*3 + 21*3)
        
    sol_el = np.array([[res.x, res.y, res.z] for res in sonuclar.left_hand_landmarks.landmark]).flatten() if sonuclar.left_hand_landmarks else np.zeros(21*3)
    
    sag_el = np.array([[res.x, res.y, res.z] for res in sonuclar.right_hand_landmarks.landmark]).flatten() if sonuclar.right_hand_landmarks else np.zeros(21*3)
    
    
    return np.concatenate([sol_el, sag_el])

