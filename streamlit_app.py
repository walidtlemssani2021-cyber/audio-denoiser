import streamlit as st
import numpy as np
import soundfile as sf
from deepfilter_stream import DeepFilterModel

st.set_page_config(page_title="إزالة الضوضاء - DeepFilterNet", layout="centered")

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
  <h1>إزالة الضوضاء (DeepFilterNet)</h1>
  <p>نموذج خفيف وسريع، يعمل عبر ONNX بدون الحاجة إلى Rust.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    # تحميل نموذج ONNX (سيتم تنزيله تلقائياً عند أول استخدام)
    model = DeepFilterModel()
    return model

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    # قراءة الصوت باستخدام soundfile (بدون torchaudio)
    audio, sr = sf.read(uploaded_file, dtype="float32")

    with st.spinner("جاري إزالة الضوضاء..."):
        model = load_model()
        # إنشاء تدفق معالجة جديد
        stream = model.new_stream()
        # معالجة الصوت (المكتبة تدعم معدلات عينات مختلفة)
        enhanced = stream.process(audio, sr=sr)
        # تفريغ أي بقايا مخزنة
        tail = stream.flush()
        if len(tail) > 0:
            enhanced = np.concatenate([enhanced, tail])

    # حفظ النتيجة بمعدل 48kHz (المعدل الذي ينتجه النموذج)
    output_path = "enhanced_deepfilternet.wav"
    sf.write(output_path, enhanced, 48000)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_deepfilternet.wav",
        )
