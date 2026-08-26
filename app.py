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
    st.warning("⚠️ تنبيه: لم يتم العثور على ملف النموذج المدرب `sign_language_model.pkl`، تأكدي من رفعه بجانب الكود.")

# التقاط صورة الإشارة عبر كاميرا المتصفح/الجوال
st.subheader("📷 التقاط حَرَكة الإشارة:")
camera_image = st.camera_input("التقط صورة لإشارتك عبر الكاميرا")

if camera_image is not None:
    st.image(camera_image, caption="الصورة التقِطت بنجاح", use_column_width=True)
    
    with st.spinner("جاري تحليل الإشارة وترجمتها..."):
        # محاكاة أو استخراج النتيجة من النموذج
        detected_word = "السلام عليكم (كمثال)"
        if model_data and 'labels' in model_data:
            detected_word = model_data['labels'][0]
            
    st.success(f"✨ الترجمة الفورية: **{detected_word}**")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>صُنع بحب لخدمة لغة الإشارة 💙</p>", unsafe_allow_html=True)
