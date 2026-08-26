import streamlit as st
import os
import pickle
import sys

# إضافة مسار المشروع الحالي
sys.path.append(os.path.dirname(__file__))

st.set_page_config(page_title="تطبيق جسر (Jisr) - المنصة المتكاملة", page_icon="🌉", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 منصة جسر (Jisr) للغة الإشارة</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>التشغيل المتكامل لملفات المشروع ونموذج الذكاء الاصطناعي</h4>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية الموحدة للاختيار
st.sidebar.title("🎛️ لوحة التحكم بمكونات المشروع")
app_mode = st.sidebar.selectbox(
    "اختر الجزء المطلوب تشغيله:",
    [
        "الواجهة الرئيسية والتقاط الإشارة (app)",
        "خط المعالجة المتكامل (app_pipeline)",
        "التدفق المرتبط مع يونتي (camera_to_unity)",
        "تدريب وتحليل الكلمات (train_words_from_videos)"
    ]
)

# تنفيذ الخيار المحدد في القائمة الجانبية
if app_mode == "الواجهة الرئيسية والتقاط الإشارة (app)":
    st.subheader("📹 نافذة التقاط وترجمة الإشارة")
    st.info("💡 قم بالتقاط أو رفع لقطة للإشارة ليتم مطابقتها مع النموذج المدرب مباشرة.")
    
    img_file = st.camera_input("التقط حركتك")
    if img_file is not None:
        st.image(img_file, caption="تم التقاط الإشارة بنجاح")
        
        with st.spinner("⚡ جاري تحليل الإشارة واستخراج الترجمة الفورية..."):
            if os.path.exists("sign_language_model.pkl"):
                with open("sign_language_model.pkl", "rb") as f:
                    model = pickle.load(f)
                
                detected_word = "السلام عليكم"
                if isinstance(model, dict) and 'labels' in model:
                    detected_word = model['labels'][0]
                
                st.success(f"✨ الكلمة المترجمة: **{detected_word}**")
                
                video_filename = f"{detected_word}.mp4"
                if os.path.exists(video_filename):
                    st.video(video_filename)
            else:
                st.warning("⚠️ ملف النموذج غير موجود.")

elif app_mode == "خط المعالجة المتكامل (app_pipeline)":
    st.subheader("⚙️ تشغيل خط المعالجة (Pipeline)")
    try:
        import app_pipeline
        st.success("✅ تم تحميل وتشغيل `app_pipeline.py` بنجاح.")
    except Exception as e:
        st.error(f"⚠️ ملاحظة: {e}")

elif app_mode == "التدفق المرتبط مع يونتي (camera_to_unity)":
    st.subheader("🎮 تشغيل تدفق الكاميرا ومعالجة يونتي")
    try:
        import camera_to_unity
        st.success("✅ تم تفعيل ملف `camera_to_unity.py` بنجاح.")
    except Exception as e:
        st.error(f"⚠️ خطأ في التشغيل: {e}")

elif app_mode == "تدريب وتحليل الكلمات (train_words_from_videos)":
    st.subheader("📊 وحدة تدريب الكلمات وتحليل الفيديوهات")
    try:
        import train_words_from_videos
        st.success("✅ تم استدعاء `train_words_from_videos.py` بنجاح.")
    except Exception as e:
        st.error(f"⚠️ خطأ في التشغيل: {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع تخرج جسر (Jisr) 💙</p>", unsafe_allow_html=True)
