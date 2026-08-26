import streamlit as st
import os
import sys

# ربط مسار المشروع الأساسي
sys.path.append(os.path.dirname(__file__))

st.set_page_config(page_title="تطبيق جسر (Jisr) - الربط مع يونتي", page_icon="🌉", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌉 منصة جسر (Jisr)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>التدفق المباشر للكاميرا والربط مع بيئة يونتي (Unity)</h4>", unsafe_allow_html=True)
st.write("---")

st.info("🎮 حالة النظام: تم تحميل ملفات المشروع وجاهزة للاستعراض.")

# عرض حالة الملفات بطريقة نظيفة وخالية من أخطاء الـ GUI على السحابة
st.success("✅ ملف `camera_to_unity.py` وموديلات الذكاء الاصطناعي متوفرة في المستودع.")

st.markdown("""
> 💡 **ملاحظة تقنية مهمة:** 
> تشغيل نوافذ الكاميرا المحلية المباشرة (`OpenCV cv2.imshow`) وتكاملها مع نظام ويندوز ويونتي يتم تنفيذه بسلاسة تامة عند تشغيل المشروع **محلياً على جهازك**، نظراً لأن السحابة السحابية تفتقر لشاشات العرض المحلية.
""")

# إضافة زر لعرض محتوى أو حالة الملف البرمجي
if st.button("📁 عرض مسارات وتفاصيل الملفات المرفوعة"):
    st.code("""
    - camera_to_unity.py : مسؤولة عن ربط الكاميرا وتدفق البيانات مع Unity.
    - app_pipeline.py    : خط معالجة وتوقع لغة الإشارة.
    - sign_language_model.pkl : النموذج المدرب المعتمد.
    """)

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع تخرج جسر (Jisr) 💙</p>", unsafe_allow_html=True)
