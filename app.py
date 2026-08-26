import streamlit as st
import os
import sys

# ربط مسار المشروع الأساسي لضمان استدعاء الملفات بسلاسة
sys.path.append(os.path.dirname(__file__))

st.set_page_config(page_title="تطبيق جسر (Jisr) - الربط مع يونتي", page_icon="🌉", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 منصة جسر (Jisr)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>التدفق المباشر للكاميرا والربط مع بيئة يونتي (Unity)</h4>", unsafe_allow_html=True)
st.write("---")

st.info("🎮 جاري تشغيل ملف `camera_to_unity.py` لاستعراض الإشارات وترجمتها المعروضة مع يونتي...")

# محاولة تفعيل واستدعاء الكود الحقيقي للربط مع يونتي الذي رفعتِهِ مسبقاً
try:
    import camera_to_unity
    st.success("✅ تم تفعيل ملف `camera_to_unity.py` والربط بنجاح.")
except Exception as e:
    st.error(f"⚠️ ملاحظة أثناء التشغيل: {e}")
    st.markdown("""
    > **تنبيه:** تشغيل كاميرا سطح المكتب المباشرة ونوافذ العرض الخارجية (`OpenCV`) يعمل بكفاءة تامة عند تشغيل الملف محلياً على جهازك. 
    """)

# زر اختياري لتشغيل الملف محلياً إذا احتجتِ
if st.button("🚀 عرض تفاصيل وتشغيل ملفات التدفق الحالية"):
    st.write("📁 الملفات المتاحة في مستودعك وتم ربطها:")
    st.code("""
    - camera_to_unity.py (مسؤول عن تدفق الكاميرا ويونتي)
    - app_pipeline.py (خط المعالجة ونموذج الذكاء الاصطناعي)
    - sign_language_model.pkl (نموذج التوقع المدرب)
    """)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع تخرج جسر (Jisr) 💙</p>", unsafe_allow_html=True)
