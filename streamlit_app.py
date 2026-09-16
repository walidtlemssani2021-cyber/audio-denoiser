import os
import streamlit as st
import soundfile as sf
from voicefixer import VoiceFixer

st.set_page_config(page_title="ترميم الصوت - VoiceFixer", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: #000000 !important;
    font-family: 'Inter', sans-serif;
}

.hero {
    text-align: center;
    padding: 20px 10px 10px;
}
.hero .mark {
    font-family: 'Fraunces', serif;
    color: #ffffff;
    opacity: 0.75;
    font-size: 14px;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 32px;
    color: #ffffff;
    margin: 6px 0 14px;
}
.hero p {
    color: #a3a3a3;
    font-size: 15px;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(160deg, #3fa0f5, #0a2a6b);
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.15);
}
[data-testid="stFileUploader"] * {
    color: #eaf3ff !important;
}

.stDownloadButton button, .stButton button {
    background: #ffffff !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 100px !important;
    font-weight: 600 !important;
    box-shadow: 0 0 28px rgba(255,255,255,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="mark">UMBRA AUDIO</div>
  <h1>رمّم صوتك بالكامل</h1>
  <p>ارفع أي تسجيل، والنموذج (VoiceFixer) يزيل الضوضاء والصدى ويرفع الجودة تلقائياً.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    vf = VoiceFixer()
    return vf


with st.spinner("جاري تحميل النموذج..."):
    vf = load_model()

uploaded_file = st.file_uploader(
    "ارفع ملف صوتي",
    type=["wav", "flac"],
)

mode = st.selectbox(
    "اختر وضع المعالجة",
    options=[0, 1, 2],
    index=0,
    help="0 = الأسرع، 2 = الأعمق والأبطأ",
)

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    output_path = "voicefixer_output.wav"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري ترميم الصوت... (قد يستغرق بعض الوقت)"):
        vf.restore(
            input=input_path,
            output=output_path,
            cuda=False,
            mode=mode,
        )

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف بعد الترميم",
            f,
            file_name="voicefixer_restored.wav",
        )
