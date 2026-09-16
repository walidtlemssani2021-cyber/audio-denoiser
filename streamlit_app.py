import streamlit as st
import soundfile as sf
import tempfile
import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

st.set_page_config(page_title="إزالة الضوضاء - ZipEnhancer", layout="centered")

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
  <h1>إزالة الضوضاء (ZipEnhancer)</h1>
  <p>نموذج من Alibaba Tongyi Lab، يزيل الضوضاء والصدى معاً.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    # تحميل pipeline من ModelScope
    ans = pipeline(
        Tasks.acoustic_noise_suppression,
        model='iic/speech_zipenhancer_ans_multiloss_16k_base',
        disable_update=True,
        disable_log=True
    )
    return ans


uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    input_path = "input_temp.wav"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        model = load_model()
        
        # استخدام مسار مؤقت آمن
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "enhanced_zipenhancer.wav")
        
        model(input_path, output_path=output_path)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_zipenhancer.wav")
