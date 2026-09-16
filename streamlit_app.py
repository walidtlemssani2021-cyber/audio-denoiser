import streamlit as st
import soundfile as sf
from clearvoice import ClearVoice

st.set_page_config(page_title="إزالة الضوضاء - FRCRN", layout="centered")

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
  <h1>إزالة الضوضاء (FRCRN)</h1>
  <p>نموذج سريع وخفيف، مناسب للمعالجة السريعة على المعالج.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    # استخدام FRCRN_SE_16K
    myClearVoice = ClearVoice(
        task='speech_enhancement',
        model_names=['FRCRN_SE_16K']
    )
    return myClearVoice


uploaded_file = st.file_uploader(
    "ارفع ملف صوتي (WAV أو FLAC)",
    type=["wav", "flac"],
)

if uploaded_file is not None:
    input_path = "input_temp." + uploaded_file.name.split(".")[-1]
    output_path = "enhanced_frcrn.wav"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        myClearVoice = load_model()

        # المعالجة
        output_wav = myClearVoice(
            input_path=input_path,
            online_write=False
        )

        # حفظ النتيجة
        myClearVoice.write(output_wav, output_path=output_path)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_frcrn.wav",
        )
