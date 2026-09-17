import streamlit as st
import torch
import soundfile as sf
import numpy as np
from denoiser import pretrained
from denoiser.dsp import convert_audio
import onnxruntime as ort
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="تنقية ورفع جودة الصوت", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>نظّف صوتك وارفع جودته</h1><p>DNS64 + FlashSR (ONNX)</p></div>', unsafe_allow_html=True)

@st.cache_resource
def load_dns_model():
    model = pretrained.dns64()
    model.eval()
    return model

@st.cache_resource
def load_sr_model():
    model_path = hf_hub_download(repo_id="YatharthS/FlashSR", filename="model.onnx", subfolder="onnx")
    return ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])

with st.spinner("جاري تحميل النماذج..."):
    dns_model = load_dns_model()
    sr_session = load_sr_model()

uploaded_file = st.file_uploader("ارفع ملف صوتي فيه ضوضاء", type=["wav", "flac"])

if uploaded_file is not None:
    input_path = "input_audio." + uploaded_file.name.split(".")[-1]
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري المعالجة..."):
        wav_np, sr = sf.read(input_path, dtype="float32")
        wav = torch.from_numpy(wav_np).float()
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        else:
            wav = wav.T

        wav = convert_audio(wav, sr, dns_model.sample_rate, dns_model.chin)
        with torch.no_grad():
            denoised = dns_model(wav.unsqueeze(0))[0]

        audio = denoised.squeeze(0).cpu().numpy()
        sr = dns_model.sample_rate

        # FlashSR ONNX
        if sr != 16000:
            import librosa
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
            sr = 16000

        audio_input = audio[np.newaxis, :].astype(np.float32)
        onnx_output = sr_session.run(["reconstruction"], {"audio_values": audio_input})[0]
        enhanced = onnx_output.squeeze(0)

        output_path = "enhanced_flashsr.wav"
        sf.write(output_path, enhanced, 48000)

    st.success("تم!")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button("تحميل الملف", f, file_name="enhanced_flashsr.wav")
