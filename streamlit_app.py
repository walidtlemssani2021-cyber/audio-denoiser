import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════
# CSS
# ═══════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;800&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;800;900&display=swap');

    * { font-family: 'JetBrains Mono', monospace !important; }

    .stApp {
        background: #000000;
        background-image:
            radial-gradient(ellipse at top, rgba(0, 255, 136, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(0, 150, 255, 0.04) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 136, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.025) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #00ff88;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ═══ HERO ═══ */
    .hero {
        min-height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
        padding: 4rem 2rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border: 1px solid rgba(0, 255, 136, 0.4);
        color: #00ff88;
        font-size: 0.7rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        opacity: 0.8;
    }

    .hero-badge::before { content: '◉ '; animation: pulse 2s infinite; }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .cyber-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(3rem, 9vw, 8rem);
        font-weight: 900;
        color: #00ff88;
        text-shadow:
            0 0 10px #00ff88,
            0 0 30px #00ff88,
            0 0 60px rgba(0, 255, 136, 0.6),
            0 0 100px rgba(0, 255, 136, 0.3);
        letter-spacing: 10px;
        line-height: 1;
        margin: 0;
        animation: flicker 4s infinite alternate;
    }

    @keyframes flicker {
        0%, 100% { opacity: 1; }
        93% { opacity: 1; }
        94% { opacity: 0.6; }
        95% { opacity: 1; }
        97% { opacity: 0.8; }
        98% { opacity: 1; }
    }

    .hero-subtitle {
        font-size: clamp(0.9rem, 1.5vw, 1.1rem);
        color: rgba(0, 255, 136, 0.7);
        letter-spacing: 6px;
        text-transform: uppercase;
        margin: 2rem 0;
        max-width: 800px;
        line-height: 1.8;
    }

    .hero-desc {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem;
        color: rgba(255, 255, 255, 0.5);
        max-width: 700px;
        line-height: 1.9;
        margin: 2rem auto;
    }

    .cyber-line {
        width: 80%;
        height: 1px;
        margin: 2rem auto;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        box-shadow: 0 0 15px #00ff88;
    }

    /* ═══ SECTIONS ═══ */
    .section {
        padding: 6rem 2rem;
        max-width: 1300px;
        margin: 0 auto;
    }

    .section-label {
        font-size: 0.7rem;
        color: rgba(0, 255, 136, 0.5);
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .section-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 3px;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .section-title span { color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.6); }

    .section-desc {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.5);
        max-width: 700px;
        line-height: 1.9;
        margin-bottom: 3rem;
    }

    /* ═══ FEATURE CARDS ═══ */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 3rem;
    }

    .feature-card {
        background: rgba(0, 10, 5, 0.6);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 2px;
        padding: 2rem;
        position: relative;
        transition: all 0.4s ease;
    }

    .feature-card:hover {
        border-color: #00ff88;
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 40px; height: 2px;
        background: #00ff88;
    }

    .feature-num {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 3rem;
        font-weight: 900;
        color: rgba(0, 255, 136, 0.15);
        position: absolute;
        top: 1rem;
        right: 1.5rem;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
    }

    .feature-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1rem;
        font-weight: 700;
        color: #00ff88;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .feature-desc {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        line-height: 1.8;
    }

    /* ═══ STEPS ═══ */
    .step {
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
        padding: 2rem;
        background: rgba(0, 10, 5, 0.4);
        border-left: 2px solid rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }

    .step:hover {
        border-left-color: #00ff88;
        background: rgba(0, 255, 136, 0.03);
    }

    .step-num {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.5rem;
        font-weight: 900;
        color: #00ff88;
        min-width: 80px;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }

    .step-content h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: #ffffff;
        letter-spacing: 2px;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .step-content p {
        font-family: 'Inter', sans-serif !important;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        line-height: 1.8;
    }

    /* ═══ SPECS TABLE ═══ */
    .specs {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }

    .spec-item {
        display: flex;
        justify-content: space-between;
        padding: 1rem 1.5rem;
        background: rgba(0, 10, 5, 0.4);
        border: 1px solid rgba(0, 255, 136, 0.15);
    }

    .spec-key {
        color: rgba(0, 255, 136, 0.6);
        font-size: 0.8rem;
        letter-spacing: 2px;
    }

    .spec-val {
        color: #00ff88;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* ═══ CTA ═══ */
    .cta-box {
        text-align: center;
        padding: 5rem 2rem;
        border: 1px solid rgba(0, 255, 136, 0.3);
        background: radial-gradient(ellipse at center, rgba(0, 255, 136, 0.05), transparent);
        margin: 4rem 0;
    }

    .cta-box h2 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(1.5rem, 3vw, 2.5rem);
        color: #ffffff;
        letter-spacing: 4px;
        margin-bottom: 1rem;
    }

    .cta-box p {
        color: rgba(255, 255, 255, 0.5);
        font-family: 'Inter', sans-serif !important;
        margin-bottom: 2rem;
    }

    /* ═══ FOOTER ═══ */
    .cyber-footer {
        text-align: center;
        color: rgba(0, 255, 136, 0.3);
        padding: 4rem 0 2rem 0;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-top: 1px solid rgba(0, 255, 136, 0.1);
        margin-top: 4rem;
    }

    /* ═══ BUTTONS (Streamlit) ═══ */
    .stButton > button {
        background: transparent !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
        border-radius: 2px !important;
        padding: 0.9rem 2.5rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: #00ff88 !important;
        color: #000000 !important;
        box-shadow: 0 0 25px #00ff88, 0 0 50px rgba(0, 255, 136, 0.4) !important;
    }

    /* hide streamlit default */
    div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# HERO
# ═══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">system online</div>
    <h1 class="cyber-title">NEUTRON<br>CIPHER</h1>
    <p class="hero-subtitle">[ hide your data in the sound of a dead star ]</p>
    <div class="cyber-line"></div>
    <p class="hero-desc">
        An experimental encryption system that transforms your messages 
        into the pulsating rhythm of a neutron star. Every byte you write 
        becomes a pulse. Every word becomes a signal. Every secret becomes 
        a dying star, screaming across the void.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# SECTION: FEATURES
# ═══════════════════════════════════════
st.markdown("""
<div class="section">
    <div class="section-label">// capabilities</div>
    <h2 class="section-title">Built for the <span>paranoid</span> mind.</h2>
    <p class="section-desc">
        Every layer of Neutron Cipher is designed with one purpose: 
        to make your message indistinguishable from cosmic noise.
    </p>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-num">01</div>
            <div class="feature-icon">⚡</div>
            <div class="feature-title">AES-128 Encryption</div>
            <div class="feature-desc">Military-grade encryption using Fernet protocol. Your message is locked before it ever touches the waveform.</div>
        </div>
        <div class="feature-card">
            <div class="feature-num">02</div>
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">HMAC Integrity</div>
            <div class="feature-desc">Every audio file carries its own cryptographic signature. Any tampering — even a single pulse — is instantly detected.</div>
        </div>
        <div class="feature-card">
            <div class="feature-num">03</div>
            <div class="feature-icon">🌟</div>
            <div class="feature-title">Pulsar Carrier</div>
            <div class="feature-desc">Your data rides on waves modeled after the Vela Pulsar — 10.9 pulses per second, echoing across the cosmos.</div>
        </div>
        <div class="feature-card">
            <div class="feature-num">04</div>
            <div class="feature-icon">🎵</div>
            <div class="feature-title">Lossless FLAC</div>
            <div class="feature-desc">Compressed without losing a single bit. 94% smaller than WAV, but identical in every measurable way.</div>
        </div>
        <div class="feature-card">
            <div class="feature-num">05</div>
            <div class="feature-icon">🔐</div>
            <div class="feature-title">Zero Knowledge</div>
            <div class="feature-desc">We never see your password. We never store your data. Everything happens in your browser, invisible to us.</div>
        </div>
        <div class="feature-card">
            <div class="feature-num">06</div>
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Universal Support</div>
            <div class="feature-desc">Arabic, English, emojis, symbols, control characters — every byte is handled with the same precision.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
# SECTION: HOW IT WORKS
# ═══════════════════════════════════════
st.markdown("""
<div class="section">
    <div class="section-label">// protocol</div>
    <h2 class="section-title">How it <span>works</span>.</h2>
    <p class="section-desc">
        Four layers of transformation. From plain text to cosmic signal.
    </p>

    <div class="step">
        <div class="step-num">01</div>
        <div class="step-content">
            <h4>Encryption</h4>
            <p>Your message is encrypted with Fernet (AES-128-CBC + HMAC-SHA256). A fresh random IV is generated for every operation, ensuring that the same message produces a different ciphertext every time.</p>
        </div>
    </div>

    <div class="step">
        <div class="step-num">02</div>
        <div class="step-content">
            <h4>Pulse Mapping</h4>
            <p>Each encrypted byte (0-255) is translated into a specific pulse intensity. The bytes flow into a continuous stream of pulses, spaced 92 milliseconds apart — matching the rhythm of the Vela Pulsar.</p>
        </div>
    </div>

    <div class="step">
        <div class="step-num">03</div>
        <div class="step-content">
            <h4>Waveform Synthesis</h4>
            <p>The pulses are rendered into an audio waveform at 44.1 kHz, with a sharp exponential envelope that mimics the electromagnetic signature of a real neutron star.</p>
        </div>
    </div>

    <div class="step">
        <div class="step-num">04</div>
        <div class="step-content">
            <h4>Lossless Compression</h4>
            <p>The final waveform is encoded as FLAC — a lossless audio format that reduces file size by up to 94% without sacrificing a single bit of data. Your message is now a star.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
# SECTION: SPECS
# ═══════════════════════════════════════
st.markdown("""
<div class="section">
    <div class="section-label">// technical_specs</div>
    <h2 class="section-title">System <span>specifications</span>.</h2>
    <p class="section-desc">
        Every parameter, every protocol, every constant.
    </p>
    <div class="specs">
        <div class="spec-item"><span class="spec-key">ENCRYPTION</span><span class="spec-val">FERNET / AES-128</span></div>
        <div class="spec-item"><span class="spec-key">INTEGRITY</span><span class="spec-val">HMAC-SHA256</span></div>
        <div class="spec-item"><span class="spec-key">KEY DERIVATION</span><span class="spec-val">SHA-256</span></div>
        <div class="spec-item"><span class="spec-key">IV</span><span class="spec-val">RANDOM / SESSION</span></div>
        <div class="spec-item"><span class="spec-key">CARRIER</span><span class="spec-val">VELA PULSAR</span></div>
        <div class="spec-item"><span class="spec-key">PULSE RATE</span><span class="spec-val">10.9 Hz</span></div>
        <div class="spec-item"><span class="spec-key">SAMPLE RATE</span><span class="spec-val">44100 Hz</span></div>
        <div class="spec-item"><span class="spec-key">BIT DEPTH</span><span class="spec-val">16-BIT PCM</span></div>
        <div class="spec-item"><span class="spec-key">CODEC</span><span class="spec-val">FLAC / LOSSLESS</span></div>
        <div class="spec-item"><span class="spec-key">MAX PAYLOAD</span><span class="spec-val">2000 CHARACTERS</span></div>
        <div class="spec-item"><span class="spec-key">COMPRESSION</span><span class="spec-val">~94%</span></div>
        <div class="spec-item"><span class="spec-key">STATUS</span><span class="spec-val">● OPERATIONAL</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
# SECTION: WARNING
# ═══════════════════════════════════════
st.markdown("""
<div class="section">
    <div class="section-label">// security_notice</div>
    <h2 class="section-title">Read <span>carefully</span>.</h2>
    <p class="section-desc">
        Neutron Cipher is built on real cryptography. That means real consequences.
    </p>

    <div class="step" style="border-left-color: #ff2e63;">
        <div class="step-num" style="color: #ff2e63; text-shadow: 0 0 20px rgba(255, 46, 99, 0.5);">!</div>
        <div class="step-content">
            <h4>Lost passwords cannot be recovered.</h4>
            <p>We do not store your password. We cannot reset it. If you forget it, your message is gone — forever, and by design.</p>
        </div>
    </div>

    <div class="step" style="border-left-color: #ff2e63;">
        <div class="step-num" style="color: #ff2e63; text-shadow: 0 0 20px rgba(255, 46, 99, 0.5);">!</div>
        <div class="step-content">
            <h4>Modified audio will not decrypt.</h4>
            <p>Every pulse carries a cryptographic signature. Trimming, compressing, or editing the audio will cause the integrity check to fail.</p>
        </div>
    </div>

    <div class="step" style="border-left-color: #ff2e63;">
        <div class="step-num" style="color: #ff2e63; text-shadow: 0 0 20px rgba(255, 46, 99, 0.5);">!</div>
        <div class="step-content">
            <h4>Always share the FLAC file.</h4>
            <p>Do not convert to MP3. Do not compress. Do not re-encode. Share the original FLAC file exactly as it was produced.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# CTA
# ═══════════════════════════════════════
st.markdown("""
<div class="cta-box">
    <h2>Ready to become a star?</h2>
    <p>Choose your path below.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
with c2:
    if st.button("⚡  ENCRYPT", use_container_width=True):
        st.switch_page("pages/encrypt.py") if hasattr(st, "switch_page") else st.info("Navigate to Encrypt page")
with c3:
    if st.button("🔓  DECRYPT", use_container_width=True):
        st.switch_page("pages/decrypt.py") if hasattr(st, "switch_page") else st.info("Navigate to Decrypt page")

# ═══ FOOTER ═══
st.markdown("""
<div class="cyber-footer">
    [ NEUTRON CIPHER v1.0 ] · ASTRONOMY × CRYPTOGRAPHY · 2026<br>
    <span style="opacity: 0.4;">A message hidden in a dying star is a message that outlives the universe.</span>
</div>
""", unsafe_allow_html=True)
