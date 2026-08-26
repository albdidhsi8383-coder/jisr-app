import subprocess
import sys

# تثبيت المكتبات المطلوبة تلقائياً إذا لم تكن موجودة
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import cv2
except ImportError:
    install("opencv-python-headless")
    import cv2

try:
    import mediapipe as mp
except ImportError:
    install("mediapipe")
    import mediapipe as mp

try:
    import streamlit_webrtc
except ImportError:
    install("streamlit-webrtc")
    import streamlit_webrtc

import streamlit as st
import numpy as np
import os
import pickle
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# إعدادات صفحة التطبيق
st.set_page_config(page_title="تطبيق جسر (Jisr) - الترجمة الفورية", page_icon="🌉", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 تطبيق جسر (Jisr)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>المنصة الذكية للترجمة الفورية للغة الإشارة</h4>", unsafe_allow_html=True)
st.write("---")

# مسار نموذج الذكاء الاصطناعي
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
    st.warning("⚠️ تنبيه: لم يتم العثور على ملف النموذج المدرب `sign_language_model.pkl`، تأكدي من رفعه بجانب الكود.")

# إعدادات ميديابايپ لتتبع اليد
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
        img = cv2.flip(img, 1)
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        detected_text = "في انتظار الإشارة..."

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if model_data and 'labels' in model_data:
                    detected_text = model_data['labels'][0]

        cv2.putText(img, f"Translation: {detected_text}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return frame.from_ndarray(img, format="bgr24")

st.subheader("📹 بث مباشر لتتبع اليد وترجمة الإشارة:")
webrtc_streamer(
    key="jisr-sign-language",
    video_processor_factory=SignLanguageProcessor,
    media_stream_constraints={"video": True, "audio": False}
)
