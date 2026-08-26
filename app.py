import streamlit as st
import os
import sys

# ربط مسار المشروع الأساسي
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="منصة جسر الإنسانية - الترجمة الشاملة",
    page_icon="🌉",
    layout="centered"
)

# تصميم الواجهة الإنسانية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌉 مشروع جسر الإنساني</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #4B5563;'>المنصة الذكية لتحويل الصوت إلى إشارات وفيديوهات توضيحية</h4>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية لتنقل الأقسام
st.sidebar.title("🎛️ لوحة التحكم بالمشروع")
mode = st.sidebar.radio(
    "اختر وضع الاستخدام:",
    [
        "🎙️ تسجيل الصوت وتحويله إلى إشارة وفيديو",
        "📹 التقاط وتحليل لغة الإشارة بالكاميرا",
        "⚙️ فحص حالة ملفات المشروع"
    ]
)

if mode == "🎙️ تسجيل الصوت وتحويله إلى إشارة وفيديو":
    st.subheader("🎙️ التسجيل الصوتي والتحويل الذكي")
    st.info("💡 قومي بتسجيل الصوت (أو النطق بالجملة)، وسيقوم النظام بتحليله، استخراج الكلمة الإشارية، وعرض الفيديو المرتبط بها مباشرة.")
    
    # محاكاة خانة تسجيل الصوت المباشر في المتصفح
    audio_file = st.audio_input("اضغطي هنا لبدء التحدث أو تسجيل الصوت")
    
    if audio_file is not None:
        st.audio(audio_file)
        
        with st.spinner("⏳ جاري تحليل الصوت، تحويله إلى جملة، واستخراج فيديو الإشارة..."):
            
            # محاكاة النص المستخرج من الصوت
            recognized_sentence = "أنا أسوق السيارة"
            target_word = "سيارة" # الكلمة المستهدفة للإشارة
            
            # عرض النتائج بطريقة إنسانية واضحة
            st.success("✅ تمت عملية تحليل الصوت والترجمة بنجاح!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📝 الجملة المستخرجة:**")
                st.info(recognized_sentence)
            with col2:
                st.markdown(f"**🎯 كلمة الإشارة المعنية:**")
                st.warning(target_word)
                
            st.write("---")
            st.subheader(f"🎬 فيديو لغة الإشارة للكلمة: ({target_word})")
            
            # محاكاة تشغيل ملف الفيديو الخاص بالإشارة
            video_filename = f"{target_word}.mp4"
            if os.path.exists(video_filename):
                st.video(video_filename)
            else:
                # عرض فيديو تجريبي أو إرشادي في حال لم يكن الملف مرفوعاً بعد
                st.info("📽️ (عرض توضيحي لفيديو الإشارة الخاص بالكلمة المرعضة)")
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

elif mode == "📹 التقاط وتحليل لغة الإشارة بالكاميرا":
    st.subheader("📹 نافذة التقاط حركة الإشارة")
    st.info("💡 التقطي الإشارة بالكاميرا ليتم مطابقتها مع النموذج وترجمتها إلى نص وصوت.")
    
    img_file = st.camera_input("التقط حركة اليد")
    if img_file is not None:
        st.image(img_file, caption="تم التقاط الإشارة")
        st.success("✨ الجملة المترجمة: **أنا أسوق السيارة**")
        st.write("🔊 [نطق صوتي]: أنا أسوق السيارة")

elif mode == "⚙️ فحص حالة ملفات المشروع":
    st.subheader("📊 فحص ملفات الموديل والمعالجة")
    st.write(f"- ملف النموذج الرئيسي: `{'متوفر ✅' if os.path.exists('sign_language_model.pkl') else 'غير متوفر ⚠️'}`")
    st.write(f"- خط المعالجة: `{'متوفر ✅' if os.path.exists('app_pipeline.py') else 'غير متوفر ⚠️'}`")
    st.write(f"- ربط يونتي: `{'متوفر ✅' if os.path.exists('camera_to_unity.py') else 'غير متوفر ⚠️'}`")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع جسر الإنساني 💙 - نخدم التواصل بلغة الإشارة</p>", unsafe_allow_html=True)
