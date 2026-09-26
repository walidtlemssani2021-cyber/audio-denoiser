import io
import streamlit as st
from PIL import Image
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from rembg import remove, new_session

st.set_page_config(page_title="أدوات الصور بالذكاء الاصطناعي", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
div[role="radiogroup"] { justify-content: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>أدوات الصور بالذكاء الاصطناعي</h1>
  <p>رفع الجودة أو نزع الخلفية بضغطة زر</p>
</div>
""", unsafe_allow_html=True)

mode = st.radio(
    "اختر الميزة",
    ["رفع جودة الصورة (x4plus)", "نزع خلفية الصورة"],
    horizontal=True,
    label_visibility="collapsed",
)

st.write("")


@st.cache_resource
def load_upscale_model():
    model_path = hf_hub_download(
        repo_id="fernandotonon/QtMeshEditor-realesrgan-onnx",
        filename="RealESRGAN_x4plus.onnx"
    )
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    return session


@st.cache_resource
def load_rembg_session():
    return new_session("birefnet-general-lite")


# ---------------- رفع جودة الصورة ----------------
if mode == "رفع جودة الصورة (x4plus)":
    load_rembg_session.clear()  # تفريغ نموذج نزع الخلفية من الذاكرة لو كان محمّل
    with st.spinner("جاري تحميل النموذج... (قد يستغرق دقيقة)"):
        session = load_upscale_model()

    uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"], key="upscale_uploader")

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="الصورة الأصلية")

        # تصغير الصورة (مهم لتقليل الذاكرة)
        MAX_INPUT_SIZE = 400
        if max(image.size) > MAX_INPUT_SIZE:
            image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
            st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

        with st.spinner("جاري رفع الجودة... (قد يستغرق وقتاً)"):
            img_array = np.asarray(image, dtype=np.float32) / 255.0
            img_array = img_array.transpose(2, 0, 1)[None, ...]  # [1, 3, H, W]

            output = session.run(None, {"input": img_array})[0][0]

            output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
            result_image = Image.fromarray(output)

        st.success("تم!")
        st.image(result_image, caption="بعد التحسين")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("تحميل الصورة", buf.getvalue(), file_name="upscaled_x4plus.png", mime="image/png")

# ---------------- نزع خلفية الصورة ----------------
else:
    load_upscale_model.clear()  # تفريغ نموذج رفع الجودة من الذاكرة لو كان محمّل
    with st.spinner("جاري تحميل النموذج... (قد يستغرق دقيقة)"):
        rembg_session = load_rembg_session()

    uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"], key="rembg_uploader")

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="الصورة الأصلية")

        # تصغير الصورة (مهم لتقليل الذاكرة) — النموذج أصلاً يشتغل بدقة محدودة داخلياً
        MAX_BG_INPUT_SIZE = 1200
        if max(image.size) > MAX_BG_INPUT_SIZE:
            image.thumbnail((MAX_BG_INPUT_SIZE, MAX_BG_INPUT_SIZE), Image.LANCZOS)
            st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

        with st.spinner("جاري نزع الخلفية..."):
            result_image = remove(image, session=rembg_session)

        st.success("تم!")
        st.image(result_image, caption="بعد نزع الخلفية")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("تحميل الصورة", buf.getvalue(), file_name="no_background.png", mime="image/png")
