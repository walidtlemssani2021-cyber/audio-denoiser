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
  <p>معالجة احترافية بمستوى بودكاست ناعم وواضح.</p>
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

        # 3. تضخيم أولي (Gain) لتوحيد المستوى
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-9)
        gain_db = -3.0 - peak_db
        audio = audio * (10 ** (gain_db / 20.0))

        # 4. De-esser متعدد النطاقات (3 نطاقات)
        def apply_multiband_de_esser(data, rate, strength=0.65):
            bands = [
                (5000, 7000, -20, 4.0),   # منطقة الحروف الرئيسية
                (7000, 9000, -22, 4.5),   # منطقة "الس" الحادة
                (9000, 11000, -24, 5.0),  # منطقة "الهواء" الحادة
            ]
            
            result = data.copy()
            for low_freq, high_freq, threshold, ratio in bands:
                # استخراج النطاق
                sos_band = butter(4, [low_freq, high_freq], 'band', fs=rate, output='sos')
                band = sosfiltfilt(sos_band, data)
                
                # حساب غلاف الطاقة
                env = np.abs(hilbert(band))
                sigma = (rate * 5 / 1000) / 2.355
                env = gaussian_filter1d(env, sigma)
                
                # حساب التخفيض
                env_db = 20 * np.log10(env + 1e-10)
                gain_db = np.where(env_db > threshold, (env_db - threshold) * (1/ratio - 1), 0.0)
                gain = 10 ** (gain_db / 20.0)
                
                # تطبيق التخفيض على النطاق
                band_compressed = band * gain
                band_original = band
                
                # الفرق بين النطاق الأصلي والمضغوط
                diff = band_compressed - band_original
                
                # تطبيق الفرق على الصوت الأصلي
                result = result + strength * diff
            
            return result

        audio = apply_multiband_de_esser(audio, sr, strength=0.65)

        # 5. سلسلة EQ (تحسين الوضوح + تقليل الحدة)
        board = Pedalboard([
            PeakFilter(cutoff_frequency_hz=250, gain_db=-2.0, q=1.0),
            PeakFilter(cutoff_frequency_hz=2000, gain_db=1.0, q=1.0),
            PeakFilter(cutoff_frequency_hz=4000, gain_db=1.5, q=1.0),
            PeakFilter(cutoff_frequency_hz=8000, gain_db=-1.5, q=1.0),
            HighShelfFilter(cutoff_frequency_hz=10000, gain_db=-3.0),
        ])
        audio = board(audio, sr)

        # 6. Saturation حقيقي (أنعم)
        def apply_saturation(data, drive=0.04):
            driven = np.tanh(data * (1 + drive * 5))
            return driven / (np.max(np.abs(driven)) + 1e-9) * np.max(np.abs(data))

        audio = apply_saturation(audio, drive=0.04)

        # 7. موازنة الصوت (LUFS) قبل الضغط
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(audio)
        gain_db = -24.0 - loudness
        audio = audio * (10 ** (gain_db / 20.0))

        # 8. Exciter خفيف (تحسين الوضوح)
        def apply_exciter(data, rate, amount=0.04):
            sos_high = butter(4, 3000, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            harmonic = np.tanh(high * 2.0) - high
            return data + amount * harmonic

        audio = apply_exciter(audio, sr, amount=0.04)

        # 9. Multiband Compression (4 نطاقات)
        def multiband_compress_4band(data, rate):
            # فصل النطاقات
            sos_low = butter(4, 300, 'low', fs=rate, output='sos')
            low = sosfiltfilt(sos_low, data)
            
            sos_mid_low = butter(4, [300, 1500], 'band', fs=rate, output='sos')
            mid_low = sosfiltfilt(sos_mid_low, data)
            
            sos_mid_high = butter(4, [1500, 4000], 'band', fs=rate, output='sos')
            mid_high = sosfiltfilt(sos_mid_high, data)
            
            sos_high = butter(4, 4000, 'high', fs=rate, output='sos')
            high = sosfiltfilt(sos_high, data)
            
            # ضغط كل نطاق بعتبة نسبية
            def relative_compress(signal, ratio, factor=10):
                peak = 20 * np.log10(np.max(np.abs(signal)) + 1e-9)
                threshold = peak - factor
                return Compressor(threshold_db=threshold, ratio=ratio, attack_ms=25, release_ms=180)(signal, rate)
            
            c_low = relative_compress(low, ratio=1.8, factor=12)
            c_mid_low = relative_compress(mid_low, ratio=1.6, factor=10)
            c_mid_high = relative_compress(mid_high, ratio=1.5, factor=8)
            c_high = relative_compress(high, ratio=1.7, factor=10)
            
            return c_low + c_mid_low + c_mid_high + c_high

        audio = multiband_compress_4band(audio, sr)

        # 10. ضغط نهائي (ناعم)
        audio = Compressor(threshold_db=-15, ratio=1.4, attack_ms=30, release_ms=250)(audio, sr)

        # 11. تطبيع نهائي إلى -24 LUFS
        meter = pyln.Meter(sr)
        final_loudness = meter.integrated_loudness(audio)
        gain_db = -24.0 - final_loudness
        audio = audio * (10 ** (gain_db / 20.0))

        # 12. منع تجاوز الذروة (-4 dBFS)
        peak_ceiling = 10 ** (-4.0 / 20.0)
        peak = np.max(np.abs(audio))
        if peak > peak_ceiling:
            audio = np.tanh(audio * (1 / peak_ceiling)) * peak_ceiling

        # 13. حفظ الملف
        output_path = "enhanced_podcast.wav"
        sf.write(output_path, audio, sr)

    st.success("تم! استمع للنتيجة.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_podcast.wav")
