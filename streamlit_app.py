import streamlit as st
import soundfile as sf
import os
from clearvoice import ClearVoice

st.set_page_config(page_title="إزالة الضوضاء - MossFormer2", layout="centered")

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
  <h1>إزالة الضوضاء (MossFormer2)</h1>
  <p>نموذج قوي لإزالة الضوضاء بجودة عالية (48kHz).</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    myClearVoice = ClearVoice(
        task='speech_enhancement',
        model_names=['MossFormer2_SE_48K']
    )
    return myClearVoice


uploaded_file = st.file_uploader(
    "ارفع ملف صوتي (WAV أو FLAC)",
    type=["wav", "flac"],
)

if uploaded_file is not None:
    input_path = "input_temp." + uploaded_file.name.split(".")[-1]
    output_path = "enhanced_mossformer2.wav"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء... (قد يستغرق وقتاً أطول)"):
        myClearVoice = load_model()

        output_wav = myClearVoice(
            input_path=input_path,
            online_write=False
        )

        myClearVoice.write(output_wav, output_path=output_path)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_mossformer2.wav",
        )
