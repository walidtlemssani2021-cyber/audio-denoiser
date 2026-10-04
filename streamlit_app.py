import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER — Encrypt in Starlight",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;800;900&display=swap');

    /* ═══ Reset ═══ */
    * { box-sizing: border-box; }

    html, body, .stApp {
        background: #050507 !important;
        color: #e8e8ea;
        font-family: 'Inter', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }

    .stApp > header { display: none; }

    /* animated grid background */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(0, 255, 136, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.025) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
        mask-image: radial-gradient(ellipse 80% 60% at 50% 40%, black 20%, transparent 90%);
    }

    /* ambient glow */
    .stApp::after {
        content: '';
        position: fixed;
        top: -30%;
        left: 50%;
        transform: translateX(-50%);
        width: 120%;
        height: 80%;
        background: radial-gradient(ellipse at center, rgba(0, 255, 136, 0.10), transparent 60%);
        pointer-events: none;
        z-index: 0;
        filter: blur(80px);
    }

    .block-container {
        max-width: 1280px !important;
        padding: 2rem 3rem 6rem 3rem !important;
        position: relative;
        z-index: 1;
    }

    /* ═══ TYPOGRAPHY ═══ */
    h1, h2, h3, h4, h5 { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -0.02em; }
    p { font-family: 'Inter', sans-serif; line-height: 1.7; }

    /* ═══ NAVBAR ═══ */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 2rem;
    }
    .nav-logo {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900;
        font-size: 1.1rem;
        letter-spacing: 4px;
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }
    .nav-logo span { color: #ffffff; }
    .nav-links { display: flex; gap: 2rem; align-items: center; }
    .nav-link {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.5);
        text-decoration: none;
        transition: color 0.3s ease;
    }
    .nav-link:hover { color: #00ff88; }
    .nav-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem;
        color: #00ff88;
        letter-spacing: 2px;
    }
    .nav-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #00ff88;
        box-shadow: 0 0 10px #00ff88;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
    }

    /* ═══ HERO ═══ */
    .hero-wrap {
        padding: 5rem 0 6rem 0;
        text-align: center;
        position: relative;
    }
    .hero-eyebrow {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: rgba(0, 255, 136, 0.6);
        padding: 0.5rem 1.2rem;
        border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 100px;
        margin-bottom: 2.5rem;
    }
    .hero-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(2.5rem, 7vw, 6.5rem);
        font-weight: 900;
        letter-spacing: -0.01em;
        line-height: 1;
        margin: 0;
        background: linear-gradient(180deg, #ffffff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 40px rgba(0, 255, 136, 0.4));
    }
    .hero-title .accent {
        color: #00ff88;
        -webkit-text-fill-color: #00ff88;
        text-shadow: 0 0 40px rgba(0, 255, 136, 0.8);
    }
    .hero-tag {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.4);
        margin-top: 2rem;
    }
    .hero-desc {
        font-size: 1.05rem;
        color: rgba(255, 255, 255, 0.55);
        max-width: 620px;
        margin: 2rem auto 3rem auto;
        line-height: 1.9;
    }

    /* ═══ DIVIDER ═══ */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.4), transparent);
        margin: 0 auto;
        max-width: 700px;
    }

    /* ═══ SECTION ═══ */
    .sec {
        padding: 6rem 0;
    }
    .sec-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: rgba(0, 255, 136, 0.5);
        margin-bottom: 1.5rem;
    }
    .sec-title {
        font-size: clamp(1.8rem, 3.5vw, 2.8rem);
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.15;
        color: #ffffff;
        margin: 0 0 1rem 0;
        max-width: 700px;
    }
    .sec-title .accent {
        color: #00ff88;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
    }
    .sec-desc {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.5);
        max-width: 620px;
        line-height: 1.9;
        margin: 0 0 3.5rem 0;
    }

    /* ═══ FEATURE GRID ═══ */
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .cell {
        background: #050507;
        padding: 2.5rem 2rem;
        position: relative;
        transition: background 0.3s ease;
    }
    .cell:hover { background: rgba(0, 255, 136, 0.03); }
    .cell:hover .cell-icon { color: #00ff88; }
    .cell-num {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 2px;
        color: rgba(255, 255, 255, 0.25);
        margin-bottom: 2rem;
    }
    .cell-icon {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.4);
        margin-bottom: 1.5rem;
        transition: color 0.3s ease;
        display: block;
    }
    .cell-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    .cell-desc {
        font-size: 0.88rem;
        color: rgba(255, 255, 255, 0.45);
        line-height: 1.75;
    }

    /* ═══ STEPS ═══ */
    .step-row {
        display: grid;
        grid-template-columns: 80px 1fr;
        gap: 2rem;
        padding: 2.5rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        transition: padding 0.3s ease;
    }
    .step-row:last-child { border-bottom: 1px solid rgba(255, 255, 255, 0.06); }
    .step-row:hover { padding-left: 1rem; }
    .step-n {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 800;
        color: rgba(0, 255, 136, 0.4);
        letter-spacing: 2px;
    }
    .step-t {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .step-d {
        font-size: 0.92rem;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.8;
    }

    /* ═══ SPEC TABLE ═══ */
    .spec-table {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .spec-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #050507;
        padding: 1.2rem 1.5rem;
    }
    .spec-k {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.35);
    }
    .spec-v {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem;
        letter-spacing: 1px;
        color: #00ff88;
    }

    /* ═══ WARNING ═══ */
    .warn-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 3rem;
    }
    .warn-card {
        border: 1px solid rgba(255, 46, 99, 0.25);
        background: rgba(255, 46, 99, 0.03);
        padding: 2rem;
        border-radius: 2px;
        position: relative;
    }
    .warn-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: #ff2e63;
        box-shadow: 0 0 15px rgba(255, 46, 99, 0.6);
    }
    .warn-icon {
        font-family: 'Orbitron', sans-serif !important;
        color: #ff2e63;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        display: block;
    }
    .warn-t {
        font-size: 0.98rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.75rem;
    }
    .warn-d {
        font-size: 0.86rem;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.75;
    }

    /* ═══ CTA ═══ */
    .cta-wrap {
        padding: 6rem 3rem;
        text-align: center;
        border: 1px solid rgba(0, 255, 136, 0.2);
        background: radial-gradient(ellipse at center, rgba(0, 255, 136, 0.06), transparent 70%);
        border-radius: 4px;
        position: relative;
        overflow: hidden;
    }
    .cta-wrap::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(0, 255, 136, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.04) 1px, transparent 1px);
        background-size: 30px 30px;
        mask-image: radial-gradient(ellipse at center, black, transparent 70%);
    }
    .cta-t {
        font-size: clamp(1.5rem, 3vw, 2.4rem);
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        position: relative;
    }
    .cta-d {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.5);
        margin-bottom: 3rem;
        position: relative;
    }

    /* ═══ STREAMLIT BUTTONS ═══ */
    .stButton > button {
        background: transparent !important;
        color: #00ff88 !important;
        border: 1px solid rgba(0, 255, 136, 0.4) !important;
        border-radius: 2px !important;
        padding: 0.85rem 2rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        background: #00ff88 !important;
        color: #000000 !important;
        border-color: #00ff88 !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.5), 0 0 60px rgba(0, 255, 136, 0.2) !important;
        transform: translateY(-1px);
    }
    .stButton > button:active { transform: translateY(0); }

    /* ═══ FOOTER ═══ */
    .foot {
        margin-top: 6rem;
        padding-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.68rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.25);
        flex-wrap: wrap;
        gap: 1rem;
    }
    .foot-brand { color: rgba(0, 255, 136, 0.6); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# NAVBAR
# ═══════════════════════════════════════
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">NEUTRON<span>CIPHER</span></div>
    <div class="nav-links">
        <a class="nav-link" href="#features">Features</a>
        <a class="nav-link" href="#protocol">Protocol</a>
        <a class="nav-link" href="#specs">Specs</a>
    </div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# HERO
# ═══════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">◉ System Online — v1.0</div>
    <h1 class="hero-title">ENCRYPT<br>IN STARLIGHT.</h1>
    <p class="hero-tag">[ hide your data in the sound of a dead star ]</p>
    <p class="hero-desc">
        Neutron Cipher transforms your messages into the pulsating rhythm 
        of a neutron star. Every byte becomes a pulse. Every word becomes 
        a signal. Every secret becomes a dying star, screaming silently 
        across the void.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════
st.markdown("""
<div class="sec" id="features">
    <div class="sec-label">// capabilities</div>
    <h2 class="sec-title">Built for the <span class="accent">paranoid</span> mind.</h2>
    <p class="sec-desc">
        Every layer is designed with one purpose — to make your message 
        indistinguishable from cosmic noise.
    </p>

    <div class="grid">
        <div class="cell">
            <div class="cell-num">/ 01</div>
            <span class="cell-icon">⚡</span>
            <div class="cell-title">AES-128 Encryption</div>
            <div class="cell-desc">Military-grade encryption via Fernet protocol. Your message is locked before it ever touches the waveform.</div>
        </div>
        <div class="cell">
            <div class="cell-num">/ 02</div>
            <span class="cell-icon">🛡</span>
            <div class="cell-title">HMAC Integrity</div>
            <div class="cell-desc">Every audio file carries its own cryptographic signature. Any tampering — even a single pulse — is instantly detected.</div>
        </div>
        <div class="cell">
            <div class="cell-num">/ 03</div>
            <span class="cell-icon">✦</span>
            <div class="cell-title">Pulsar Carrier</div>
            <div class="cell-desc">Your data rides on waves modeled after the Vela Pulsar — 10.9 pulses per second, echoing across the cosmos.</div>
        </div>
        <div class="cell">
            <div class="cell-num">/ 04</div>
            <span class="cell-icon">◐</span>
            <div class="cell-title">Lossless FLAC</div>
            <div class="cell-desc">Compressed without losing a single bit. 94% smaller than WAV, yet identical in every measurable way.</div>
        </div>
        <div class="cell">
            <div class="cell-num">/ 05</div>
            <span class="cell-icon">◈</span>
            <div class="cell-title">Zero Knowledge</div>
            <div class="cell-desc">We never see your password. We never store your data. Everything happens in memory, invisible to us.</div>
        </div>
        <div class="cell">
            <div class="cell-num">/ 06</div>
            <span class="cell-icon">◍</span>
            <div class="cell-title">Universal Support</div>
            <div class="cell-desc">Arabic, English, emojis, symbols, control characters — every byte is handled with the same precision.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# PROTOCOL
# ═══════════════════════════════════════
st.markdown("""
<div class="sec" id="protocol">
    <div class="sec-label">// protocol</div>
    <h2 class="sec-title">Four layers. <span class="accent">One signal.</span></h2>
    <p class="sec-desc">
        From plain text to cosmic transmission — a transformation in four acts.
    </p>

    <div class="step-row">
        <div class="step-n">01</div>
        <div>
            <div class="step-t">Encryption</div>
            <div class="step-d">Your message is encrypted with Fernet (AES-128-CBC + HMAC-SHA256). A fresh random IV is generated for every operation — the same message produces a different ciphertext every single time.</div>
        </div>
    </div>
    <div class="step-row">
        <div class="step-n">02</div>
        <div>
            <div class="step-t">Pulse Mapping</div>
            <div class="step-d">Each encrypted byte (0–255) is translated into a specific pulse intensity. The bytes flow into a continuous stream, spaced 92 milliseconds apart — matching the rhythm of the Vela Pulsar.</div>
        </div>
    </div>
    <div class="step-row">
        <div class="step-n">03</div>
        <div>
            <div class="step-t">Waveform Synthesis</div>
            <div class="step-d">The pulses are rendered into an audio waveform at 44.1 kHz, with a sharp exponential envelope that mimics the electromagnetic signature of a real neutron star.</div>
        </div>
    </div>
    <div class="step-row">
        <div class="step-n">04</div>
        <div>
            <div class="step-t">Lossless Compression</div>
            <div class="step-d">The waveform is encoded as FLAC — a lossless format that reduces file size by up to 94% without sacrificing a single bit of data. Your message is now a star.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# SPECS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec" id="specs">
    <div class="sec-label">// technical_specs</div>
    <h2 class="sec-title">Every parameter. <span class="accent">Documented.</span></h2>
    <p class="sec-desc">
        Full transparency — the cryptographic primitives, constants, and constraints.
    </p>

    <div class="spec-table">
        <div class="spec-row"><span class="spec-k">Encryption</span><span class="spec-v">FERNET / AES-128</span></div>
        <div class="spec-row"><span class="spec-k">Integrity</span><span class="spec-v">HMAC-SHA256</span></div>
        <div class="spec-row"><span class="spec-k">Key Derivation</span><span class="spec-v">SHA-256</span></div>
        <div class="spec-row"><span class="spec-k">IV</span><span class="spec-v">RANDOM / SESSION</span></div>
        <div class="spec-row"><span class="spec-k">Carrier</span><span class="spec-v">VELA PULSAR</span></div>
        <div class="spec-row"><span class="spec-k">Pulse Rate</span><span class="spec-v">10.9 Hz</span></div>
        <div class="spec-row"><span class="spec-k">Sample Rate</span><span class="spec-v">44100 Hz</span></div>
        <div class="spec-row"><span class="spec-k">Bit Depth</span><span class="spec-v">16-BIT PCM</span></div>
        <div class="spec-row"><span class="spec-k">Codec</span><span class="spec-v">FLAC / LOSSLESS</span></div>
        <div class="spec-row"><span class="spec-k">Max Payload</span><span class="spec-v">2000 CHARS</span></div>
        <div class="spec-row"><span class="spec-k">Compression</span><span class="spec-v">~94%</span></div>
        <div class="spec-row"><span class="spec-k">Status</span><span class="spec-v">● OPERATIONAL</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# WARNINGS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec">
    <div class="sec-label">// security_notice</div>
    <h2 class="sec-title">Read <span class="accent">carefully.</span></h2>
    <p class="sec-desc">
        Neutron Cipher is built on real cryptography. That means real consequences.
    </p>

    <div class="warn-grid">
        <div class="warn-card">
            <span class="warn-icon">!</span>
            <div class="warn-t">Lost passwords cannot be recovered.</div>
            <div class="warn-d">We do not store your password. We cannot reset it. If you forget it, your message is gone — forever, and by design.</div>
        </div>
        <div class="warn-card">
            <span class="warn-icon">!</span>
            <div class="warn-t">Modified audio will not decrypt.</div>
            <div class="warn-d">Every pulse carries a cryptographic signature. Trimming, compressing, or editing the audio will cause the integrity check to fail.</div>
        </div>
        <div class="warn-card">
            <span class="warn-icon">!</span>
            <div class="warn-t">Always share the FLAC file.</div>
            <div class="warn-d">Do not convert to MP3. Do not compress. Do not re-encode. Share the original FLAC file exactly as it was produced.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# CTA
# ═══════════════════════════════════════
st.markdown("""
<div class="cta-wrap">
    <div class="cta-t">Ready to become a star?</div>
    <div class="cta-d">Choose your path below.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1.2, 1.2, 1])
with col2:
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True):
        try:
            st.switch_page("pages/encrypt.py")
        except:
            st.info("Create pages/encrypt.py to enable this.")
with col3:
    if st.button("◈  DECRYPT AUDIO", use_container_width=True):
        try:
            st.switch_page("pages/decrypt.py")
        except:
            st.info("Create pages/decrypt.py to enable this.")


# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
st.markdown("""
<div class="foot">
    <div><span class="foot-brand">NEUTRON CIPHER</span> · v1.0 · 2026</div>
    <div>ASTRONOMY × CRYPTOGRAPHY</div>
</div>
""", unsafe_allow_html=True)
