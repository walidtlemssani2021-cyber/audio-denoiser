import streamlit as st
import soundfile as sf
import numpy as np
import onnxruntime as ort
import os
import tempfile

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


def process_chunk(session, chunk_audio):
    """معالجة قطعة صوتية واحدة عبر ONNX."""
    input_name = session.get_inputs()[0].name
    audio_input = chunk_audio.reshape(1, -1).astype(np.float32)
    outputs = session.run(None, {input_name: audio_input})
    return outputs[0].squeeze()


uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    session = load_model()
    if session is None:
        st.stop()

    # حفظ الملف في مسار مؤقت
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.getbuffer())
        input_path = tmp.name

    with st.spinner("جاري إزالة الضوضاء..."):
        # قراءة معلومات الملف فقط (بدون تحميله كاملاً)
        info = sf.info(input_path)
        sr = info.samplerate
        total_frames = info.frames

        # حجم القطعة: 10 ثوانٍ (لتقليل استهلاك الذاكرة)
        chunk_size = sr * 10
        enhanced_chunks = []

        # معالجة على شكل قطع
        with sf.SoundFile(input_path, 'r') as f:
            while True:
                chunk = f.read(chunk_size, dtype='float32')
                if len(chunk) == 0:
                    break
                # تحويل إلى mono إذا كان stereo
                if chunk.ndim > 1:
                    chunk = chunk.mean(axis=1)
                enhanced_chunk = process_chunk(session, chunk)
                enhanced_chunks.append(enhanced_chunk)

        enhanced = np.concatenate(enhanced_chunks)

        output_path = "enhanced_zipenhancer_onnx.wav"
        sf.write(output_path, enhanced, 16000)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_zipenhancer_onnx.wav")
