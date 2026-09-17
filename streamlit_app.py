import streamlit as st
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF

st.set_page_config(page_title="PDF Translator", layout="wide")

st.title("📄 PDF Translator for Human")

# دالة الترجمة
def translate_text(text, target_lang='ar'):
    if not text.strip():
        return ""
    try:
        # GoogleTranslator يدعم اللغات بدون مفتاح API
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Error: {e}"

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    # قراءة الملف في الذاكرة
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)

    st.sidebar.write(f"عدد الصفحات: {total_pages}")

    # اختيار الصفحة واللغة
    page_num = st.sidebar.number_input("اختر الصفحة", min_value=1, max_value=total_pages, value=1) - 1
    target_lang = st.sidebar.selectbox("اللغة الهدف", ["ar", "en", "fr", "es", "de"], index=0)

    # عرض الصفحة الأصلية
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("النص الأصلي")
        original_text = doc[page_num].get_text()
        st.text_area("Original Text", original_text, height=400, key="orig")

    with col2:
        st.subheader("الترجمة")
        # زر لترجمة الصفحة الحالية فقط (لحفظ الذاكرة)
        if st.button("ترجم هذه الصفحة"):
            with st.spinner("جاري الترجمة..."):
                translated = translate_text(original_text, target_lang)
                st.session_state['translated'] = translated

        # عرض الترجمة إذا كانت موجودة في الجلسة
        if 'translated' in st.session_state:
            st.text_area("Translated Text", st.session_state['translated'], height=400, key="trans")
