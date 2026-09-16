import streamlit as st
import torch
import librosa
import soundfile as sf
import numpy as np
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
  <p>نموذج قوي يعالج الطور والاتساع معاً، بمتطلبات خفيفة نسبياً.</p>
</div>
""", unsafe_allow_html=True)

# ملاحظة: هذا الكود يفترض وجود ملف النموذج المدرب مسبقاً في المستودع
# سنحتاج إلى تحميله من مكان ما أو تدريبه لاحقاً
MODEL_PATH = "dccrn_model.pth"

@st.cache_resource
def load_model():
    # في هذا المثال، سنفترض أن النموذج موجود كملف .pth
    # لكن في الواقع، DCCRN يحتاج إلى تعريف بنية الشبكة أولاً
    # سنستخدم مكتبة أو كود جاهز لتحميله
    from models.dccrn_model import DCCRN  # نحتاج لإنشاء هذا الملف لاحقاً
    
    model = DCCRN()
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()
    return model

uploaded_file = st.file_uploader("ارفع ملف صوتي (WAV)", type=["wav"])

if uploaded_file is not None:
    # حفظ الملف المؤقت
    input_path = "input_temp.wav"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("جاري إزالة الضوضاء..."):
        # تحميل الصوت (16kHz)
        audio, sr = librosa.load(input_path, sr=16000, mono=True)
        
        # تحويل إلى Tensor
        audio_tensor = torch.from_numpy(audio).float().unsqueeze(0)
        
        # تشغيل النموذج
        model = load_model()
        with torch.no_grad():
            enhanced = model(audio_tensor)
        
        # حفظ النتيجة
        enhanced_np = enhanced.squeeze().cpu().numpy()
        output_path = "enhanced_dccrn.wav"
        sf.write(output_path, enhanced_np, 16000)

    st.success("تم! استمع للنتيجة أو حمّلها.")
    st.audio(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            "تحميل الملف",
            f,
            file_name="enhanced_dccrn.wav",
        )
