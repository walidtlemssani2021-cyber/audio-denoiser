import streamlit as st
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import tempfile
import os

st.set_page_config(page_title="PDF Translator (OCR + Batch)", layout="wide")

st.title("📄 PDF Translator (OCR + Batch)")

# --- دالة OCR للصفحات الممسوحة ضوئياً ---
def ocr_page(image):
    """تحويل صورة الصفحة إلى نص باستخدام Tesseract."""
    # تحسين الصورة قبل OCR
    image = image.convert("L")  # Grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # زيادة التباين
    image = image.filter(ImageFilter.MedianFilter())  # إزالة الضوضاء
    image = image.filter(ImageFilter.SHARPEN)  # زيادة الحدة
    
    # OCR (يدعم لغات متعددة)
    text = pytesseract.image_to_string(image, lang='eng+ara')
    return text

# --- دالة الترجمة ---
def translate_text(text, target_lang='ar'):
    if not text.strip():
        return ""
    try:
        # تقسيم النص الطويل إلى أجزاء (لتجنب تجاوز الحد)
        max_chars = 4000
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        translated_chunks = []
        for chunk in chunks:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(chunk)
            translated_chunks.append(translated)
        return " ".join(translated_chunks)
    except Exception as e:
        return f"Error: {e}"

# --- رفع الملف ---
uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    # حفظ الملف مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    # فتح الملف
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    st.sidebar.write(f"عدد الصفحات: {total_pages}")

    # خيارات المستخدم
    target_lang = st.sidebar.selectbox("اللغة الهدف", ["ar", "en", "fr", "es", "de"], index=0)
    use_ocr = st.sidebar.checkbox("تفعيل OCR (للكتب الممسوحة ضوئياً)", value=False)
    translate_all = st.sidebar.button("ترجم الكتاب كاملاً")

    # --- الترجمة الدفعية ---
    if translate_all:
        progress_bar = st.progress(0)
        status_text = st.empty()
        all_translated = []

        for page_num in range(total_pages):
            status_text.text(f"جاري معالجة الصفحة {page_num + 1}/{total_pages}...")

            # استخراج النص
            if use_ocr:
                # تحويل الصفحة إلى صورة ثم OCR
                pages = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1, dpi=300)
                if pages:
                    original_text = ocr_page(pages[0])
                else:
                    original_text = ""
            else:
                # استخراج النص المباشر
                original_text = doc[page_num].get_text()

            # ترجمة النص
            if original_text.strip():
                translated = translate_text(original_text, target_lang)
                all_translated.append(f"--- Page {page_num + 1} ---\n{translated}\n")
            else:
                all_translated.append(f"--- Page {page_num + 1} ---\n(لا يوجد نص)\n")

            progress_bar.progress((page_num + 1) / total_pages)

        status_text.text("تمت الترجمة!")
        final_text = "\n".join(all_translated)

        # عرض النتيجة وتحميلها
        st.text_area("الترجمة الكاملة", final_text, height=400)
        st.download_button(
            "تحميل الترجمة (TXT)",
            final_text,
            file_name="translated_book.txt"
        )

    # --- العرض التفاعلي (صفحة بصفحة) ---
    else:
        page_num = st.sidebar.number_input("اختر الصفحة", min_value=1, max_value=total_pages, value=1) - 1

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("النص الأصلي")
            if use_ocr:
                pages = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1, dpi=300)
                original_text = ocr_page(pages[0]) if pages else ""
            else:
                original_text = doc[page_num].get_text()
            st.text_area("Original Text", original_text, height=400, key="orig")

        with col2:
            st.subheader("الترجمة")
            if st.button("ترجم هذه الصفحة"):
                with st.spinner("جاري الترجمة..."):
                    translated = translate_text(original_text, target_lang)
                    st.session_state['translated'] = translated

            if 'translated' in st.session_state:
                st.text_area("Translated Text", st.session_state['translated'], height=400, key="trans")
