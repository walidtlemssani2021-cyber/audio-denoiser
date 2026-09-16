import streamlit as st
import soundfile as sf
import numpy as np
import onnxruntime as ort
import requests
import os

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
    
    # إنشاء جلسة ONNX
    session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
    return session

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    # قراءة الصوت
    audio, sr = sf.read(uploaded_file, dtype="float32")

    # GTCRN يتوقع 16kHz mono
    if sr != 16000:
        # إعادة تشكيل بسيطة (resample)
        import torch
        import torchaudio
        audio = torch.from_numpy(audio).float()
        if audio.dim() > 1:
            audio = audio.mean(dim=1)
        audio = torchaudio.functional.resample(audio, sr, 16000).numpy()
        sr = 16000

    with st.spinner("جاري إزالة الضوضاء..."):
        session = load_model()
        
        # تجهيز المدخلات (GTCRN يتوقع شكل معين من ONNX)
        # المدخلات: [batch, 1, time] أو مشابه حسب النموذج
        input_name = session.get_inputs()[0].name
        input_shape = session.get_inputs()[0].shape
        
        # عادةً ما يتوقع [1, 1, T] أو [1, T, 1]
        if len(input_shape) == 3:
            if input_shape[1] == 1:
                audio_input = audio.reshape(1, 1, -1)
            else:
                audio_input = audio.reshape(1, -1, 1)
        else:
            audio_input = audio.reshape(1, -1)
        
        # تشغيل النموذج
        outputs = session.run(None, {input_name: audio_input})
        enhanced = outputs[0].squeeze()
        
        # حفظ النتيجة
        output_path = "enhanced_gtcrn.wav"
        sf.write(output_path, enhanced, 16000)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_gtcrn.wav",
              )
