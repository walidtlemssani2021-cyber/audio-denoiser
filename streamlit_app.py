import os
import requests
import streamlit as st
from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from deep_translator import GoogleTranslator
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

st.set_page_config(page_title="استخراج وترجمة نص الكتب", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>استخراج وترجمة نص الكتب</h1><p>قراءة الصفحة (RapidOCR) ثم ترجمتها للعربية وتصديرها PDF</p></div>', unsafe_allow_html=True)

# خط عربي (Amiri) يُحمَّل مرة واحدة عند أول تشغيل ويُخبَّأ محلياً
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
FONT_PATH = "/tmp/Amiri-Regular.ttf"


@st.cache_resource
def load_ocr_engine():
    return RapidOCR()


@st.cache_resource
def get_arabic_font_path():
    if not os.path.exists(FONT_PATH):
        response = requests.get(FONT_URL, timeout=30)
        response.raise_for_status()
        with open(FONT_PATH, "wb") as f:
            f.write(response.content)
    return FONT_PATH


def translate_line_to_arabic(translator: GoogleTranslator, line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    try:
        return translator.translate(line) or line
    except Exception:
        # في حال فشل الاتصال بخدمة الترجمة لهذا السطر، نُبقي النص الأصلي بدل إيقاف كل العملية
        return line


def build_arabic_pdf(arabic_lines, font_path: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.add_font(fname=font_path)
    pdf.set_font("Amiri", size=14)

    for line in arabic_lines:
        if line:
            reshaped = arabic_reshaper.reshape(line)
            bidi_line = get_display(reshaped)
        else:
            bidi_line = ""
        pdf.multi_cell(0, 10, bidi_line, align="R")

    return bytes(pdf.output())


with st.spinner("جاري تحميل محرك القراءة..."):
    engine = load_ocr_engine()

uploaded_file = st.file_uploader("ارفع صورة صفحة من الكتاب", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصفحة الأصلية")

    # تصغير الصورة لتقليل استهلاك الذاكرة (مهم على استضافات بذاكرة محدودة مثل Streamlit Cloud)
    MAX_INPUT_SIZE = 1600
    if max(image.size) > MAX_INPUT_SIZE:
        image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
        st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

    with st.spinner("جاري التعرف على النص..."):
        img_array = np.array(image)
        result, elapse = engine(img_array)

    if not result:
        st.warning("لم يتم العثور على نص واضح في الصورة.")
    else:
        english_lines = [item[1] for item in result]

        with st.expander(f"عرض النص الإنجليزي المستخرج ({len(english_lines)} سطر)"):
            st.text_area("النص الأصلي", value="\n".join(english_lines), height=200)

        with st.spinner("جاري الترجمة إلى العربية..."):
            translator = GoogleTranslator(source="en", target="ar")
            arabic_lines = [translate_line_to_arabic(translator, line) for line in english_lines]

        st.success("تمت الترجمة.")
        st.text_area("النص المترجم", value="\n".join(arabic_lines), height=250)

        with st.spinner("جاري إنشاء ملف PDF..."):
            font_path = get_arabic_font_path()
            pdf_bytes = build_arabic_pdf(arabic_lines, font_path)

        st.download_button(
            "تحميل الترجمة (PDF)",
            data=pdf_bytes,
            file_name="translated_arabic.pdf",
            mime="application/pdf",
        )
