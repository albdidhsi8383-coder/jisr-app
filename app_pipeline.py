import os
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import cv2

# المسار الصحيح للمجلد الذي يحتوي على الفيديوهات
UNITY_STREAMING_ASSETS = r"C:\Users\Asmaaalfalahi\Downloads\StreamingAssets"

# قائمة الكلمات الزائدة والضمائر التي يتم تخطيها
FILLER_WORDS = {"انا", "انت", "أنتم", "هو", "هي", "نحن", "في", "على", "من", "إلى", "عن", "مع", "هذا", "هذه", "الذي", "التي"}

# قاموس تقريب وتحويل الكلمات (Mapping) إلى الكلمات المتوفرة في المجلد لديك
# يمكنك تعديل أو إضافة الكلمات هنا حسب ما هو موجود لديك في مجلد StreamingAssets
SYNONYMS_MAPPING = {
    "اسوق": "سائق",
    "أسوق": "سائق",
    "سياره": "سائق",
    "السياره": "سائق",
    "أذهب": "يمشي",
    "اذهب": "يمشي",
    "أقرا": "يقرأ",
    "اقرا": "يقرأ"
}

def clean_and_map_words(text):
    """
    تصفية الكلمات، إزالة الحشو، وتحويلها إلى الكلمات المقابلة المتوفرة في المجلد
    """
    words = text.split()
    gloss_words = []
    
    for word in words:
        clean = word.strip()
        
        # تخطي كلمات الحشو والضمائر
        if clean in FILLER_WORDS:
            print(f"  [i] تخطي كلمة حشو/ضمير: '{clean}'")
            continue
            
        # إزالة "الـ" التعريف إن وجدت
        if clean.startswith("ال") and len(clean) > 3:
            clean_no_al = clean[2:]
        else:
            clean_no_al = clean
            
        # فحص القاموس هل لها كلمة قريبة/مرادفة
        if clean in SYNONYMS_MAPPING:
            mapped = SYNONYMS_MAPPING[clean]
            print(f"  [~] تحويل '{clean}' إلى المرادف المتاح: '{mapped}'")
            gloss_words.append(mapped)
        elif clean_no_al in SYNONYMS_MAPPING:
            mapped = SYNONYMS_MAPPING[clean_no_al]
            print(f"  [~] تحويل '{clean}' إلى المرادف المتاح: '{mapped}'")
            gloss_words.append(mapped)
        else:
            # إذا لم تكن في القاموس، نستخدم الكلمة بعد تنظيفها
            gloss_words.append(clean_no_al)
            
    return gloss_words

def record_audio_and_convert(duration=7, sample_rate=44100):
    print(f"\n[+] جاري الاستماع لمدة {duration} ثوانٍ... تحدثي الآن بوضوح:")
    
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    
    temp_wav = "temp_speech.wav"
    write(temp_wav, sample_rate, recording)
    
    recognizer = sr.Recognizer()
    gloss_words = []
    
    try:
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio, language="ar-SA")
        print(f"[✓] النص المنطوق (الأصلي): {text}")
        
        gloss_words = clean_and_map_words(text)
        print(f"[✓] كلمات الإشارة بعد المطابقة والتقريب: {gloss_words}")
        
    except sr.UnknownValueError:
        print("[!] لم يتم التعرف على الصوت بوضوح. تأكدي من قرب الميكروفون وحاولي مرة أخرى.")
    except Exception as e:
        print(f"[!] خطأ في التعرف على الصوت: {e}")
    finally:
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception:
                pass

    return gloss_words

def play_connected_videos(video_paths):
    """
    تشغيل الفيديوهات متسلسلة وراء بعضها بحجم متوسط وواضح
    """
    if not video_paths:
        return

    print("\n--- جاري عرض فيديوهات لغة الإشارة للجملة متسلسلة ---")
    
    # إنشاء نافذة قابلة لتعديل الحجم وتحديد حجم متوسط افتراضي (مثلاً 800×600)
    window_name = "Sign Language Gloss Player"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    for v_path in video_paths:
        if not os.path.exists(v_path):
            continue
            
        cap = cv2.VideoCapture(v_path)
        word_name = os.path.basename(v_path).replace(".mp4", "")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # (اختياري) يمكنك تصغير أو تكبير الإطار برمجياً بدقة إذا احتجت، 
            # ولكن cv2.resizeWindow ستضبط النافذة بالحجم المتوسط المطلوب (800x600)
            
            # كتابة اسم الكلمة على الشاشة بخط واضح
            cv2.putText(frame, f"Sign: {word_name}", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow(window_name, frame)
            
            # اضغط على زر 'q' للخروج المبكر أثناء العرض
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        cap.release()
        
    cv2.destroyAllWindows()
    print("تم الانتهاء من عرض جملة الإشارة بنجاح.")

def process_pipeline():
    gloss_words = record_audio_and_convert(duration=7)
    
    if not gloss_words:
        return

    matched_videos = []

    print("\n[→] جاري البحث عن فيديوهات الكلمات المطابقة في المجلد...")
    for word in gloss_words:
        video_path = os.path.join(UNITY_STREAMING_ASSETS, f"{word}.mp4")

        if os.path.exists(video_path):
            print(  f"[✓] متوفر: '{word}'")
            matched_videos.append(video_path)
        else:
            print(  f"[✗] غير متوفر: '{word}' (لا يوجد فيديو بهذا الاسم في StreamingAssets)")

    if matched_videos:
        play_connected_videos(matched_videos)
    else:
        print("\n[!] لم يتم العثور على أي فيديو مطابق. تأكدي من إضافة المرادفات في القاموس حسب الكلمات المتوفرة لديك.")

if __name__ == "__main__":
    process_pipeline()