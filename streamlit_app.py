import streamlit as st
import torch
import soundfile as sf
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
from pedalboard import Pedalboard, Compressor, PeakFilter
import pyloudnorm as pyln

st.set_page_config(page_title="تحسين الصوت للبودكاست", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');
.stApp { background: #000000 !important; font-family: 'Inter', sans-serif; }
.hero { text-align: center; padding: 20px 10px 10px; }
.hero h1 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 32px; color: #ffffff; margin: 6px 0 14px; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>نظّف صوتك وارفع جودته</h1>
  <p>إزالة الضوضاء تليها سلسلة معالجة تلقائية للبودكاست.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = pretrained.dns64()
    model.eval()
    return model

with st.spinner("جاري تحميل النموذج..."):
    model = load_model()

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
        wav = convert_audio(wav, sr, model.sample_rate, model.chin)
        with torch.no_grad():
            denoised = model(wav.unsqueeze(0))[0]

        audio = denoised.squeeze(0).cpu().numpy()
        sr = model.sample_rate

        # 3. حساب ذروة الصوت لتحديد العتبة النسبية للضغط
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-9)
        # العتبة تكون أقل من الذروة بـ 10dB (ضغط لطيف)
        threshold = peak_db - 10.0

        # 4. سلسلة المعالجة (بدون Highpass وبدون Gain ثابت)
        board = Pedalboard([
            # تقليل الطنين في 250Hz
            PeakFilter(cutoff_frequency_hz=250, gain_db=-2.0, q=1.0),
            # تعزيز وضوح الكلام في 3kHz
            PeakFilter(cutoff_frequency_hz=3000, gain_db=2.0, q=1.0),
            # ضغط نسبي: العتبة تُحسب تلقائياً
            Compressor(threshold_db=threshold, ratio=3.0, attack_ms=20.0, release_ms=150.0),
        ])

        processed = board(audio, sr)

        # 5. تطبيع الجهارة تلقائياً إلى -16 LUFS
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(processed.T)
        normalized = pyln.normalize.loudness(processed.T, loudness, -16.0)

        # 6. منع تجاوز الذروة
        peak = np.max(np.abs(normalized))
        if peak > 1.0:
            normalized = normalized / peak

        # 7. حفظ الملف
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, normalized, sr)

    st.success("تم! استمع للنتيجة.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
