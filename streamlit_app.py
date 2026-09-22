import streamlit as st
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile
import os
import argostranslate.package
import argostranslate.translate

st.set_page_config(page_title="ترجمة الكتب الممسوحة", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>ترجم كتبك الممسوحة</h1><p>Tesseract (OCR) + Argos (ترجمة)</p></div>', unsafe_allow_html=True)


@st.cache_resource
def load_translation_model():
    # تحميل حزمة الترجمة من الإنجليزية إلى العربية
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == "en" and x.to_code == "ar", available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    return True


@st.cache_resource
def configure_tesseract():
    # إعداد مسار Tesseract (يختلف حسب نظام التشغيل)
    # على Streamlit Cloud (Linux)، عادةً يكون في المسار الافتراضي
    return pytesseract.get_tesseract_version()


with st.spinner("جاري تحضير أدوات الترجمة..."):
    load_translation_model()
    configure_tesseract()

uploaded_file = st.file_uploader("ارفع ملف PDF ممسوحاً ضوئياً", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    with st.spinner("جاري تحويل الصفحات إلى صور..."):
        images = convert_from_path(pdf_path, dpi=300)

    total_pages = len(images)
    st.sidebar.write(f"عدد الصفحات: {total_pages}")

    lang = st.sidebar.selectbox(
        "لغة النص الأصلي",
        ["eng", "eng+ara"],
        index=0
    )

    page_num = st.sidebar.number_input("اختر الصفحة", 1, total_pages, 1) - 1

    with st.spinner(f"جاري استخراج النص من الصفحة {page_num + 1}..."):
        img = images[page_num].convert("L")
        img = img.point(lambda x: 0 if x < 128 else 255, '1')
        original_text = pytesseract.image_to_string(img, lang=lang)

    with st.spinner("جاري الترجمة..."):
        translated_text = argostranslate.translate.translate(original_text, "en", "ar")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("النص الأصلي")
        st.text_area("Original", original_text, height=400)

    with col2:
        st.subheader("الترجمة")
        st.text_area("Translated", translated_text, height=400)

    if st.button("استخراج وترجمة كل الصفحات"):
        all_text = []
        progress = st.progress(0)

        for i, img in enumerate(images):
            img_gray = img.convert("L")
            img_bin = img_gray.point(lambda x: 0 if x < 128 else 255, '1')
            page_text = pytesseract.image_to_string(img_bin, lang=lang)

            if page_text.strip():
                translated = argostranslate.translate.translate(page_text, "en", "ar")
                all_text.append(f"--- صفحة {i+1} ---\n{translated}\n")
            else:
                all_text.append(f"--- صفحة {i+1} ---\n(لا يوجد نص)\n")

            progress.progress((i + 1) / total_pages)

        full_text = "\n".join(all_text)
        st.text_area("الترجمة الكاملة", full_text, height=500)

        st.download_button(
            "تحميل الترجمة (TXT)",
            full_text,
            file_name="translated_book.txt"
        )

    os.unlink(pdf_path)
