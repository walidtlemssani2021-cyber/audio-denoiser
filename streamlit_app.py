import streamlit as st
import soundfile as sf
import numpy as np
import sherpa_onnx
import os
import requests

st.set_page_config(page_title="إزالة الضوضاء - GTCRN", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>إزالة الضوضاء (GTCRN)</h1>
  <p>نموذج خفيف جداً (48.2K معامل) بجودة تنافسية وسرعة عالية.</p>
</div>
""", unsafe_allow_html=True)

MODEL_PATH = "gtcrn_simple.onnx"
MODEL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/speech-enhancement-models/gtcrn_simple.onnx"

@st.cache_resource
def load_model():
    # تحميل النموذج إن لم يكن موجوداً
    if not os.path.exists(MODEL_PATH):
        with st.spinner("جاري تحميل النموذج..."):
            r = requests.get(MODEL_URL, stream=True)
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    # إعداد نموذج إزالة الضوضاء
    config = sherpa_onnx.OfflineSpeechDenoiserConfig(
        model=sherpa_onnx.OfflineSpeechDenoiserModelConfig(
            gtcrn=sherpa_onnx.OfflineSpeechDenoiserGtcrnModelConfig(
                model=MODEL_PATH
            ),
            debug=False,
            num_threads=1,
            provider="cpu",
        )
    )
    return sherpa_onnx.OfflineSpeechDenoiser(config)

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    # قراءة الصوت (مع تحويله إلى أحادي القناة)
    data, sample_rate = sf.read(uploaded_file, always_2d=True, dtype="float32")
    samples = np.ascontiguousarray(data[:, 0])

    with st.spinner("جاري إزالة الضوضاء..."):
        sd = load_model()
        # معالجة الملف كاملاً في خطوة واحدة
        denoised = sd(samples, sample_rate)

    output_path = "enhanced_gtcrn.wav"
    sf.write(output_path, denoised.samples, denoised.sample_rate)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_gtcrn.wav",
        )
