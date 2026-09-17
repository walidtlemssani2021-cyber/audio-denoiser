import streamlit as st
import soundfile as sf
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
import librosa

st.set_page_config(page_title="رفع جودة الصوت - FlashSR", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>ارفع جودة صوتك</h1><p>FlashSR (ONNX) من 16kHz إلى 48kHz</p></div>', unsafe_allow_html=True)


@st.cache_resource
def load_sr_model():
    model_path = hf_hub_download(
        repo_id="YatharthS/FlashSR",
        filename="model.onnx",
        subfolder="onnx"
    )
    return ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])


with st.spinner("جاري تحميل النموذج..."):
    sr_session = load_sr_model()

uploaded_file = st.file_uploader("ارفع ملف صوتي", type=["wav", "flac"])

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري رفع الجودة..."):
        # قراءة الصوت
        audio, sr = sf.read(input_path, dtype="float32")

        # تحويل إلى mono إذا كان stereo
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # FlashSR يتوقع 16kHz
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
            sr = 16000

        # تجهيز المدخلات
        audio_input = audio[np.newaxis, :].astype(np.float32)

        # تشغيل النموذج
        input_name = sr_session.get_inputs()[0].name
        output_name = sr_session.get_outputs()[0].name
        onnx_output = sr_session.run([output_name], {input_name: audio_input})[0]

        enhanced = onnx_output.squeeze(0)

        output_path = "enhanced_flashsr.wav"
        sf.write(output_path, enhanced, 48000)

    st.success("تم!")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_flashsr.wav")
