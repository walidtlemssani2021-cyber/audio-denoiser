import io
import streamlit as st
from PIL import Image
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from rembg import remove, new_session

st.set_page_config(page_title="PIXLY — AI Photo Tools", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

:root {
  --bg: #05050a;
  --surface: #0e0e16;
  --border: #202028;
  --text: #f5f5f7;
  --muted: #8a8a98;
  --accent-a: #4de8ff;
  --accent-b: #c24dff;
}

html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }

.stApp {
  background-color: var(--bg) !important;
  background-image:
    radial-gradient(circle at 15% 0%, rgba(77,232,255,0.14), transparent 42%),
    radial-gradient(circle at 85% 8%, rgba(194,77,255,0.14), transparent 42%);
}

.hero { text-align: center; padding: 40px 10px 8px; }

.hero .wordmark {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: 15px;
  letter-spacing: 5px;
  color: var(--text);
  margin-bottom: 20px;
}

.hero .chip {
  display: inline-block;
  padding: 6px 18px;
  border: 1px solid var(--border);
  border-radius: 100px;
  font-size: 12px;
  color: var(--muted);
  background: rgba(255,255,255,0.03);
  margin-bottom: 26px;
}

.hero h1 {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: 38px;
  line-height: 1.18;
  color: var(--text);
  margin: 0;
}

.hero h1 .accent {
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero p {
  color: var(--muted);
  font-size: 15px;
  margin: 18px auto 0;
  max-width: 380px;
}

div[role="radiogroup"] { justify-content: center; gap: 10px; margin-top: 30px; }

div[role="radiogroup"] label {
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 6px 18px;
  background: var(--surface);
}

div[data-testid="stFileUploader"] {
  border: 1px dashed var(--border);
  border-radius: 16px;
  padding: 4px;
  background: var(--surface);
}

.stDownloadButton button {
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b)) !important;
  color: #05050a !important;
  border: none !important;
  border-radius: 100px !important;
  font-weight: 600 !important;
  box-shadow: 0 0 22px rgba(194,77,255,0.35);
}

button[kind="primary"] {
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b)) !important;
  color: #05050a !important;
  border: none !important;
  border-radius: 100px !important;
  font-weight: 600 !important;
  box-shadow: 0 0 22px rgba(194,77,255,0.35);
  width: 100%;
}

button[kind="secondary"] {
  background: rgba(194,77,255,0.10) !important;
  color: var(--accent-b) !important;
  border: 1px solid var(--accent-b) !important;
  border-radius: 100px !important;
  width: 100%;
}

.back-link { color: var(--muted); font-size: 14px; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"


def go_to(page_name):
    st.session_state.page = page_name


@st.cache_resource
def load_upscale_model():
    model_path = hf_hub_download(
        repo_id="Heliosoph/realesrgan-onnx",
        filename="realesr-general-x4v3.onnx"
    )
    return ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])


@st.cache_resource
def load_rembg_session():
    return new_session("u2net")


# ==================== HOME PAGE ====================
if st.session_state.page == "home":
    load_upscale_model.clear()  # no tool selected yet, keep memory free
    load_rembg_session.clear()

    st.markdown("""
    <div class="hero">
      <div class="wordmark">PIXLY</div>
      <div class="chip">Powered by open-source AI models</div>
      <h1>Sharper photos,<br><span class="accent">cleaner cutouts.</span></h1>
      <p>Upload a photo. Pixly upscales the details or removes the background in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("Upscale Photo", type="primary", use_container_width=True):
        go_to("upscale")
        st.rerun()

    st.write("")
    if st.button("Remove Background", type="secondary", use_container_width=True):
        go_to("remove_bg")
        st.rerun()

# ==================== UPSCALE PAGE ====================
elif st.session_state.page == "upscale":
    if st.button("← Back", type="secondary"):
        go_to("home")
        st.rerun()

    load_rembg_session.clear()

    with st.spinner("Loading model..."):
        session = load_upscale_model()

    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg", "webp"], key="upscale_uploader")

    if uploaded_file is not None:
        file_key = f"upscale_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("upscale_key") != file_key:
            image = Image.open(uploaded_file).convert("RGB")

            MAX_INPUT_SIZE = 800
            if max(image.size) > MAX_INPUT_SIZE:
                image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
                st.info(f"Resized to {image.size} to reduce memory usage.")

            with st.spinner("Upscaling..."):
                img_array = np.asarray(image, dtype=np.float32) / 255.0
                img_array = img_array.transpose(2, 0, 1)[None, ...]

                output = session.run(None, {"input": img_array})[0][0]

                output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
                result_image = Image.fromarray(output)

            st.session_state.upscale_key = file_key
            st.session_state.upscale_original = image
            st.session_state.upscale_result = result_image

        image = st.session_state.upscale_original
        result_image = st.session_state.upscale_result

        st.image(image, caption="Original")
        st.success("Done!")
        st.image(result_image, caption="Upscaled")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("Download", buf.getvalue(), file_name="upscaled.png", mime="image/png")

# ==================== REMOVE BACKGROUND PAGE ====================
else:
    if st.button("← Back", type="secondary"):
        go_to("home")
        st.rerun()

    with st.spinner("Loading models..."):
        rembg_session = load_rembg_session()
        upscale_session = load_upscale_model()

    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg", "webp"], key="rembg_uploader")

    if uploaded_file is not None:
        file_key = f"rembg_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("rembg_key") != file_key:
            image = Image.open(uploaded_file).convert("RGB")

            MAX_BG_INPUT_SIZE = 2000
            if max(image.size) > MAX_BG_INPUT_SIZE:
                image.thumbnail((MAX_BG_INPUT_SIZE, MAX_BG_INPUT_SIZE), Image.LANCZOS)
                st.info(f"Resized to {image.size} to reduce memory usage.")

            with st.spinner("Removing background..."):
                no_bg_image = remove(image, session=rembg_session)  # RGBA

            # Split alpha (transparency) from RGB, since the upscale model only accepts 3 channels
            rgb_part = no_bg_image.convert("RGB")
            alpha_part = no_bg_image.split()[-1]

            MAX_UPSCALE_INPUT_SIZE = 800
            if max(rgb_part.size) > MAX_UPSCALE_INPUT_SIZE:
                rgb_part.thumbnail((MAX_UPSCALE_INPUT_SIZE, MAX_UPSCALE_INPUT_SIZE), Image.LANCZOS)
                alpha_part = alpha_part.resize(rgb_part.size, Image.LANCZOS)
                st.info(f"Resized to {rgb_part.size} before upscaling to reduce memory usage.")

            with st.spinner("Upscaling result..."):
                img_array = np.asarray(rgb_part, dtype=np.float32) / 255.0
                img_array = img_array.transpose(2, 0, 1)[None, ...]

                output = upscale_session.run(None, {"input": img_array})[0][0]

                output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
                upscaled_rgb = Image.fromarray(output)

                # Resize alpha channel to match the upscaled size
                upscaled_alpha = alpha_part.resize(upscaled_rgb.size, Image.LANCZOS)
                result_image = Image.merge("RGBA", (*upscaled_rgb.split(), upscaled_alpha))

            st.session_state.rembg_key = file_key
            st.session_state.rembg_original = image
            st.session_state.rembg_result = result_image

        image = st.session_state.rembg_original
        result_image = st.session_state.rembg_result

        st.image(image, caption="Original")
        st.success("Done!")
        st.image(result_image, caption="Background removed + upscaled")

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        st.download_button("Download", buf.getvalue(), file_name="no_background_upscaled.png", mime="image/png")
