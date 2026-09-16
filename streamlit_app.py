import streamlit as st
import soundfile as sf
import dpdfnet

st.set_page_config(page_title="إزالة الضوضاء - DPDFNet", layout="centered")

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
  <h1>إزالة الضوضاء (DPDFNet)</h1>
  <p>نموذج خفيف يعمل على المعالج بكفاءة، ويدعم ملفات 48kHz.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    dpdfnet.download("dpdfnet2_48khz_hr")
    return "dpdfnet2_48khz_hr"


uploaded_file = st.file_uploader(
    "ارفع ملف صوتي (WAV أو FLAC)",
    type=["wav", "flac"],
)

if uploaded_file is not None:
    input_path = "input_temp." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        model_name = load_model()
        audio, sr = sf.read(input_path)
        enhanced = dpdfnet.enhance(audio, sample_rate=sr, model=model_name)

        output_path = "enhanced_dpdfnet.wav"
        sf.write(output_path, enhanced, sr)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_dpdfnet.wav",
        )
