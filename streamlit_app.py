import streamlit as st
import torch
import soundfile as sf
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
from audiosronnx import load_sr

st.set_page_config(page_title="تنقية ورفع جودة الصوت", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');
.stApp { background: #000000 !important; font-family: 'Inter', sans-serif; }
.hero { text-align: center; padding: 20px 10px 10px; }
.hero h1 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 32px; color: #ffffff; margin: 6px 0 14px; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>نظّف صوتك وارفع جودته</h1>
  <p>DNS64 لإزالة الضوضاء + LavaSR لرفع الدقة إلى 48kHz.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_dns_model():
    model = pretrained.dns64()
    model.eval()
    return model


@st.cache_resource
def load_sr_model():
    return load_sr("lavasr")


with st.spinner("جاري تحميل النماذج..."):
    dns_model = load_dns_model()
    sr_model = load_sr_model()

uploaded_file = st.file_uploader("ارفع ملف صوتي فيه ضوضاء", type=["wav", "flac"])

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري المعالجة..."):
        # 1. قراءة الصوت
        wav_np, sr = sf.read(input_path, dtype="float32")
        wav = torch.from_numpy(wav_np).float()
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        else:
            wav = wav.T

        # 2. إزالة الضوضاء (DNS64)
        wav = convert_audio(wav, sr, dns_model.sample_rate, dns_model.chin)
        with torch.no_grad():
            denoised = dns_model(wav.unsqueeze(0))[0]

        audio = denoised.squeeze(0).cpu().numpy()
        sr = dns_model.sample_rate

        # 3. رفع الدقة (LavaSR)
        audio, sr = sr_model.upscale(audio, sr)

        # 4. حفظ الملف
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, audio, sr)

    st.success("تم! استمع للنتيجة.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
