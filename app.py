import streamlit as st
import os
import pickle
import numpy as np

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
    st.success("✅ تم تحميل نموذج الذكاء الاصطناعي وملفات الترجمة بنجاح.")
else:
    st.warning("⚠️ تنبيه: ملف النموذج (`sign_language_model.pkl`) غير موجود في المستودع، يرجى رفعه بجانب الكود.")

# واجهة التقاط الحركة أو الصورة لتحليلها وترجمتها وعرض الفيديو المرتبط
st.subheader("📹 التقاط حَرَكة الإشارة:")
camera_image = st.camera_input("التقط صورة أو لقطة لحركة إشارتك عبر الكاميرا")

if camera_image is not None:
    st.image(camera_image, caption="تم التقاط الإشارة بنجاح")
    
    with st.spinner("جاري تحليل الإشارة واستخراج الكلمة..."):
        # محاكاة الاستخراج أو قراءة الكلمة المترجمة من النموذج المدرب
        detected_word = "مرحباً"
        if model_data and 'labels' in model_data:
            detected_word = model_data['labels'][0]
            
    st.success(f"✨ الكلمة المترجمة: **{detected_word}**")
    
    # هنا يتم جلب الفيديو الخاص بالكلمة المترجمة (تأكدي من وجود مجلد الفيديوهات لديكِ أو مسارها)
    video_filename = f"{detected_word}.mp4"
    
    # محاكاة عرض فيديو الإشارة إذا كان متوفراً
    if os.path.exists(video_filename):
        st.video(video_filename)
    else:
        st.info(f"📁 جاري البحث عن ملف الفيديو الخاص بـ '{detected_word}' لعرضه...")
        # يمكنكِ وضع مسار فيديو افتراضي تجريبي للتأكد من عمل مشغل الفيديو
        # st.video("sample_sign.mp4")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>صُنع بحب لخدمة لغة الإشارة 💙</p>", unsafe_allow_html=True)
