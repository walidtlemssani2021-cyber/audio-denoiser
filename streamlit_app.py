import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════
# HELPER — يمنع ظهور HTML كنص
# ═══════════════════════════════════════
def html(code):
    """يحذف المسافات والأسطر الجديدة لتجنب عرض HTML كنص"""
    clean = "".join(line.strip() for line in code.split("\n"))
    st.markdown(clean, unsafe_allow_html=True)


# ═══════════════════════════════════════
# CSS
# ═══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;600&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; }

html, body, .stApp {
    background: #04040a !important;
    color: #e8e8ea;
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stApp > header { display: none; }

.block-container {
    max-width: 1300px !important;
    padding: 0 3rem 4rem 3rem !important;
}

/* ═══ Ambient background ═══ */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,255,136,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,0.02) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    mask-image: radial-gradient(ellipse 90% 70% at 50% 30%, black 10%, transparent 80%);
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    top: -40%; left: 50%;
    transform: translateX(-50%);
    width: 140%; height: 90%;
    background: radial-gradient(ellipse at center, rgba(0,255,136,0.12), transparent 55%);
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
}

/* ═══ NAV ═══ */
.nav {
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.5rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative; z-index: 2;
}
.nav-brand {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900; font-size: 1.05rem; letter-spacing: 4px;
    color: #00ff88; text-shadow: 0 0 20px rgba(0,255,136,0.6);
}
.nav-brand span { color: #fff; }
.nav-status {
    display: flex; align-items: center; gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 3px; color: #00ff88;
}
.nav-dot {
    width: 6px; height: 6px; border-radius: 50%; background: #00ff88;
    box-shadow: 0 0 12px #00ff88; animation: blink 1.8s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ═══ HERO ═══ */
.hero {
    padding: 6rem 0 5rem 0; text-align: center;
    position: relative; z-index: 2;
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 5px; text-transform: uppercase;
    color: rgba(0,255,136,0.7);
    padding: 0.55rem 1.4rem;
    border: 1px solid rgba(0,255,136,0.25);
    border-radius: 100px;
    margin-bottom: 2.5rem;
    backdrop-filter: blur(10px);
}
.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(2.8rem, 8vw, 7rem);
    font-weight: 900; line-height: 0.95;
    letter-spacing: -0.02em; margin: 0;
    background: linear-gradient(180deg, #ffffff 0%, #00ff88 130%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 60px rgba(0,255,136,0.35));
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem; letter-spacing: 5px;
    text-transform: uppercase; color: rgba(255,255,255,0.35);
    margin-top: 2rem;
}
.hero-desc {
    font-size: 1.08rem; color: rgba(255,255,255,0.55);
    max-width: 620px; margin: 2.5rem auto 0 auto; line-height: 1.9;
}

/* ═══ DIVIDER ═══ */
.div {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,136,0.5), transparent);
    margin: 0 auto; max-width: 800px;
}

/* ═══ SECTION ═══ */
.sec { padding: 6rem 0; position: relative; z-index: 2; }
.sec-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 5px;
    text-transform: uppercase; color: rgba(0,255,136,0.55);
    margin-bottom: 1.5rem;
}
.sec-title {
    font-size: clamp(1.8rem, 3.6vw, 2.9rem);
    font-weight: 800; letter-spacing: -0.02em;
    line-height: 1.15; color: #fff; margin: 0 0 1rem 0;
    max-width: 720px;
}
.sec-title em { color: #00ff88; font-style: normal; text-shadow: 0 0 40px rgba(0,255,136,0.5); }
.sec-desc {
    font-size: 1rem; color: rgba(255,255,255,0.5);
    max-width: 620px; line-height: 1.9; margin: 0 0 3.5rem 0;
}

/* ═══ FEATURE GRID ═══ */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 4px; overflow: hidden;
}
.cell {
    background: #04040a;
    padding: 2.5rem 2rem;
    transition: background 0.4s ease;
    position: relative;
}
.cell:hover { background: rgba(0,255,136,0.035); }
.cell:hover .ico { color: #00ff88; text-shadow: 0 0 20px rgba(0,255,136,0.8); }
.cell-num {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 3px;
    color: rgba(255,255,255,0.2); margin-bottom: 2rem;
}
.ico {
    font-size: 1.6rem; color: rgba(255,255,255,0.35);
    transition: all 0.4s ease; display: block; margin-bottom: 1.5rem;
}
.cell-t {
    font-size: 1rem; font-weight: 700;
    color: #fff; margin-bottom: 0.7rem; letter-spacing: -0.01em;
}
.cell-d {
    font-size: 0.88rem; color: rgba(255,255,255,0.45); line-height: 1.75;
}

/* ═══ STEPS ═══ */
.step {
    display: grid; grid-template-columns: 90px 1fr;
    gap: 2rem; padding: 2.5rem 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    transition: padding-left 0.3s ease;
}
.step:last-child { border-bottom: 1px solid rgba(255,255,255,0.06); }
.step:hover { padding-left: 1rem; }
.step-n {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.6rem; font-weight: 800;
    color: rgba(0,255,136,0.4); letter-spacing: 2px;
}
.step-t { font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
.step-d { font-size: 0.92rem; color: rgba(255,255,255,0.5); line-height: 1.8; }

/* ═══ SPECS ═══ */
.specs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 4px; overflow: hidden;
}
.spec {
    display: flex; justify-content: space-between; align-items: center;
    background: #04040a; padding: 1.2rem 1.5rem;
}
.spec-k {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 2px;
    text-transform: uppercase; color: rgba(255,255,255,0.35);
}
.spec-v {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem; letter-spacing: 1px; color: #00ff88;
}

/* ═══ WARNINGS ═══ */
.warns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem; margin-top: 3rem;
}
.warn {
    border: 1px solid rgba(255,46,99,0.25);
    background: rgba(255,46,99,0.03);
    padding: 2rem; border-radius: 4px;
    position: relative;
}
.warn::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 100%; height: 2px; background: #ff2e63;
    box-shadow: 0 0 20px rgba(255,46,99,0.6);
}
.warn-ico {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff2e63; font-size: 1.4rem;
    font-weight: 800; margin-bottom: 1rem; display: block;
}
.warn-t { font-size: 1rem; font-weight: 700; color: #fff; margin-bottom: 0.7rem; }
.warn-d { font-size: 0.87rem; color: rgba(255,255,255,0.5); line-height: 1.75; }

/* ═══ CTA ═══ */
.cta {
    padding: 6rem 3rem; text-align: center;
    border: 1px solid rgba(0,255,136,0.2);
    background: radial-gradient(ellipse at center, rgba(0,255,136,0.07), transparent 70%);
    border-radius: 4px; position: relative; overflow: hidden;
    margin-top: 4rem;
}
.cta::before {
    content: ''; position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(0,255,136,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    mask-image: radial-gradient(ellipse at center, black, transparent 75%);
}
.cta-t {
    font-size: clamp(1.6rem, 3vw, 2.5rem);
    font-weight: 800; color: #fff;
    margin-bottom: 1rem; position: relative;
}
.cta-d { font-size: 0.95rem; color: rgba(255,255,255,0.5); position: relative; }

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: transparent !important;
    color: #00ff88 !important;
    border: 1px solid rgba(0,255,136,0.45) !important;
    border-radius: 3px !important;
    padding: 0.9rem 2rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
}
.stButton > button:hover {
    background: #00ff88 !important;
    color: #000 !important;
    border-color: #00ff88 !important;
    box-shadow: 0 0 30px rgba(0,255,136,0.6), 0 0 70px rgba(0,255,136,0.25) !important;
    transform: translateY(-2px);
}

/* ═══ FOOTER ═══ */
.foot {
    margin-top: 6rem; padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; justify-content: space-between; align-items: center;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.66rem; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(255,255,255,0.25);
    flex-wrap: wrap; gap: 1rem;
}
.foot-brand { color: rgba(0,255,136,0.7); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# NAV
# ═══════════════════════════════════════
html("""
<div class="nav">
    <div class="nav-brand">NEUTRON<span>CIPHER</span></div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")


# ═══════════════════════════════════════
# HERO
# ═══════════════════════════════════════
html("""
<div class="hero">
    <div class="hero-badge">◉ System Online — v1.0</div>
    <h1 class="hero-title">ENCRYPT<br>IN STARLIGHT.</h1>
    <p class="hero-sub">[ hide your data in the sound of a dead star ]</p>
    <p class="hero-desc">
        Neutron Cipher transforms your messages into the pulsating rhythm of a neutron star.
        Every byte becomes a pulse. Every word becomes a signal.
        Every secret becomes a dying star, screaming silently across the void.
    </p>
</div>
""")

html('<div class="div"></div>')


# ═══════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// capabilities</div>
    <h2 class="sec-title">Built for the <em>paranoid</em> mind.</h2>
    <p class="sec-desc">Every layer is designed with one purpose — to make your message indistinguishable from cosmic noise.</p>
    <div class="grid">
        <div class="cell"><div class="cell-num">/ 01</div><span class="ico">⚡</span><div class="cell-t">AES-128 Encryption</div><div class="cell-d">Military-grade encryption via Fernet. Your message is locked before it ever touches the waveform.</div></div>
        <div class="cell"><div class="cell-num">/ 02</div><span class="ico">◈</span><div class="cell-t">HMAC Integrity</div><div class="cell-d">Every file carries its own cryptographic signature. Any tampering — even a single pulse — is instantly detected.</div></div>
        <div class="cell"><div class="cell-num">/ 03</div><span class="ico">✦</span><div class="cell-t">Pulsar Carrier</div><div class="cell-d">Your data rides on waves modeled after the Vela Pulsar — 10.9 pulses per second, echoing across the cosmos.</div></div>
        <div class="cell"><div class="cell-num">/ 04</div><span class="ico">◐</span><div class="cell-t">Lossless FLAC</div><div class="cell-d">Compressed without losing a single bit. 94% smaller than WAV, yet identical in every measurable way.</div></div>
        <div class="cell"><div class="cell-num">/ 05</div><span class="ico">○</span><div class="cell-t">Zero Knowledge</div><div class="cell-d">We never see your password. We never store your data. Everything happens in memory, invisible to us.</div></div>
        <div class="cell"><div class="cell-num">/ 06</div><span class="ico">◎</span><div class="cell-t">Universal Support</div><div class="cell-d">Arabic, English, emojis, symbols, control characters — every byte is handled with the same precision.</div></div>
    </div>
</div>
""")

html('<div class="div"></div>')


# ═══════════════════════════════════════
# PROTOCOL
# ═══════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// protocol</div>
    <h2 class="sec-title">Four layers. <em>One signal.</em></h2>
    <p class="sec-desc">From plain text to cosmic transmission — a transformation in four acts.</p>
    <div class="step"><div class="step-n">01</div><div><div class="step-t">Encryption</div><div class="step-d">Your message is encrypted with Fernet (AES-128-CBC + HMAC-SHA256). A fresh random IV is generated for every operation — the same message produces a different ciphertext every single time.</div></div></div>
    <div class="step"><div class="step-n">02</div><div><div class="step-t">Pulse Mapping</div><div class="step-d">Each encrypted byte (0–255) is translated into a specific pulse intensity. The bytes flow into a continuous stream, spaced 92 milliseconds apart — matching the rhythm of the Vela Pulsar.</div></div></div>
    <div class="step"><div class="step-n">03</div><div><div class="step-t">Waveform Synthesis</div><div class="step-d">The pulses are rendered into an audio waveform at 44.1 kHz, with a sharp exponential envelope that mimics the electromagnetic signature of a real neutron star.</div></div></div>
    <div class="step"><div class="step-n">04</div><div><div class="step-t">Lossless Compression</div><div class="step-d">The waveform is encoded as FLAC — a lossless format that reduces file size by up to 94% without sacrificing a single bit. Your message is now a star.</div></div></div>
</div>
""")

html('<div class="div"></div>')


# ═══════════════════════════════════════
# SPECS
# ═══════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// technical_specs</div>
    <h2 class="sec-title">Every parameter. <em>Documented.</em></h2>
    <p class="sec-desc">Full transparency — the cryptographic primitives, constants, and constraints.</p>
    <div class="specs">
        <div class="spec"><span class="spec-k">Encryption</span><span class="spec-v">FERNET / AES-128</span></div>
        <div class="spec"><span class="spec-k">Integrity</span><span class="spec-v">HMAC-SHA256</span></div>
        <div class="spec"><span class="spec-k">Key Derivation</span><span class="spec-v">SHA-256</span></div>
        <div class="spec"><span class="spec-k">IV</span><span class="spec-v">RANDOM / SESSION</span></div>
        <div class="spec"><span class="spec-k">Carrier</span><span class="spec-v">VELA PULSAR</span></div>
        <div class="spec"><span class="spec-k">Pulse Rate</span><span class="spec-v">10.9 Hz</span></div>
        <div class="spec"><span class="spec-k">Sample Rate</span><span class="spec-v">44100 Hz</span></div>
        <div class="spec"><span class="spec-k">Bit Depth</span><span class="spec-v">16-BIT PCM</span></div>
        <div class="spec"><span class="spec-k">Codec</span><span class="spec-v">FLAC / LOSSLESS</span></div>
        <div class="spec"><span class="spec-k">Max Payload</span><span class="spec-v">2000 CHARS</span></div>
        <div class="spec"><span class="spec-k">Compression</span><span class="spec-v">~94%</span></div>
        <div class="spec"><span class="spec-k">Status</span><span class="spec-v">● OPERATIONAL</span></div>
    </div>
</div>
""")

html('<div class="div"></div>')


# ═══════════════════════════════════════
# WARNINGS
# ═══════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// security_notice</div>
    <h2 class="sec-title">Read <em>carefully.</em></h2>
    <p class="sec-desc">Neutron Cipher is built on real cryptography. That means real consequences.</p>
    <div class="warns">
        <div class="warn"><span class="warn-ico">!</span><div class="warn-t">Lost passwords cannot be recovered.</div><div class="warn-d">We do not store your password. We cannot reset it. If you forget it, your message is gone — forever, and by design.</div></div>
        <div class="warn"><span class="warn-ico">!</span><div class="warn-t">Modified audio will not decrypt.</div><div class="warn-d">Every pulse carries a cryptographic signature. Trimming, compressing, or editing the audio will cause the integrity check to fail.</div></div>
        <div class="warn"><span class="warn-ico">!</span><div class="warn-t">Always share the FLAC file.</div><div class="warn-d">Do not convert to MP3. Do not compress. Do not re-encode. Share the original FLAC file exactly as it was produced.</div></div>
    </div>
</div>
""")


# ═══════════════════════════════════════
# CTA
# ═══════════════════════════════════════
html("""
<div class="cta">
    <div class="cta-t">Ready to become a star?</div>
    <div class="cta-d">Choose your path below.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1.3, 1.3, 1])
with col2:
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True):
        st.switch_page("pages/encrypt.py")
with col3:
    if st.button("◈  DECRYPT AUDIO", use_container_width=True):
        st.switch_page("pages/decrypt.py")


# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
html("""
<div class="foot">
    <div><span class="foot-brand">NEUTRON CIPHER</span> · v1.0 · 2026</div>
    <div>ASTRONOMY × CRYPTOGRAPHY</div>
</div>
""")
