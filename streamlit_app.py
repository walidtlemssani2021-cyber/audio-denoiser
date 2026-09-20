import io
import streamlit as st
import torch
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, Swin2SRForImageSuperResolution

st.set_page_config(page_title="رفع جودة الصور", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: #000000 !important;
    font-family: 'Inter', sans-serif;
}

.hero {
    text-align: center;
    padding: 20px 10px 10px;
}
.hero .mark {
    font-family: 'Fraunces', serif;
    color: #ffffff;
    opacity: 0.75;
    font-size: 14px;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 32px;
    color: #ffffff;
    margin: 6px 0 14px;
}
.hero p {
    color: #a3a3a3;
    font-size: 15px;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(160deg, #3fa0f5, #0a2a6b);
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.15);
}
[data-testid="stFileUploader"] * {
    color: #eaf3ff !important;
}

.stDownloadButton button, .stButton button {
    background: #ffffff !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 100px !important;
    font-weight: 600 !important;
    box-shadow: 0 0 28px rgba(255,255,255,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="mark">UMBRA VISION</div>
  <h1>ارفع جودة صورتك</h1>
  <p>ارفع أي صورة، والنموذج (Swin2SR) يكبّرها ويرفع دقتها ٤ أضعاف تلقائياً.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained("caidas/swin2SR-classical-sr-x4-64")
    model = Swin2SRForImageSuperResolution.from_pretrained("caidas/swin2SR-classical-sr-x4-64")
    model.eval()
    return processor, model


with st.spinner("جاري تحميل النموذج..."):
    processor, model = load_model()

uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة الأصلية")

    with st.spinner("جاري رفع الجودة... (قد يأخذ دقيقة حسب حجم الصورة)"):
        inputs = processor(image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        output = outputs.reconstruction.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.moveaxis(output, 0, -1)
        output = (output * 255.0).round().astype(np.uint8)
        result_image = Image.fromarray(output)

    st.success("تم! الصورة بعد رفع الجودة:")
    st.image(result_image, caption="بعد التحسين")

    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    st.download_button("تحميل الصورة المحسّنة", buf.getvalue(), file_name="upscaled.png", mime="image/png")
