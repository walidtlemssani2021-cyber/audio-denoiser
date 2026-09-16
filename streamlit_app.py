import streamlit as st
import torch
import torchaudio
import soundfile as sf
from denoiser import pretrained
from denoiser.dsp import convert_audio

st.set_page_config(page_title="إزالة الضوضاء الصوتية", layout="centered")

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
  <h1>نظّف صوتك من الضوضاء</h1>
  <p>ارفع أي تسجيل صوتي، والنموذج (DNS64) يزيل الضوضاء تلقائياً خلال ثوانٍ.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model = pretrained.dns64()
    model.eval()
    return model


with st.spinner("جاري تحميل النموذج..."):
    model = load_model()

uploaded_file = st.file_uploader(
    "ارفع ملف صوتي فيه ضوضاء",
    type=["wav", "mp3", "flac", "ogg"],
)

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        wav, sr = torchaudio.load(input_path)
        wav = convert_audio(wav, sr, model.sample_rate, model.chin)
        with torch.no_grad():
            denoised = model(wav.unsqueeze(0))[0]

        output_path = "denoised_output.wav"
        sf.write(output_path, denoised.squeeze().cpu().numpy(), model.sample_rate)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف بعد التنقية",
            f,
            file_name="denoised.wav",
    )
