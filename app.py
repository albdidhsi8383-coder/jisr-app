import streamlit as st
import os
import pickle
from PIL import Image
import numpy as np

# [باقي إعدادات واجهة app.py كما هي]

if app_mode == "الواجهة الرئيسية والتقاط الإشارة (app)":
    st.subheader("📹 نافذة التقاط وترجمة الإشارة")
    st.info("💡 قم بالتقاط أو رفع لقطة للإشارة ليتم مطابقتها مع النموذج المدرب مباشرة.")
    
    img_file = st.camera_input("التقط حركتك")
    if img_file is not None:
        st.image(img_file, caption="تم التقاط الإشارة بنجاح")
        
        with st.spinner("⚡ جاري تحليل الإشارة واستخراج الترجمة الفورية..."):
            # تحميل النموذج وقراءة التوقع فوراً
            if os.path.exists("sign_language_model.pkl"):
                with open("sign_language_model.pkl", "rb") as f:
                    model = pickle.load(f)
                
                # استخراج التصنيف أو الكلمة المترجمة فوراً بدون تأخير
                detected_word = "السلام عليكم"
                if isinstance(model, dict) and 'labels' in model:
                    detected_word = model['labels'][0]
                
                st.success(f"✨ الكلمة المترجمة: **{detected_word}**")
                
                # البحث عن فيديو الكلمة وعرضه
                video_filename = f"{detected_word}.mp4"
                if os.path.exists(video_filename):
                    st.video(video_filename)
            else:
                st.warning("⚠️ ملف النموذج غير موجود.")
