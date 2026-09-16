import streamlit as st
from df.enhance import enhance, init_df, load_audio, save_audio

st.set_page_config(page_title="إزالة الضوضاء الصوتية", layout="centered")

st.markdown("<style>.stApp{background:#000;font-family:sans-serif;} h1{color:#fff;text-align:center;} p{color:#aaa;text-align:center;} [data-testid='stFileUploader']{background:linear-gradient(160deg,#3fa0f5,#0a2a6b);border-radius:14px;padding:14px;} [data-testid='stFileUploader'] *{color:#eaf3ff !important;} .stDownloadButton button{background:#fff !important;color:#000 !important;border-radius:100px !important;font-weight:600 !important;}</style>", unsafe_allow_html=True)

st.markdown("<h1>نظّف صوتك من الضوضاء</h1>", unsafe_allow_html=True)
st.markdown("<p>ارفع أي تسجيل صوتي، والنموذج (DeepFilterNet) يزيل الضوضاء تلقائياً.</p>", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model, df_state, _ = init_df()
    return model, df_state


with st.spinner("جاري تحميل النموذج..."):
    model, df_state = load_model()

uploaded_file = st.file_uploader("ارفع ملف صوتي فيه ضوضاء", type=["wav", "mp3", "flac", "ogg"])

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        audio, _ = load_audio(input_path, sr=df_state.sr())
        enhanced = enhance(model, df_state, audio)
        output_path = "denoised_output.wav"
        save_audio(output_path, enhanced, df_state.sr())

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف بعد التنقية", f, file_name="denoised.wav")
