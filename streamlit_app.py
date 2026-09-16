import streamlit as st
import soundfile as sf
import numpy as np
import onnxruntime as ort
import os

st.set_page_config(page_title="إزالة الضوضاء - ZipEnhancer ONNX", layout="centered")

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
  <h1>إزالة الضوضاء (ZipEnhancer ONNX)</h1>
  <p>نموذج سريع وخفيف يعمل على ONNX Runtime.</p>
</div>
""", unsafe_allow_html=True)

MODEL_PATH = "zipenhancer.onnx"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"ملف النموذج {MODEL_PATH} غير موجود.")
        return None
    session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
    return session

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    session = load_model()
    if session is None:
        st.stop()

    input_path = "input_temp.wav"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        audio, sr = sf.read(input_path, dtype="float32")
        
        # تجهيز المدخلات حسب متطلبات النموذج
        input_name = session.get_inputs()[0].name
        audio_input = audio.reshape(1, -1).astype(np.float32)
        
        outputs = session.run(None, {input_name: audio_input})
        enhanced = outputs[0].squeeze()

        output_path = "enhanced_zipenhancer_onnx.wav"
        sf.write(output_path, enhanced, 16000)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_zipenhancer_onnx.wav")
