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
.hero h1 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 32px; color: #ffffff; }
.hero p { color: #a3a3a3; font-size: 15px; }
[data-testid="stFileUploader"] { background: linear-gradient(160deg, #3fa0f5, #0a2a6b); border-radius: 14px; padding: 14px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>نظّف صوتك وارفع جودته</h1>
  <p>إزالة الضوضاء + سلسلة معالجة احترافية (De-esser حقيقي، Saturation حقيقي، Multiband).</p>
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

        # 3. De-esser ديناميكي حقيقي (يعمل فقط عند وجود حروف حادة)
        def apply_de_esser(data, rate, strength=0.5):
            """De-esser ديناميكي: يقسم الصوت إلى نطاقين ويعالج النطاق العالي فقط عند تجاوزه العتبة."""
            cutoff = 5000  # منطقة الحروف الحادة "س" و "ش"
            
            # فصل النطاق العالي
            sos_high = butter(4, cutoff, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            
            # حساب غلاف الطاقة
            env = np.abs(hilbert(high))
            sigma = (rate * 5 / 1000) / 2.355  # نافذة 5ms
            env = gaussian_filter1d(env, sigma)
            
            # حساب التخفيض (عتبة -20dB، نسبة 4:1)
            env_db = 20 * np.log10(env + 1e-10)
            gain_db = np.where(env_db > -20, (env_db + 20) * (1/4 - 1), 0.0)
            gain = 10 ** (gain_db / 20.0)
            
            # تطبيق التخفيض على النطاق العالي فقط
            high_compressed = high * gain
            
            # فصل النطاق المنخفض
            sos_low = butter(4, cutoff, 'low', fs=rate, output='sos')
            low = sosfiltfilt(sos_low, data)
            
            # الدمج
            return (1 - strength) * data + strength * (low + high_compressed)

        audio = apply_de_esser(audio, sr, strength=0.6)

        # 4. حساب العتبة النسبية للضغط
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-9)
        threshold = peak_db - 10.0

        # 5. سلسلة المعالجة (EQ + Compressor + Saturation)
        board = Pedalboard([
            # تقليل الطنين (250Hz)
            PeakFilter(cutoff_frequency_hz=250, gain_db=-2.0, q=1.0),
            
            # تعزيز الوضوح (3kHz)
            PeakFilter(cutoff_frequency_hz=3000, gain_db=2.0, q=1.0),
            
            # إضافة "الهواء" (10kHz)
            HighShelfFilter(cutoff_frequency_hz=10000, gain_db=1.5),
            
            # الضغط النسبي
            Compressor(threshold_db=threshold, ratio=3.0, attack_ms=20.0, release_ms=150.0),
        ])

        processed = board(audio, sr)

        # 6. Saturation حقيقي (إضافة توافقيات ناعمة)
        def apply_saturation(data, drive=0.1):
            """إضافة توافقيات ناعمة عبر soft-clipping (tanh) مع الحفاظ على المستوى."""
            driven = np.tanh(data * (1 + drive * 5))
            # إعادة المستوى الأصلي
            return driven / (np.max(np.abs(driven)) + 1e-9) * np.max(np.abs(data))
        
        processed = apply_saturation(processed, drive=0.15)

        # 7. Multiband Compression بسيط (3 نطاقات)
        def multiband_compress(data, rate):
            """ضغط مستقل للنطاقات: منخفض، متوسط، عالي."""
            # فصل النطاقات
            sos_low = butter(4, 300, 'low', fs=rate, output='sos')
            low = sosfiltfilt(sos_low, data)
            
            sos_mid = butter(4, [300, 3000], 'band', fs=rate, output='sos')
            mid = sosfiltfilt(sos_mid, data)
            
            sos_high = butter(4, 3000, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            
            # ضغط كل نطاق بشكل مستقل (عتبة مختلفة)
            compressor_low = Compressor(threshold_db=-25, ratio=2.5, attack_ms=30, release_ms=200)
            compressor_mid = Compressor(threshold_db=-22, ratio=3.0, attack_ms=20, release_ms=150)
            compressor_high = Compressor(threshold_db=-20, ratio=3.5, attack_ms=15, release_ms=100)
            
            low_c = compressor_low(low, rate)
            mid_c = compressor_mid(mid, rate)
            high_c = compressor_high(high, rate)
            
            # الدمج
            return low_c + mid_c + high_c

        processed = multiband_compress(processed, sr)

        # 8. تطبيع الجهارة إلى -16 LUFS
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(processed.T)
        normalized = pyln.normalize.loudness(processed.T, loudness, -16.0)

        # 9. منع تجاوز الذروة
        peak = np.max(np.abs(normalized))
        if peak > 1.0:
            normalized = normalized / peak

        # 10. حفظ الملف
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, normalized, sr)

    st.success("تم! استمع للنتيجة.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
