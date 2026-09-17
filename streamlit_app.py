import streamlit as st
import torch
import soundfile as sf
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
from pedalboard import Pedalboard, Compressor, PeakFilter, HighShelfFilter
import pyloudnorm as pyln
from scipy.signal import butter, sosfiltfilt, hilbert
from scipy.ndimage import gaussian_filter1d

st.set_page_config(page_title="تحسين الصوت للبودكاست", layout="centered")

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
  <p>معالجة احترافية بمستوى بودكاست ناعم ومستقر.</p>
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

        # 3. De-esser ديناميكي (أقوى لتقليل الحدة)
        def apply_de_esser(data, rate, strength=0.6):
            cutoff = 5000
            sos_high = butter(4, cutoff, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            env = np.abs(hilbert(high))
            sigma = (rate * 5 / 1000) / 2.355
            env = gaussian_filter1d(env, sigma)
            env_db = 20 * np.log10(env + 1e-10)
            gain_db = np.where(env_db > -20, (env_db + 20) * (1/4 - 1), 0.0)
            gain = 10 ** (gain_db / 20.0)
            high_compressed = high * gain
            sos_low = butter(4, cutoff, 'low', fs=rate, output='sos')
            low = sosfiltfilt(sos_low, data)
            return (1 - strength) * data + strength * (low + high_compressed)

        audio = apply_de_esser(audio, sr, strength=0.6)

        # 4. حساب العتبة النسبية للضغط
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-9)
        threshold = peak_db - 10.0

        # 5. سلسلة المعالجة (EQ + Compressor) - تقليل الحدة
        board = Pedalboard([
            PeakFilter(cutoff_frequency_hz=250, gain_db=-2.0, q=1.0),
            PeakFilter(cutoff_frequency_hz=3000, gain_db=0.5, q=0.8),
            HighShelfFilter(cutoff_frequency_hz=10000, gain_db=-2.0),
            Compressor(threshold_db=threshold, ratio=3.0, attack_ms=20.0, release_ms=150.0),
        ])

        processed = board(audio, sr)

        # 6. Saturation حقيقي (أنعم)
        def apply_saturation(data, drive=0.08):
            driven = np.tanh(data * (1 + drive * 5))
            return driven / (np.max(np.abs(driven)) + 1e-9) * np.max(np.abs(data))

        processed = apply_saturation(processed, drive=0.08)

        # 7. Multiband Compression (3 نطاقات) - ضغط لطيف
        def multiband_compress(data, rate):
            sos_low = butter(4, 300, 'low', fs=rate, output='sos')
            low = sosfiltfilt(sos_low, data)
            sos_mid = butter(4, [300, 3000], 'band', fs=rate, output='sos')
            mid = sosfiltfilt(sos_mid, data)
            sos_high = butter(4, 3000, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            
            c_low = Compressor(threshold_db=-25, ratio=2.0, attack_ms=30, release_ms=200)
            c_mid = Compressor(threshold_db=-20, ratio=2.0, attack_ms=25, release_ms=180)
            c_high = Compressor(threshold_db=-20, ratio=2.5, attack_ms=15, release_ms=100)
            
            return c_low(low, rate) + c_mid(mid, rate) + c_high(high, rate)

        processed = multiband_compress(processed, sr)

        # 8. ضغط إضافي لطيف (للاستقرار)
        processed = Compressor(threshold_db=-15, ratio=2.0, attack_ms=30, release_ms=250)(processed, sr)

        # 9. تطبيع الجهارة إلى -22 LUFS مع حد ذروة -3 dBFS
        TARGET_LUFS = -22.0
        PEAK_CEILING_DB = -3.0

        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(processed.T)

        gain_db = TARGET_LUFS - loudness
        gain_linear = 10 ** (gain_db / 20.0)
        normalized = processed.T * gain_linear

        peak_ceiling = 10 ** (PEAK_CEILING_DB / 20.0)
        peak = np.max(np.abs(normalized))

        if peak > peak_ceiling:
            normalized = np.tanh(normalized * (1 / peak_ceiling)) * peak_ceiling

        final_loudness = meter.integrated_loudness(normalized)
        if final_loudness < TARGET_LUFS - 0.5:
            correction_db = TARGET_LUFS - final_loudness
            normalized = normalized * (10 ** (correction_db / 20.0))
            peak = np.max(np.abs(normalized))
            if peak > peak_ceiling:
                normalized = np.tanh(normalized * (1 / peak_ceiling)) * peak_ceiling

        # 10. حفظ الملف
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, normalized, sr)

    st.success("تم! استمع للنتيجة.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
