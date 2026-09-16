import streamlit as st
import numpy as np
import soundfile as sf
import torch
import os
import requests
from ai_edge_litert.interpreter import Interpreter

st.set_page_config(page_title="تنقية وترميم الصوت", layout="centered")

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
  <h1>نظّف صوتك وارفع جودته</h1>
  <p>اختر العملية: إزالة الضوضاء أو رفع الجودة، أو كلاهما معاً.</p>
</div>
""", unsafe_allow_html=True)

# --- إعدادات CMGAN ---
CMGAN_SR = 16000
CMGAN_NFFT = 400
CMGAN_HOP = 100
CMGAN_CHUNK = 32000

@st.cache_resource
def load_cmgan_model():
    model_url = "https://huggingface.co/litert-community/CMGAN-LiteRT/resolve/main/cmgan_fp16.tflite"
    model_path = "cmgan_fp16.tflite"
    if not os.path.exists(model_path):
        r = requests.get(model_url)
        with open(model_path, "wb") as f:
            f.write(r.content)
    return model_path

@st.cache_resource
def load_lavasr_model():
    try:
        from audio_super_resolution import AudioSuperResolver
        resolver = AudioSuperResolver(target_sr=48000)
        return resolver
    except Exception as e:
        st.error(f"خطأ في تحميل LavaSR: {e}")
        return None

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV أو FLAC)", type=["wav", "flac"])

option = st.radio(
    "اختر العملية:",
    ("إزالة الضوضاء فقط", "رفع الجودة فقط", "إزالة الضوضاء + رفع الجودة"),
)

if uploaded_file is not None:
    input_path = "input_temp." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --- المرحلة الأولى: CMGAN ---
    if option in ["إزالة الضوضاء فقط", "إزالة الضوضاء + رفع الجودة"]:
        with st.spinner("جاري إزالة الضوضاء (CMGAN)..."):
            cmgan_path = load_cmgan_model()
            wav, sr = sf.read(input_path, dtype="float32")
            if len(wav.shape) > 1:
                wav = wav.mean(axis=1)
            if sr != CMGAN_SR:
                import torchaudio
                wav = torchaudio.functional.resample(
                    torch.from_numpy(wav).float(), sr, CMGAN_SR
                ).numpy()

            outputs = []
            for i in range(0, len(wav), CMGAN_CHUNK):
                chunk = wav[i:i+CMGAN_CHUNK]
                if len(chunk) < 100:
                    continue
                x = np.zeros(CMGAN_CHUNK, np.float32)
                x[:len(chunk)] = chunk
                c = np.sqrt(CMGAN_CHUNK / (x @ x + 1e-12))
                x *= c
                xp = np.concatenate([
                    x[CMGAN_NFFT//2:0:-1],
                    x,
                    x[-2:-CMGAN_NFFT//2-2:-1]
                ])
                it = Interpreter(model_path=cmgan_path)
                it.allocate_tensors()
                it.set_tensor(it.get_input_details()[0]["index"], xp[None])
                it.invoke()
                r, i = (torch.tensor(it.get_tensor(o["index"])) for o in
                        sorted(it.get_output_details(), key=lambda o: o["index"]))
                m2 = (r * r + i * i).clamp_min(1e-12) ** (7.0 / 6.0)
                spec = torch.complex(r * m2, i * m2)[0, 0].T
                den = torch.istft(
                    spec, CMGAN_NFFT, CMGAN_HOP,
                    window=torch.hamming_window(CMGAN_NFFT),
                    length=CMGAN_CHUNK
                )
                outputs.append((den.numpy() / c)[:len(chunk)])

            clean_audio = np.concatenate(outputs)
            sf.write("denoised_temp.wav", clean_audio, CMGAN_SR)
            current_path = "denoised_temp.wav"
    else:
        current_path = input_path

    # --- المرحلة الثانية: LavaSR ---
    if option in ["رفع الجودة فقط", "إزالة الضوضاء + رفع الجودة"]:
        with st.spinner("جاري رفع الجودة (LavaSR)..."):
            resolver = load_lavasr_model()
            if resolver:
                output_path = "final_output.wav"
                resolver.enhance(current_path, output_path)
            else:
                output_path = current_path
    else:
        output_path = current_path

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_output.wav")
