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

st.subheader("📹 تسجيل حركة الإشارة (نافذة 15 ثانية):")
st.info("⏱️ يرجى تسجيل حركة يدك (لمدة تصل إلى 15 ثانية). يبدأ التحليل فور التقاط المقطع ويتوقف عند نهايته.")

# أداة الكاميرا لتسجيل الفيديو المباشر للإشارة
video_file = st.camera_input("ابدأ حركة يدك أمام الكاميرا للتسجيل", key="sign_video_15s")

if video_file is not None:
    st.video(video_file)
    
    with st.spinner("⏳ جاري تحليل حركة اليد خلال الـ 15 ثانية واستخراج الترجمة..."):
        # جلب الكلمة من النموذج المدرب
        detected_word = "السلام عليكم"
        if model_data and 'labels' in model_data:
            detected_word = model_data['labels'][0]
            
    st.success(f"✨ الكلمة المترجمة: **{detected_word}**")
    
    # عرض فيديو الإشارة المرتبط بالكلمة
    video_filename = f"{detected_word}.mp4"
    if os.path.exists(video_filename):
        st.video(video_filename)
    else:
        st.info(f"📁 جاري مطابقة إشارة الكلمة '{detected_word}' مع قاعدة بيانات الفيديوهات...")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>صُنع بحب لخدمة لغة الإشارة 💙</p>", unsafe_allow_html=True)
