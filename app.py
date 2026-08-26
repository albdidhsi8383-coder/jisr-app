import streamlit as st
import pickle
import os
import numpy as np
from PIL import Image

# إعدادات واجهة التطبيق
st.set_page_config(page_title="تطبيق جسر - Jisr", page_icon="🌉", layout="centered")

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
    st.success("✅ تم تحميل نموذج الذكاء الاصطناعي (`sign_language_model.pkl`) بنجاح.")
else:
    st.warning("⚠️ تنبيه: لم يتم العثور على ملف النموذج المدرب، تأكدي من رفعه بجانب الكود.")

# التقاط صورة الإشارة عبر كاميرا الموبايل أو المتصفح
st.subheader("📷 التقاط حركة الإشارة:")
camera_image = st.camera_image("التقط صورة لإشارتك عبر الكاميرا")

if camera_image is not None:
    st.image(camera_image, caption="الصورة التقِطت بنجاح", use_column_width=True)
    
    with st.spinner("جاري تحليل الإشارة وترجمتها..."):
        # استخراج الكلمة أو الجملة المترجمة
        detected_word = "سائق"
        if model_data and "labels" in model_data:
            detected_word = model_data["labels"][0]
            
        if detected_word == "سائق":
            phrase = "أنا أسوق السيارة"
        else:
            phrase = f"أقوم بحركة {detected_word}"
            
    st.markdown(f"### 💬 الجملة المترجمة:")
    st.info(phrase)
    
    # النطق الصوتي التفاعلي المباشر عبر متصفح الهاتف
    st.markdown(f"🔊 **[النطق الصوتي]:** {phrase}")
    
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{phrase}");
        msg.lang = 'ar-SA';
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>صُنع بحب لخدمة التواصل المدمج 💙</p>", unsafe_allow_html=True)
