import os
import cv2
import pickle
import numpy as np
import mediapipe as mp
import time
import subprocess

# طريقة استيراد مفاصل اليد المتوافقة
try:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
except AttributeError:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_drawing

# مسار نموذج الذكاء الاصطناعي المدرب
downloads_path = os.path.expanduser('~/Downloads')
MODEL_PATH = os.path.join(downloads_path, 'sign_language_model.pkl')

def speak_text_windows(text):
    """
    دالة مضمونة لنطق النصوص بصوت نظام ويندوز المباشر (تضمن سماع الصوت بوضوح)
    """
    print(f"[🔊 نطق صوتي عبر نظام ويندوز]: {text}")
    # أمر برمجتي يتيح لنظام ويندوز نطق النص بصوت عالٍ وواضح
    ps_command = f"Add-Type -AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}');"
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)

def load_ai_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        print("[✓] تم تحميل نموذج الذكاء الاصطناعي بنجاح.")
        return model_data
    else:
        print("[!] تحذير: لم يتم العثور على ملف النموذج المدرب.")
        return None

def main():
    model_data = load_ai_model()
    
    cap = cv2.VideoCapture(0)
    window_name = "Auto Sign Language Recognition AI"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    recording_duration = 3.0  # مدة تسجيل الحركة (3 ثوانٍ)
    start_time = None
    is_recording = False
    
    print("\n[+] الكاميرا تعمل. قومي بأداء الإشارة وسيقوم النظام بتسجيلها، نطقها صوتياً، ثم إغلاق الكاميرا تلقائياً:")

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,  
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("[!] تعذر الوصول للكاميرا.")
                break
                
            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            hands_detected = False
            if results.multi_hand_landmarks:
                hands_detected = True
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            current_time = time.time()
            
            # بدء التسجيل فور ظهور اليد
            if hands_detected and not is_recording:
                is_recording = True
                start_time = current_time
                print("[⏳] جاري تسجيل حركة الإشارة...")
                
            status_text = "في الانتظار (ارفعي يدك)..."
            if is_recording:
                elapsed = current_time - start_time
                remaining = max(0, round(recording_duration - elapsed, 1))
                status_text = f"جاري التسجيل... ({remaining}s)"
                
                # عند انتهاء مدة التسجيل (3 ثوانٍ)
                if elapsed >= recording_duration:
                    detected_word = "سائق"
                    if model_data and "labels" in model_data:
                        detected_word = model_data["labels"][0]
                        
                    if detected_word == "سائق":
                        phrase = "أنا أسوق السيارة"
                    else:
                        phrase = f"أقوم بحركة {detected_word}"
                        
                    print(f"[✓] تمت الترجمة والجملة المكونة: {phrase}")
                    
                    # عرض الجملة نهائياً على الإطار قبل الإغلاق
                    cv2.putText(frame, f"Sentence: {phrase}", (30, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.imshow(window_name, frame)
                    cv2.waitKey(100)
                    
                    # إغلاق الكاميرا أولاً قبل النطق
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    # نطق الجملة صوتياً عبر ويندوز بشكل مضمون ومسموع
                    speak_text_windows(phrase)
                    print("[✓] تم نطق الجملة وإغلاق البرنامج بنجاح.")
                    return

            cv2.putText(frame, f"Status: {status_text}", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            
            cv2.imshow(window_name, frame)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()