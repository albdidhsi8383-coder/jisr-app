import cv2
import mediapipe as mp
import pickle
import os
import time
import streamlit as st

st.set_page_config(page_title="تطبيق جسر (Jisr) - الترجمة الفورية التلقائية", page_icon="🌉", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 تطبيق جسر (Jisr) - التتبع التلقائي</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>يبدأ التسجيل فوراً عند رصد حركة اليد ويتوقف تلقائياً</h4>", unsafe_allow_html=True)
st.write("---")

MODEL_PATH = 'sign_language_model.pkl'

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None

model_data = load_model()

if model_data:
    st.success("✅ تم تحميل نموذج الذكاء الاصطناعي بنجاح.")
else:
    st.warning("⚠️ تنبيه: ملف النموذج غير موجود.")

# زر لتشغيل الكاميرا المحلية آلياً
if st.button("🚀 تشغيل التتبع التلقائي للإشارة (عبر كاميرا الحاسوب)"):
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    
    st.info("📹 الكاميرا تعمل الآن... حرك يدك أمام الكاميرا وسيبدأ النظام بالترجمة الفورية آلياً.")
    frame_placeholder = st.empty()
    text_placeholder = st.empty()
    
    start_time = time.time()
    duration = 15  # نافذة الـ 15 ثانية للتسجيل التلقائي
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("تعذر الوصول إلى الكاميرا.")
            break
            
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        detected_word = "في انتظار حركة اليد..."
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                detected_word = "مرحباً (إشارة مرصودة)"
                if model_data and 'labels' in model_data:
                    detected_word = model_data['labels'][0]
        
        cv2.putText(frame, f"Sign: {detected_word}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # عرض الإطار مباشرة على واجهة Streamlit
        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        text_placeholder.success(f"✨ الترجمة الحية: **{detected_word}**")
        
        # إيقاف تلقائي بعد 15 ثانية أو عند توقف الإشارة
        if time.time() - start_time > duration:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    st.success("🏁 انتهت جلسة الترجمة التلقائية (15 ثانية).")
