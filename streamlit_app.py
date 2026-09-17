import streamlit as st
import torch
import torchaudio
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

st.set_page_config(page_title="تحسين جودة الصوت", layout="centered")

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
  <div class="mark">UMBRA AUDIO</div>
  <h1>حوّل صوتك لجودة بودكاست</h1>
  <p>تنظيف بالذكاء الاصطناعي (DNS64)، ثم نورماليزيشن وكومبريشن احترافي.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model = pretrained.dns64()
    model.eval()
    return model


def numpy_to_audiosegment(samples, sr):
    int_samples = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16)
    return AudioSegment(
        int_samples.tobytes(),
        frame_rate=sr,
        sample_width=2,
        channels=1,
    )


with st.spinner("جاري تحميل النموذج..."):
    model = load_model()

uploaded_file = st.file_uploader(
    "ارفع ملف صوتي",
    type=["wav", "mp3", "flac", "ogg"],
)

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري تنظيف الصوت وتحسينه..."):
        # 1) تنظيف الضوضاء بالنموذج
        wav, sr = torchaudio.load(input_path)
        wav = convert_audio(wav, sr, model.sample_rate, model.chin)
        with torch.no_grad():
            denoised = model(wav.unsqueeze(0))[0]
        denoised_np = denoised.squeeze().cpu().numpy()

        # 2) تحويلها لصيغة يفهمها pydub
        segment = numpy_to_audiosegment(denoised_np, model.sample_rate)

        # 3) نورماليزيشن (توحيد مستوى الصوت)
        segment = normalize(segment)

        # 4) كومبريشن (تقليل الفرق بين الأجزاء العالية والمنخفضة)
        segment = compress_dynamic_range(segment)

        output_path = "enhanced_output.wav"
        segment.export(output_path, format="wav")

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف المحسّن", f, file_name="enhanced.wav")
