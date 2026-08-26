import os
import cv2
import pickle
import numpy as np
import mediapipe as mp

# المسارات
UNITY_STREAMING_ASSETS = r"C:\Users\Asmaaalfalahi\Downloads\StreamingAssets"
MODEL_PATH = os.path.join(os.path.expanduser('~/Downloads'), 'sign_language_model.pkl')

# إعداد MediaPipe Hands لاستخراج المعالم
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def extract_landmarks_from_video(video_path):
    """
    استخراج إحداثيات اليد لكل إطار داخل فيديو الكلمة
    """
    cap = cv2.VideoCapture(video_path)
    data_sequences = []
    
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # تجميع إحداثيات (x, y, z) لكل مصلب في اليد
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])
                    data_sequences.append(landmarks)
                    
    cap.release()
    return data_sequences

def train_model_from_streaming_assets():
    print("\n[⏳] جاري البدء بتعلم الكلمات من فيديوهات StreamingAssets...")
    
    if not os.path.exists(UNITY_STREAMING_ASSETS):
        print(f"[!] خطأ: مسار المجلد غير موجود: {UNITY_STREAMING_ASSETS}")
        return

    X = [] # البيانات (الحركات)
    y = [] # أسماء الكلمات
    
    for file in os.listdir(UNITY_STREAMING_ASSETS):
        if file.endswith(".mp4"):
            word_name = file.replace(".mp4", "")
            video_path = os.path.join(UNITY_STREAMING_ASSETS, file)
            
            print(f"  [→] جاري معالجة وتعلم كلمة: '{word_name}' ...")
            sequences = extract_landmarks_from_video(video_path)
            
            if sequences:
                # نأخذ متوسط الحركات أو نلخصها كبصمة لهذه الكلمة
                mean_sequence = np.mean(sequences, axis=0)
                X.append(mean_sequence)
                y.append(word_name)
                print(f"  [✓] تم تعلم '{word_name}' بنجاح.")

    if X and y:
        # حفظ النموذج المدرب في ملف pkl المعتمد لديك
        model_data = {"data": X, "labels": y}
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"\n[🎉] تم حفظ نموذج الكلمات المدرب بنجاح في المسار:\n{MODEL_PATH}")
    else:
        print("\n[!] لم يتم استخراج أي بيانات كافية من الفيديوهات.")

if __name__ == "__main__":
    train_model_from_streaming_assets()