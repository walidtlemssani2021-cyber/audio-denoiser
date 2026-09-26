import streamlit as st
import torch
import numpy as np
from PIL import Image
import io
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import os

# ============================================
# ⚠️ ملاحظة: هذا النموذج يحتاج معمارية ATD
# سنستخدم مكتبة "spandrel" لتشغيله بسهولة
# ============================================

st.set_page_config(page_title="رفع جودة الصور - Nomos ATD", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000 !important; }
.hero { text-align: center; padding: 20px 10px; }
.hero h1 { color: #ffffff; font-family: 'Fraunces', serif; font-size: 32px; }
.hero p { color: #a3a3a3; font-size: 15px; }
.stDownloadButton button { background: #ffffff !important; color: #000000 !important; border-radius: 100px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>رفع جودة الصور (Nomos ATD)</h1>
  <p>نموذج قوي للصور الفوتوغرافية 4x</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    try:
        from spandrel import ModelLoader
        from spandrel.architectures.ATD import ATD
        
        # تحميل الملف من Hugging Face
        model_path = hf_hub_download(
            repo_id="Phips/4xNomosWebPhoto_atd",
            filename="4xNomosWebPhoto_atd.safetensors"
        )
        
        # تحميل الأوزان
        state_dict = load_file(model_path)
        
        # بناء النموذج عبر spandrel
        loader = ModelLoader()
        model = loader.load_from_state_dict(state_dict)
        model.eval()
        
        # تحويل إلى FP16 لتقليل الذاكرة (إذا كان CPU لا يمكن، نبقى FP32)
        if torch.cuda.is_available():
            model = model.half().cuda()
        else:
            model = model.float()
        
        return model
        
    except ImportError:
        st.error("مكتبة `spandrel` غير مثبتة. الرجاء إضافتها إلى `requirements.txt`.")
        st.stop()
    except Exception as e:
        st.error(f"خطأ في تحميل النموذج: {e}")
        st.stop()


with st.spinner("جاري تحميل النموذج..."):
    model = load_model()

uploaded_file = st.file_uploader("ارفع صورة", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة الأصلية")

    # تصغير الصورة لتقليل الذاكرة
    MAX_INPUT_SIZE = 512
    if max(image.size) > MAX_INPUT_SIZE:
        image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
        st.info(f"تم تصغير الصورة إلى {image.size} لتقليل استهلاك الذاكرة.")

    with st.spinner("جاري رفع الجودة (4x)..."):
        # تجهيز المدخلات
        img_np = np.array(image).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0)
        
        if torch.cuda.is_available():
            img_tensor = img_tensor.half().cuda()
        
        with torch.no_grad():
            output_tensor = model(img_tensor)
        
        # تحويل المخرجات
        output_tensor = output_tensor.squeeze(0).clamp(0, 1)
        output_np = (output_tensor.permute(1, 2, 0).cpu().float().numpy() * 255).astype(np.uint8)
        result_image = Image.fromarray(output_np)

    st.success("تم!")
    st.image(result_image, caption="بعد التحسين")

    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="upscaled_atd.png", mime="image/png")
