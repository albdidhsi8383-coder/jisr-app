import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import os
import pickle
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# إعدادات صفحة التطبيق
st.set_page_config(page_title="تطبيق جسر (Jisr) - الترجمة الفورية", page_icon="🌉", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 تطبيق جسر (Jisr)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>المنصة الذكية للترجمة الفورية للغة الإشارة</h4>", unsafe_allow_html=True)
st.write("---")

# مسار نموذج الذكاء الاصطناعي (تأكدي أن اسم الملف مطابق لما رفعتيه على غيت هاب)
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
    st.warning("⚠️ تنبيه: لم يتم العثور على ملف النموذج المدرب، تأكدي من رفعه بجانب الكود في غيت هاب.")

# إعدادات ميديابايپ لتتبع اليد (نفس إعدادات مشروعك المحلي)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class SignLanguageProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # انعكاس الصورة لتعمل كمرآة
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        
        # تحويل الألوان لمعالجة Mediapipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        detected_text = "في انتظار الإشارة..."

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # رسم خطوط تتبع اليد على الفيديو الحي
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # هنا يمكنك استخراج الـ landmarks تماماً كما في كودك المحلي (integrated_app.py)
                # وإدخالها للنموذج للتنبؤ بالكلمة
                if model_data and 'labels' in model_data:
                    detected_text = model_data['labels'][0]  # استبدليها بالتنبؤ الفعلي من نموذجك

        # كتابة الكلمة المترجمة على الشاشة الحية للفيديو
        cv2.putText(img, f"Translation: {detected_text}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return frame.from_ndarray(img, format="bgr24")

# تشغيل البث الحي وتتبع اليد عبر المتصفح والهاتف
st.subheader("📹 بث مباشر لتتبع اليد وترجمة الإشارة:")
webrtc_streamer(
    key="jisr-sign-language",
    video_processor_factory=SignLanguageProcessor,
    media_stream_constraints={"video": True, "audio": False}
)
