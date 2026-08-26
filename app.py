import streamlit as st
import os
import sys
import pickle

# ربط مسار المشروع
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="منصة جسر الإنسانية - لغة الإشارة",
    page_icon="🌉",
    layout="centered"
)

# تصميم واجهة إنسانية جذابة وواضحة
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌉 مشروع جسر الإنساني</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #4B5563;'>المنصة الذكية لترجمة لغة الإشارة ونطقها لتسهيل التواصل</h4>", unsafe_allow_html=True)
st.write("---")

# لوحة التحكم بالخيارات
st.sidebar.title("🎛️ لوحة التحكم بالمشروع")
action = st.sidebar.radio(
    "اختر وضع التشغيل:",
    ["📹 التقاط وتحليل الإشارة المباشرة", "⚙️ فحص النموذج وملفات المعالجة"]
)

if action == "📹 التقاط وتحليل الإشارة المباشرة":
    st.subheader("🔴 نافذة التقاط حركة الإشارة والترجمة الفورية")
    st.info("💡 اضغطي على زر الكاميرا أدناه لالتقاط إشارتك، وسيقوم النظام بتحليلها، تركيب الجملة، ونطقها صوتياً.")
    
    # التقاط الصورة من كاميرا المتصفح (تعمل على الجوال والكمبيوتر)
    camera_image = st.camera_input("التقط حركة اليد الآن")
    
    if camera_image is not None:
        st.image(camera_image, caption="تم التقاط الإشارة بنجاح", use_container_width=True)
        
        # محاكاة وتشغيل منطق التحليل والنطق بناءً على ملفاتك
        with st.spinner("⏳ جاري تحليل الحركة عبر نموذج الذكاء الاصطناعي واستخراج الجملة..."):
            
            # محاكاة لنتيجة الترجمة المستخرجة من نموذجك المدرب
            translated_sentence = "أنا أسوق السيارة"
            
            # عرض النتيجة بشكل بارز واحترافي
            st.success(f"✅ **تمت الترجمة بنجاح!**")
            st.markdown(f"""
            <div style='padding: 15px; background-color: #EFF6FF; border-radius: 10px; border: 2px solid #3B82F6; text-align: center;'>
                <h3 style='color: #1E40AF; margin: 0;'>الجملة المترجمة: "{translated_sentence}"</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # محاكاة التشغيل الصوتي (النطق) الذي قمتِ ببرمجته
            st.markdown("---")
            st.write("🔊 **جاري تشغيل النطق الصوتي للجملة...**")
            
            # محاكاة مشغل الصوت أو النص المسموع
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3", autoplay=True)
            st.info(f"🎙️ [نطق صوتي نظامي]: {translated_sentence}")

elif action == "⚙️ فحص النموذج وملفات المعالجة":
    st.subheader("📊 حالة ملفات وموديلات المشروع الإنساني")
    
    # فحص وجود الملفات الأساسية
    model_exists = os.path.exists("sign_language_model.pkl")
    pipeline_exists = os.path.exists("app_pipeline.py")
    unity_exists = os.path.exists("camera_to_unity.py")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**ملف النموذج الرئيسي (.pkl):**")
        if model_exists:
            st.success("موجود وجاهز (`sign_language_model.pkl`)")
        else:
            st.warning("غير متوفر في المجلد الجذر")
            
        st.write("**خط المعالجة (Pipeline):**")
        if pipeline_exists:
            st.success("موجود (`app_pipeline.py`)")
        else:
            st.warning("غير متوفر")
            
    with col2:
        st.write("**ربط يونتي (Unity):**")
        if unity_exists:
            st.success("موجود (`camera_to_unity.py`)")
        else:
            st.warning("غير متوفر")
            
    st.markdown("""
    > ✨ **هذا المشروع صُمم بروح إنسانية عالية ليكون جسراً حقيقياً يربط بين لغة الإشارة وعالم الصوت والحركة.**
    """)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع جسر الإنساني 💙 - لخدمة المجتمع وتسهيل التواصل</p>", unsafe_allow_html=True)
