import streamlit as st
import soundfile as sf
import torch
import os
from df.enhance import enhance, init_df, load_audio

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
  <p>نموذج خفيف وسريع، مصمم للعمل على المعالج.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    # تحميل DeepFilterNet3 (الأحدث والأفضل)
    model, df_state, _ = init_df(model_base_dir="DeepFilterNet3")
    return model, df_state


uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV أو FLAC)", type=["wav", "flac"])

if uploaded_file is not None:
    input_path = "input_temp." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        model, df_state = load_model()
        # تحميل الصوت
        audio, _ = load_audio(input_path, sr=df_state.sr())
        # إزالة الضوضاء
        enhanced = enhance(model, df_state, audio)
        # حفظ النتيجة
        output_path = "enhanced_deepfilternet.wav"
        sf.write(output_path, enhanced.squeeze().cpu().numpy(), df_state.sr())

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_deepfilternet.wav",
        )
