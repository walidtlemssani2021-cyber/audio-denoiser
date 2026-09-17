import streamlit as st
import torch
import soundfile as sf
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
from pedalboard import Pedalboard, HighpassFilter, Compressor, PeakFilter, LowShelfFilter, HighShelfFilter, Gain
import pyloudnorm as pyln

st.set_page_config(page_title="تحسين الصوت للبودكاست", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');
.stApp { background: #000000 !important; font-family: 'Inter', sans-serif; }
.hero { text-align: center; padding: 20px 10px 10px; }
.hero .mark { font-family: 'Fraunces', serif; color: #ffffff; opacity: 0.75; font-size: 14px; letter-spacing: 0.1em; margin-bottom: 10px; }
.hero h1 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 32px; color: #ffffff; margin: 6px 0 14px; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; border: 1px solid rgba(255,255,255,0.15); }
[data-testid="stFileUploader"] * { color: #eaf3ff !important; }
.stDownloadButton button, .stButton button { background: #ffffff !important; color: #000000 !important; border: none !important; border-radius: 100px !important; font-weight: 600 !important; box-shadow: 0 0 28px rgba(255,255,255,0.4) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="mark">UMBRA AUDIO</div>
  <h1>نظّف صوتك وارفع جودته</h1>
  <p>إزالة الضوضاء تليها سلسلة معالجة احترافية للبودكاست.</p>
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

    with st.spinner("جاري إزالة الضوضاء وتحسين الصوت..."):
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
        
        # 3. تحويل للـ numpy للمعالجة الإضافية
        audio = denoised.squeeze(0).cpu().numpy()
        sr = model.sample_rate
        
        # 4. سلسلة المعالجة الاحترافية للبودكاست
        # الترتيب: High-pass -> EQ -> Compressor -> Makeup Gain
        board = Pedalboard([
            # قطع الترددات المنخفضة تحت 80Hz (الاهتزازات)
            HighpassFilter(cutoff_frequency_hz=80),
            
            # تقليل الطنين في منطقة 250Hz (2-3 dB)
            PeakFilter(cutoff_frequency_hz=250, gain_db=-3.0, q=1.0),
            
            # تعزيز الوضوح في 3kHz (2 dB)
            PeakFilter(cutoff_frequency_hz=3000, gain_db=2.0, q=1.0),
            
            # ضغط الصوت: 3:1 مع عتبة -20dB و10dB تعويض
            Compressor(threshold_db=-20.0, ratio=3.0, attack_ms=20.0, release_ms=150.0),
            
            # تعويض مستوى الصوت بعد الضغط
            Gain(gain_db=6.0)
        ])
        
        processed = board(audio, sr)
        
        # 5. التطبيع (Normalization) إلى -16 LUFS مع سقف -1 dBTP
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(processed.T)
        normalized = pyln.normalize.loudness(processed.T, loudness, -16.0)
        
        # ضمان عدم تجاوز الذروة
        peak = np.max(np.abs(normalized))
        if peak > 1.0:
            normalized = normalized / peak
        
        # 6. حفظ الملف النهائي
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, normalized, sr)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
