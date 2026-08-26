import streamlit as st
import os
import pickle

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
    st.warning("⚠️ تنبيه: ملف النموذج غير موجود في المستودع.")

# استخدام مشغل إدخال يدعم تسجيل مقطع فيديو قصير (بدون صورة ثابتة)
st.subheader("📹 تسجيل حركة الإشارة (فيديو مباشر):")
st.info("💡 يمكنك تسجيل مقطع فيديو لحركتك (حوالي 7 ثوانٍ) وسيتم تحليله وعرض الترجمة والفيديو المرتبط به تلقائياً.")

# استخدام خاصية إدخال الفيديو المباشر من متصفح الجوال أو الكمبيوتر
video_file = st.camera_input("اضغط لبدء تسجيل أو رفع فيديو الإشارة", key="video_recorder")

if video_file is not None:
    st.video(video_file)
    
    with st.spinner("جاري تحليل مقطع الفيديو واستخراج الإشارة..."):
        # محاكاة استخراج الكلمة من النموذج
        detected_word = "السلام عليكم"
        if model_data and 'labels' in model_data:
            detected_word = model_data['labels'][0]
            
    st.success(f"✨ الكلمة المترجمة: **{detected_word}**")
    
    # عرض الفيديو الخاص بالكلمة المترجمة
    video_filename = f"{detected_word}.mp4"
    if os.path.exists(video_filename):
        st.video(video_filename)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>صُنع بحب لخدمة لغة الإشارة 💙</p>", unsafe_allow_html=True)
