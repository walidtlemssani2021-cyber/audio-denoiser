import io
import os
import concurrent.futures
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
MAX_INPUT_SIZE = 1200  # أقصى بعد للصورة قبل المعالجة (خُفِّض من 1600 لتسريع OCR)
PDF_RENDER_SCALE = 1.6  # ~115dpi عند تحويل صفحات PDF إلى صور (خُفِّض من 2.0 لتسريع OCR)
MAX_TRANSLATE_WORKERS = 5  # عدد طلبات الترجمة المتزامنة (أعلى = أسرع لكن خطر حظر أكبر من الخدمة المجانية)


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


@st.cache_resource
def get_supported_codepoints(font_path: str):
    """يرجع مجموعة الرموز (codepoints) التي يدعمها الخط فعلياً، لتفادي رموز تُسقط PDF."""
    from fontTools.ttLib import TTFont
    tt_font = TTFont(font_path)
    cmap = tt_font.getBestCmap() or {}
    return set(cmap.keys())


def sanitize_for_font(text: str, supported: set) -> str:
    """يستبدل أي رمز لا يدعمه الخط بعلامة استفهام، بدل أن يوقف البرنامج بخطأ."""
    return "".join(ch if ord(ch) in supported else "?" for ch in text)


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


def add_arabic_page(pdf: FPDF, paragraph_text: str, label: str, supported: set):
    pdf.add_page()
    max_width = pdf.w - pdf.l_margin - pdf.r_margin

    label = sanitize_for_font(label, supported)
    paragraph_text = sanitize_for_font(paragraph_text, supported)

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
        font_path = get_arabic_font_path()
        pdf.add_font(FONT_FAMILY, "", font_path)
        supported_chars = get_supported_codepoints(font_path)

        error_log = []
        failed_pages = []
        crashed_pages = []
        progress = st.progress(0.0)
        status = st.empty()

        # المرحلة 1: استخراج النص من كل صفحة (تسلسلي عمداً لضبط استهلاك الذاكرة)
        ocr_results = []  # كل عنصر: (idx, label, النص الإنجليزي أو None عند فشل الصفحة)
        for idx, (page_image, label) in enumerate(pages, start=1):
            status.write(f"جاري استخراج النص: صفحة {idx} من {total_pages}")
            try:
                page_image_resized = resize_for_memory(page_image)
                img_array = np.array(page_image_resized)
                result, _ = engine(img_array, use_cls=False)
                english_text = " ".join(item[1] for item in result) if result else ""
                ocr_results.append((idx, label, english_text))
            except Exception as e:
                crashed_pages.append(idx)
                error_log.append(f"OCR صفحة {idx}: {e}")
                ocr_results.append((idx, label, None))
            progress.progress(idx / total_pages)

        # المرحلة 2: ترجمة كل الصفحات بالتوازي (الترجمة عبر الشبكة، فتشغيلها معاً يوفّر وقتاً كبيراً)
        status.write("جاري ترجمة الصفحات (بالتوازي)...")
        translations = {}
        translatable = [(idx, text) for idx, _, text in ocr_results if text is not None]
        progress.progress(0.0)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_TRANSLATE_WORKERS) as executor:
            future_to_idx = {
                executor.submit(translate_text_block, text, error_log): idx
                for idx, text in translatable
            }
            done = 0
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    translations[idx] = future.result()
                except Exception as e:
                    translations[idx] = ("", False)
                    error_log.append(f"ترجمة صفحة {idx}: {e}")
                done += 1
                progress.progress(done / len(future_to_idx) if future_to_idx else 1.0)

        # المرحلة 3: بناء ملف PDF بالترتيب الصحيح (تسلسلي؛ سريع نسبياً)
        status.write("جاري تجميع ملف PDF...")
        for idx, label, english_text in ocr_results:
            try:
                if english_text is None:
                    add_arabic_page(pdf, "", f"{label} (تعذّرت معالجة هذه الصفحة)", supported_chars)
                    continue
                arabic_text, ok = translations.get(idx, ("", False))
                page_label = label
                if not ok:
                    failed_pages.append(idx)
                    page_label = f"{label} (لم تُترجم)"
                add_arabic_page(pdf, arabic_text, page_label, supported_chars)
            except Exception as e:
                crashed_pages.append(idx)
                error_log.append(f"صفحة {idx}: {e}")
                try:
                    add_arabic_page(pdf, "", f"{label} (تعذّرت معالجة هذه الصفحة)", supported_chars)
                except Exception:
                    pass

        status.write("تم الانتهاء من جميع الصفحات ✅")
        pdf_bytes = bytes(pdf.output())

        if failed_pages:
            st.warning(
                f"تعذّرت ترجمة {len(failed_pages)} صفحة من {total_pages} "
                f"(بقيت بالإنجليزية في الملف): {failed_pages}"
            )
        if crashed_pages:
            st.error(f"حدث خطأ أثناء معالجة {len(crashed_pages)} صفحة بالكامل: {crashed_pages}")
        if error_log:
            with st.expander("تفاصيل الأخطاء (لتشخيص المشكلة)"):
                st.code("\n".join(error_log[:10]))

        st.download_button(
            "تحميل الكتاب المترجم (PDF)",
            data=pdf_bytes,
            file_name="translated_book.pdf",
            mime="application/pdf",
        )
