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
    ["رفع جودة الصورة", "نزع خلفية الصورة"],
    horizontal=True,
    label_visibility="collapsed",
)

st.write("")


@st.cache_resource
def load_upscale_model():
    model_path = hf_hub_download(
        repo_id="Heliosoph/realesrgan-onnx",
        filename="realesr-general-x4v3.onnx"
    )
    return ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])


@st.cache_resource
def load_rembg_session():
    return new_session("u2net")


# ---------------- رفع جودة الصورة ----------------
if mode == "رفع جودة الصورة":
    load_rembg_session.clear()  # تفريغ نموذج نزع الخلفية من الذاكرة لو كان محمّل

    with st.spinner("جاري تحميل النموذج..."):
        session = load_upscale_model()

    uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"], key="upscale_uploader")

    if uploaded_file is not None:
        file_key = f"upscale_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("upscale_key") != file_key:
            image = Image.open(uploaded_file).convert("RGB")

            MAX_INPUT_SIZE = 800
            if max(image.size) > MAX_INPUT_SIZE:
                image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
                st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

            with st.spinner("جاري رفع الجودة..."):
                img_array = np.asarray(image, dtype=np.float32) / 255.0
                img_array = img_array.transpose(2, 0, 1)[None, ...]

                output = session.run(None, {"input": img_array})[0][0]

                output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
                result_image = Image.fromarray(output)

            st.session_state.upscale_key = file_key
            st.session_state.upscale_original = image
            st.session_state.upscale_result = result_image

        image = st.session_state.upscale_original
        result_image = st.session_state.upscale_result

        st.image(image, caption="الصورة الأصلية")
        st.success("تم!")
        st.image(result_image, caption="بعد التحسين")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("تحميل الصورة", buf.getvalue(), file_name="upscaled.png", mime="image/png")

# ---------------- نزع خلفية الصورة ----------------
else:
    with st.spinner("جاري تحميل النماذج..."):
        rembg_session = load_rembg_session()
        upscale_session = load_upscale_model()

    uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"], key="rembg_uploader")

    if uploaded_file is not None:
        file_key = f"rembg_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("rembg_key") != file_key:
            image = Image.open(uploaded_file).convert("RGB")

            MAX_BG_INPUT_SIZE = 2000
            if max(image.size) > MAX_BG_INPUT_SIZE:
                image.thumbnail((MAX_BG_INPUT_SIZE, MAX_BG_INPUT_SIZE), Image.LANCZOS)
                st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

            with st.spinner("جاري نزع الخلفية..."):
                no_bg_image = remove(image, session=rembg_session)  # RGBA

            # فصل قناة الشفافية (alpha) عن الألوان (RGB) لأن نموذج رفع الجودة يتعامل مع 3 قنوات فقط
            rgb_part = no_bg_image.convert("RGB")
            alpha_part = no_bg_image.split()[-1]

            MAX_UPSCALE_INPUT_SIZE = 800
            if max(rgb_part.size) > MAX_UPSCALE_INPUT_SIZE:
                rgb_part.thumbnail((MAX_UPSCALE_INPUT_SIZE, MAX_UPSCALE_INPUT_SIZE), Image.LANCZOS)
                alpha_part = alpha_part.resize(rgb_part.size, Image.LANCZOS)
                st.info(f"تم تصغير الصورة إلى {rgb_part.size} قبل رفع الجودة لتقليل استهلاك الذاكرة.")

            with st.spinner("جاري رفع جودة النتيجة..."):
                img_array = np.asarray(rgb_part, dtype=np.float32) / 255.0
                img_array = img_array.transpose(2, 0, 1)[None, ...]

                output = upscale_session.run(None, {"input": img_array})[0][0]

                output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
                upscaled_rgb = Image.fromarray(output)

                # تكبير قناة الشفافية لنفس حجم الصورة بعد رفع الجودة
                upscaled_alpha = alpha_part.resize(upscaled_rgb.size, Image.LANCZOS)
                result_image = Image.merge("RGBA", (*upscaled_rgb.split(), upscaled_alpha))

            st.session_state.rembg_key = file_key
            st.session_state.rembg_original = image
            st.session_state.rembg_result = result_image

        image = st.session_state.rembg_original
        result_image = st.session_state.rembg_result

        st.image(image, caption="الصورة الأصلية")
        st.success("تم!")
        st.image(result_image, caption="بعد نزع الخلفية ورفع الجودة")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("تحميل الصورة", buf.getvalue(), file_name="no_background_upscaled.png", mime="image/png")
