import io
import streamlit as st
from PIL import Image
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from rembg import remove, new_session

# ==================== إعدادات الأمان ====================
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_INPUT_PIXELS = 25_000_000
ALLOWED_FORMATS = {"PNG", "JPEG", "WEBP"}

ALLOWED_SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"RIFF": "WEBP",
}

st.set_page_config(
    page_title="PIXLY | AI Photo Tools",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def validate_uploaded_file(uploaded_file):
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds {MAX_FILE_SIZE_MB}MB."
    if uploaded_file.size == 0:
        return False, "Empty file."

    header = uploaded_file.read(16)
    uploaded_file.seek(0)

    if not header:
        return False, "Cannot read file."

    sig_ok = any(header.startswith(s) for s in ALLOWED_SIGNATURES)
    if header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        sig_ok = True
    elif header.startswith(b"RIFF"):
        sig_ok = False

    if not sig_ok:
        return False, "File type not allowed."

    try:
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        img.verify()

        uploaded_file.seek(0)
        img = Image.open(uploaded_file)

        if img.format not in ALLOWED_FORMATS:
            return False, f"Format not allowed: {img.format}"

        w, h = img.size
        if w * h > MAX_INPUT_PIXELS:
            return False, f"Image too large ({w}x{h})."
        if w < 8 or h < 8:
            return False, "Image too small."
    except Exception:
        return False, "Corrupted or invalid image."

    uploaded_file.seek(0)
    return True, "ok"


def safe_open_image(uploaded_file):
    try:
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        img.load()
        return img
    except Exception:
        return None


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
  max-width: 92%;
  padding: 8px 18px;
  border: 1px solid var(--border);
  border-radius: 18px;
  font-size: 12px;
  line-height: 1.5;
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
  transition: box-shadow 1.8s ease-in 0.5s;
}

button[kind="secondary"] {
  background: rgba(194,77,255,0.10) !important;
  color: var(--accent-b) !important;
  border: 1px solid var(--accent-b) !important;
  border-radius: 100px !important;
  width: 100%;
  box-shadow: 0 0 0 rgba(194,77,255,0);
  transition: box-shadow 1.8s ease-in 0.5s;
}

.stApp:has(.floating-start-btn:active) button[kind="primary"] {
  box-shadow: 0 0 55px 10px rgba(77,232,255,0.85) !important;
  transition: none;
}
.stApp:has(.floating-start-btn:active) button[kind="secondary"] {
  box-shadow: 0 0 55px 10px rgba(194,77,255,0.9) !important;
  transition: none;
}

.back-link { color: var(--muted); font-size: 14px; }

.section-title {
  font-family: 'Fraunces', serif;
  font-weight: 700;
  font-size: 27px;
  color: var(--text);
  text-align: center;
  margin: 64px 0 24px;
}

.steps { display: flex; flex-direction: column; gap: 12px; margin-bottom: 8px; }
.step {
  display: flex; align-items: flex-start; gap: 14px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 16px;
}
.step-num {
  flex-shrink: 0; width: 26px; height: 26px; border-radius: 100px;
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
  color: #05050a; font-weight: 600; font-size: 12px;
  display: flex; align-items: center; justify-content: center;
}
.step-text { color: var(--text); font-size: 14px; line-height: 1.5; }
.step-text .step-sub { color: var(--muted); font-size: 12px; display: block; margin-top: 2px; }

.features { display: flex; flex-direction: column; gap: 14px; }
.feature-card {
  display: flex; align-items: flex-start; gap: 16px;
  border: 1px solid var(--border); border-radius: 14px;
  padding: 20px; background: var(--surface);
  border-left: 3px solid var(--feature-color);
}
.feature-card.upscale { --feature-color: var(--accent-a); }
.feature-card.removebg { --feature-color: var(--accent-b); }
.feature-icon {
  flex-shrink: 0; width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; font-weight: 700;
  background: var(--feature-color);
  color: #05050a;
}
.feature-content h3 { font-family: 'Fraunces', serif; font-size: 16px; color: var(--text); margin: 0 0 6px; }
.feature-content p { color: var(--muted); font-size: 13px; margin: 0; line-height: 1.5; }

.footer-credit {
  text-align: center; color: var(--muted); font-size: 12px;
  padding: 46px 10px 36px; border-top: 1px solid var(--border); margin-top: 40px;
}

.section-title-large {
  font-family: 'Fraunces', serif;
  font-weight: 700;
  font-size: 27px;
  color: var(--text);
  text-align: center;
  margin: 44px 0 20px;
}

.intro-card {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 22px 22px;
  background: linear-gradient(180deg, rgba(77,232,255,0.06), rgba(194,77,255,0.06)), var(--surface);
  box-shadow: 0 0 30px rgba(194,77,255,0.10);
}
.intro-card p {
  color: var(--text);
  font-size: 15px;
  line-height: 1.8;
  margin: 0;
}
.intro-card strong { color: var(--accent-a); font-weight: 600; }

.specs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stat-tile {
  position: relative; overflow: hidden;
  border: 1px solid var(--border); border-radius: 14px;
  padding: 16px; background: var(--surface);
}
.stat-tile::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
}
.stat-tile .stat-value { font-family: 'Fraunces', serif; font-weight: 600; font-size: 19px; color: var(--text); }
.stat-tile .stat-label { font-size: 12px; color: var(--muted); margin-top: 4px; }
.stat-tile.wide { grid-column: 1 / -1; }
.stat-tile.wide .stat-value { font-size: 15px; }

.privacy-card {
  border-left: 3px solid var(--accent-a); border-radius: 10px;
  background: var(--surface); padding: 18px 20px;
}
.privacy-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px; }
.privacy-list li { display: flex; align-items: flex-start; gap: 10px; color: var(--muted); font-size: 13px; line-height: 1.5; }
.privacy-list li .check { color: var(--accent-a); font-weight: 700; flex-shrink: 0; }

.faq { display: flex; flex-direction: column; gap: 10px; }
details.faq-item {
  border: 1px solid var(--border); border-radius: 12px;
  background: var(--surface); padding: 0 18px;
}
details.faq-item summary {
  list-style: none; cursor: pointer; padding: 14px 0;
  font-size: 14px; font-weight: 600; color: var(--text);
  display: flex; justify-content: space-between; align-items: center;
}
details.faq-item summary::-webkit-details-marker { display: none; }
details.faq-item summary::after {
  content: '+'; font-size: 18px; color: var(--accent-a);
  transition: transform 0.2s ease; margin-left: 12px; flex-shrink: 0;
}
details.faq-item[open] summary::after { transform: rotate(45deg); }
details.faq-item p { color: var(--muted); font-size: 13px; line-height: 1.5; padding: 0 0 16px; margin: 0; }

html { scroll-behavior: smooth; }

.floating-start-btn {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  z-index: 999;
  display: inline-block;
  padding: 14px 32px;
  border-radius: 100px;
  background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
  color: #05050a !important;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  box-shadow: 0 0 24px rgba(194,77,255,0.45);
}
.bottom-spacer { height: 90px; }
</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "home"


def go_to(page_name):
    st.session_state.page = page_name


# ملاحظة: try/except صارت خارج الدوال المخزّنة بالكاش، عشان فشل مؤقت
# (مثلاً مشكلة شبكة) ما ينحفظ بالكاش ويترجع لكل الزوار الجايين بعده.
@st.cache_resource(show_spinner=False)
def load_upscale_model():
    model_path = hf_hub_download(
        repo_id="Heliosoph/realesrgan-onnx",
        filename="realesr-general-x4v3.onnx",
    )
    return ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],
    )


@st.cache_resource(show_spinner=False)
def load_rembg_session():
    return new_session("u2net")


# ==================== الصفحة الرئيسية ====================
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero" id="top">
      <div class="wordmark">PIXLY</div>
      <div class="chip">Notice: the site is currently in beta and is not running at full capacity</div>
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

    st.markdown("""
    <div class="section-title-large">What is Pixly?</div>
    <div class="intro-card">
      <p>Pixly is a recently launched website dedicated to photo editing. It currently offers two options: the first is <strong>upscaling photo quality</strong>, and the second is <strong>removing photo backgrounds</strong>. Both are powered by two AI models, Real-ESRGAN and U²-Net.</p>
    </div>

    <div class="section-title">What Pixly does</div>
    <div class="features">
      <div class="feature-card upscale">
        <div class="feature-icon">4×</div>
        <div class="feature-content">
          <h3>Upscale Photo</h3>
          <p>Increases resolution up to 4x and recovers sharper detail using Real-ESRGAN.</p>
        </div>
      </div>
      <div class="feature-card removebg">
        <div class="feature-icon">✂</div>
        <div class="feature-content">
          <h3>Remove Background</h3>
          <p>Isolates the subject into a transparent PNG using U²-Net, then sharpens the result automatically.</p>
        </div>
      </div>
    </div>

    <div class="section-title">How it works</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-text">Upload a photo<span class="step-sub">PNG, JPG, or WEBP (max 10MB)</span></div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-text">Pixly processes it<span class="step-sub">Upscaling or background removal in seconds</span></div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-text">Download the result<span class="step-sub">Full-resolution PNG</span></div>
      </div>
    </div>

    <div class="section-title">Privacy</div>
    <div class="privacy-card">
      <ul class="privacy-list">
        <li><span class="check">✓</span> Processed only for the duration of your session</li>
        <li><span class="check">✓</span> Not saved to disk or any database — processed in memory only</li>
        <li><span class="check">✓</span> Never shared with third parties or used to train any model</li>
      </ul>
    </div>

    <div class="section-title">FAQ</div>
    <div class="faq">
      <details class="faq-item">
        <summary>Is Pixly free?</summary>
        <p>Yes. Pixly is free to use and built entirely on open-source AI models.</p>
      </details>
      <details class="faq-item">
        <summary>What image formats are supported?</summary>
        <p>PNG, JPG, JPEG, and WEBP.</p>
      </details>
      <details class="faq-item">
        <summary>Is there a file size limit?</summary>
        <p>Yes, up to 10MB per photo. Larger photos are automatically resized before processing to keep things fast.</p>
      </details>
      <details class="faq-item">
        <summary>Are my photos stored?</summary>
        <p>No. Photos are processed in memory for your session only, not saved to disk or any database.</p>
      </details>
    </div>

    <div class="footer-credit">
      © 2026 PIXLY. All rights reserved.
    </div>

    <div class="bottom-spacer"></div>

    <a href="#top" class="floating-start-btn">Let's start</a>
    """, unsafe_allow_html=True)


# ==================== صفحة التكبير ====================
elif st.session_state.page == "upscale":
    if st.button("← Back", type="secondary"):
        go_to("home")
        st.rerun()

    try:
        with st.spinner("Loading model..."):
            session = load_upscale_model()
    except Exception:
        st.error("Failed to load the upscale model. Please try again shortly.")
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload a photo",
        type=["png", "jpg", "jpeg", "webp"],
        key="upscale_uploader",
        help=f"Max {MAX_FILE_SIZE_MB}MB",
    )

    if uploaded_file is not None:
        ok, msg = validate_uploaded_file(uploaded_file)
        if not ok:
            st.error(msg)
            st.stop()

        file_key = f"upscale_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("upscale_key") != file_key:
            image = safe_open_image(uploaded_file)
            if image is None:
                st.error("Cannot open image.")
                st.stop()

            image = image.convert("RGB")

            MAX_INPUT_SIZE = 800
            if max(image.size) > MAX_INPUT_SIZE:
                image.thumbnail((MAX_INPUT_SIZE, MAX_INPUT_SIZE), Image.LANCZOS)
                st.info(f"Resized to {image.size} to reduce memory usage.")

            try:
                with st.spinner("Upscaling..."):
                    img_array = np.asarray(image, dtype=np.float32) / 255.0
                    img_array = img_array.transpose(2, 0, 1)[None, ...]

                    output = session.run(None, {"input": img_array})[0][0]

                    output = (output.transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8)
                    result_image = Image.fromarray(output)
            except Exception:
                st.error("Error while processing the image.")
                st.stop()

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


# ==================== صفحة إزالة الخلفية ====================
else:
    if st.button("← Back", type="secondary"):
        go_to("home")
        st.rerun()

    try:
        with st.spinner("Loading models..."):
            rembg_session = load_rembg_session()
            upscale_session = load_upscale_model()
    except Exception:
        st.error("Failed to load the AI models. Please try again shortly.")
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload a photo",
        type=["png", "jpg", "jpeg", "webp"],
        key="rembg_uploader",
        help=f"Max {MAX_FILE_SIZE_MB}MB",
    )

    if uploaded_file is not None:
        ok, msg = validate_uploaded_file(uploaded_file)
        if not ok:
            st.error(msg)
            st.stop()

        file_key = f"rembg_{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.get("rembg_key") != file_key:
            image = safe_open_image(uploaded_file)
            if image is None:
                st.error("Cannot open image.")
                st.stop()

            image = image.convert("RGB")

            MAX_BG_INPUT_SIZE = 2000
            if max(image.size) > MAX_BG_INPUT_SIZE:
                image.thumbnail((MAX_BG_INPUT_SIZE, MAX_BG_INPUT_SIZE), Image.LANCZOS)
                st.info(f"Resized to {image.size} to reduce memory usage.")

            try:
                with st.spinner("Removing background..."):
                    no_bg_image = remove(image, session=rembg_session)

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

                    upscaled_alpha = alpha_part.resize(upscaled_rgb.size, Image.LANCZOS)
                    result_image = Image.merge("RGBA", (*upscaled_rgb.split(), upscaled_alpha))
            except Exception:
                st.error("Error while processing the image.")
                st.stop()

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
