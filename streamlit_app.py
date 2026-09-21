import io
import os
import requests
import streamlit as st
from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from deep_translator import GoogleTranslator, MyMemoryTranslator
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF
import pypdfium2 as pdfium

st.set_page_config(page_title="ترجمة كتاب PDF إلى العربية", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button, .stButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>ترجمة كتاب PDF إلى العربية</h1><p>ارفع ملف PDF للكتاب، ونعيده لك PDF عربي واحد</p></div>', unsafe_allow_html=True)

# خط عربي (Amiri) يُحمَّل مرة واحدة عند أول تشغيل ويُخبَّأ محلياً
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
FONT_PATH = "/tmp/Amiri-Regular.ttf"
FONT_FAMILY = "Amiri"  # اسم صريح للعائلة كي لا يعتمد على اسم ملف الخط
MAX_INPUT_SIZE = 1600  # أقصى بعد للصورة قبل المعالجة، لتقليل استهلاك الذاكرة
PDF_RENDER_SCALE = 2.0  # ~144dpi عند تحويل صفحات PDF إلى صور


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


def resize_for_memory(image: Image.Image) -> Image.Image:
    if max(image.size) > MAX_INPUT_SIZE:
        image = image.copy()
        image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
    return image


def extract_pdf_pages(pdf_file):
    """يحوّل كل صفحات ملف PDF المرفوع إلى قائمة (صورة الصفحة, وسم الصفحة)."""
    pdf_bytes = pdf_file.getvalue()
    doc = pdfium.PdfDocument(io.BytesIO(pdf_bytes))
    pages = []
    for i in range(len(doc)):
        page = doc[i]
        image = page.render(scale=PDF_RENDER_SCALE).to_pil().convert("RGB")
        pages.append((image, f"صفحة {i + 1}"))
    return pages


def split_by_limit(text: str, limit: int):
    words = text.split(" ")
    parts, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 > limit:
            parts.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        parts.append(current)
    return parts


def translate_text_block(text: str, error_log: list) -> tuple:
    """يترجم النص للعربية. يجرّب Google أولاً، وإن فشل يجرّب MyMemory كبديل.
    يُرجع (النص المترجم أو الأصلي, نجحت الترجمة أم لا)."""
    text = text.strip()
    if not text:
        return "", True

    # المحاولة الأولى: Google (عبر deep-translator)
    try:
        parts = split_by_limit(text, 4500)
        google = GoogleTranslator(source="en", target="ar")
        return " ".join(google.translate(p) or p for p in parts), True
    except Exception as e:
        error_log.append(f"Google: {e}")

    # المحاولة الثانية: MyMemory كبديل (حد أقصر تقريباً 500 حرف لكل طلب)
    try:
        parts = split_by_limit(text, 450)
        mymemory = MyMemoryTranslator(source="en", target="ar")
        return " ".join(mymemory.translate(p) or p for p in parts), True
    except Exception as e:
        error_log.append(f"MyMemory: {e}")

    return text, False


def wrap_arabic_paragraph(pdf: FPDF, text: str, max_width: float):
    """يقسّم الفقرة إلى أسطر تناسب عرض الصفحة، بالترتيب المنطقي قبل التشكيل البصري (bidi)."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        reshaped = arabic_reshaper.reshape(candidate)
        if not current or pdf.get_string_width(reshaped) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def add_arabic_page(pdf: FPDF, paragraph_text: str, label: str):
    pdf.add_page()
    max_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font(FONT_FAMILY, size=10)
    pdf.cell(0, 8, get_display(arabic_reshaper.reshape(label)), align="C", ln=1)
    pdf.ln(2)

    pdf.set_font(FONT_FAMILY, size=13)
    if paragraph_text.strip():
        for line in wrap_arabic_paragraph(pdf, paragraph_text, max_width):
            bidi_line = get_display(arabic_reshaper.reshape(line))
            pdf.cell(0, 9, bidi_line, align="R", ln=1)
    else:
        pdf.cell(0, 9, get_display(arabic_reshaper.reshape("(لم يُعثر على نص في هذه الصفحة)")), align="C", ln=1)


with st.spinner("جاري تحميل محرك القراءة..."):
    engine = load_ocr_engine()

pdf_file = st.file_uploader(
    "ارفع ملف PDF للكتاب كاملاً",
    type=["pdf"],
    accept_multiple_files=False,
)

if pdf_file is not None:
    pages = extract_pdf_pages(pdf_file)
    total_pages = len(pages)
    st.info(f"تم التعرف على {total_pages} صفحة إجمالاً. قد تستغرق الترجمة بضع ثوانٍ لكل صفحة.")

    if st.button("ابدأ الاستخراج والترجمة"):
        pdf = FPDF()
        pdf.set_margins(15, 15, 15)
        pdf.add_font(FONT_FAMILY, "", get_arabic_font_path())

        progress = st.progress(0.0)
        status = st.empty()
        error_log = []
        failed_pages = []

        for idx, (page_image, label) in enumerate(pages, start=1):
            status.write(f"جاري معالجة الصفحة {idx} من {total_pages}: {label}")

            page_image = resize_for_memory(page_image)
            img_array = np.array(page_image)
            result, _ = engine(img_array)

            english_text = " ".join(item[1] for item in result) if result else ""
            arabic_text, ok = translate_text_block(english_text, error_log)
            if not ok:
                failed_pages.append(idx)
                label = f"{label} ⚠️ لم تُترجم"

            add_arabic_page(pdf, arabic_text, label)
            progress.progress(idx / total_pages)

        status.write("تم الانتهاء من جميع الصفحات ✅")
        pdf_bytes = bytes(pdf.output())

        if failed_pages:
            st.warning(
                f"تعذّرت ترجمة {len(failed_pages)} صفحة من {total_pages} "
                f"(بقيت بالإنجليزية في الملف): {failed_pages}"
            )
            with st.expander("تفاصيل الخطأ (لتشخيص المشكلة)"):
                st.code("\n".join(error_log[:5]))

        st.download_button(
            "تحميل الكتاب المترجم (PDF)",
            data=pdf_bytes,
            file_name="translated_book.pdf",
            mime="application/pdf",
        )
