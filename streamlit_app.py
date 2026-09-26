import io
import streamlit as st
from PIL import Image
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="رفع جودة الصور - RealESRGAN x4plus", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>ارفع جودة صورتك (x4plus)</h1>
  <p>RealESRGAN x4plus (FP32) — الأقوى في العائلة</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model_path = hf_hub_download(
        repo_id="fernandotonon/QtMeshEditor-realesrgan-onnx",
        filename="RealESRGAN_x4plus.onnx"
    )
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    return session


with st.spinner("جاري تحميل النموذج... (قد يستغرق دقيقة)"):
    session = load_model()

uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"])

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
