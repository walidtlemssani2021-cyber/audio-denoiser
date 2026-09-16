import streamlit as st
from clearvoice import ClearVoice
import soundfile as sf
import tempfile
import os

st.set_page_config(page_title="إزالة الضوضاء - DCCRN", layout="centered")

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
  <h1>إزالة الضوضاء (DCCRN)</h1>
  <p>نموذج قوي يعالج الطور والاتساع معاً.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return ClearVoice(task='speech_enhancement', model_names=['DCCRN_SE_16K'])


uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    input_path = "input_temp.wav"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        model = load_model()
        output_wav = model(input_path=input_path, online_write=False)
        
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "enhanced_dccrn.wav")
        model.write(output_wav, output_path=output_path)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_dccrn.wav")
