import io
import streamlit as st
from PIL import Image
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import torch

st.set_page_config(page_title="رفع جودة الصور", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');
.stApp { background: #000000 !important; font-family: 'Inter', sans-serif; }
.hero { text-align: center; padding: 20px 10px 10px; }
.hero h1 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 32px; color: #ffffff; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>ارفع جودة صورتك</h1>
  <p>Real-ESRGAN (خفيف) لرفع الدقة 4x</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
    upsampler = RealESRGANer(
        scale=4,
        model_path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
        model=model,
        tile=256,  # ✅ تقسيم الصورة إلى قطع صغيرة لتقليل الذاكرة
        tile_pad=10,
        pre_pad=0,
        half=False,
        device="cpu",
    )
    return upsampler


with st.spinner("جاري تحميل النموذج..."):
    upsampler = load_model()

uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة الأصلية")

    # تصغير الصورة لتقليل الذاكرة
    MAX_INPUT_SIZE = 800
    if max(image.size) > MAX_INPUT_SIZE:
        image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)

    with st.spinner("جاري رفع الجودة..."):
        img_np = np.array(image)
        output, _ = upsampler.enhance(img_np, outscale=4)
        result_image = Image.fromarray(output)

    st.success("تم!")
    st.image(result_image, caption="بعد التحسين")

    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="upscaled.png", mime="image/png")
