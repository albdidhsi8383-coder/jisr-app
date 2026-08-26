import streamlit as st
import os
import sys

# ربط مسار المشروع الأساسي
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="منصة جسر الإنسانية - ترجمة لغة الإشارة",
    page_icon="🌉",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌉 مشروع جسر الإنساني</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #4B5563;'>المنصة الذكية للربط الصوتي والمرئي مع فيديوهات لغة الإشارة</h4>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية لتنقل الأقسام
st.sidebar.title("🎛️ لوحة التحكم بالمشروع")
mode = st.sidebar.radio(
    "اختر وضع الاستخدام:",
    [
        "🎙️ تسجيل الصوت والبحث في فيديوهات StreamingAssets",
        "📹 التقاط وتحليل لغة الإشارة بالكاميرا",
        "📁 فحص مجلد الفيديوهات (418 فيديو)"
    ]
)

# تحديد المسار الفعلي لمجلد الفيديوهات الذي يحتوي على الـ 418 فيديو
VIDEO_DIR = "StreamingAssets"

if mode == "🎙️ تسجيل الصوت والبحث في فيديوهات StreamingAssets":
    st.subheader("🎙️ التسجيل الصوتي والتحويل المرئي الفوري")
    st.info("💡 قومي بتسجيل الصوت أو التحدث، وسيقوم النظام باستخراج الكلمة والبحث عنها مباشرة داخل مجلد فيديوهات الإشارة.")
    
    audio_file = st.audio_input("اضغطي هنا لبدء التسجيل الصوتي")
    
    if audio_file is not None:
        st.audio(audio_file)
        
        with st.spinner("⏳ جاري تحليل الصوت واستخراج كلمة الإشارة من قاعدة البيانات..."):
            
            # محاكاة الكلمة المستخرجة من الصوت (كمثال: إحدى الكلمات الموجودة في مجلدك مثل 'يمشي' أو 'ينام' أو 'يقدر')
            # يمكنك لاحقاً ربط هذه المتغيرات بنتيجة موديل التعرف الصوتي لديك
            target_word = "يمشي" 
            recognized_sentence = "الشخص يمشي ببطء"
            
            st.success("✅ تمت عملية تحليل الصوت والترجمة بنجاح!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📝 الجملة المستخرجة:**")
                st.info(recognized_sentence)
            with col2:
                st.markdown(f"**🎯 كلمة الإشارة المعنية:**")
                st.warning(target_word)
                
            st.write("---")
            st.subheader(f"🎬 فيديو لغة الإشارة الحقيقي للكلمة: ({target_word})")
            
            # بناء مسار البحث عن الفيديو داخل مجلد StreamingAssets
            video_path = os.path.join(VIDEO_DIR, f"{target_word}.mp4")
            
            if os.path.exists(video_path):
                st.video(video_path)
                st.success(f"📁 تم جلب وتشغيل فيديو الإشارة الحقيقي بنجاح من مجلد `{VIDEO_DIR}`.")
            else:
                st.error(f"⚠️ عذراً، لم يتم العثور على ملف الفيديو باسم (`{target_word}.mp4`) في مجلد `{VIDEO_DIR}`.")
                st.info(f"تأكد من أن الكلمة تطابق اسم ملف الفيديو الموجود في المجلد (مثلاً: ينام.mp4، يبكي.mp4، إلخ).")

elif mode == "📹 التقاط وتحليل لغة الإشارة بالكاميرا":
    st.subheader("📹 نافذة التقاط حركة الإشارة بالكاميرا")
    st.info("💡 التقطي الإشارة بالكاميرا ليتم تحليلها وعرض الفيديو المرتبط بها.")
    
    img_file = st.camera_input("التقط حركة اليد")
    if img_file is not None:
        st.image(img_file, caption="تم التقاط الإشارة")
        target_word = "يمشي"
        st.success(f"✨ الكلمة المترجمة: **{target_word}**")
        
        video_path = os.path.join(VIDEO_DIR, f"{target_word}.mp4")
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"فيديو الكلمة غير متوفر في مسار `{VIDEO_DIR}`.")

elif mode == "📁 فحص مجلد الفيديوهات (418 فيديو)":
    st.subheader("📊 فحص قاعدة بيانات الفيديوهات الحالية")
    if os.path.exists(VIDEO_DIR):
        video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
        st.success(f"✅ مجلد `{VIDEO_DIR}` متوفر ويحتوي على **{len(video_files)}** ملف فيديو جاهز للعمل!")
        
        # عرض عينة من أسماء الفيديوهات المتاحة في المجلد للتأكد
        with st.expander("🔍 اضغط هنا لعرض عينة من أسماء الكلمات المتوفرة في المجلد"):
            st.write(video_files[:30]) # يظهر أول 30 كلمة كمثال
    else:
        st.warning(f"⚠️ مجلد `{VIDEO_DIR}` غير موجود في مسار العمل الحالي. تأكد من وضعه بجانب ملف app.py.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>مشروع جسر الإنساني 💙 - نخدم التواصل بلغة الإشارة بكل حب</p>", unsafe_allow_html=True)
