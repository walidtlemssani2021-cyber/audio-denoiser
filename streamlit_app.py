import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER — Encrypt in Starlight",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def html(code):
    clean = "".join(line.strip() for line in code.split("\n"))
    st.markdown(clean, unsafe_allow_html=True)


# ═══════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #04040a !important;
    color: #e8e8ea;
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    scroll-behavior: smooth;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stApp > header { display: none; }

.block-container {
    max-width: 1300px !important;
    padding: 0 3rem 4rem 3rem !important;
}

/* ═══ Ambient ═══ */
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
    background: radial-gradient(ellipse at center, rgba(0,255,136,0.10), transparent 55%);
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
    animation: breathe 8s ease-in-out infinite;
}
@keyframes breathe {
    0%,100% { opacity: 0.8; }
    50% { opacity: 1; }
}

/* ═══ NAV (Sticky) ═══ */
.nav {
    position: sticky; top: 0;
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    background: rgba(4,4,10,0.7);
    margin: 0 -3rem 0 -3rem;
    padding-left: 3rem; padding-right: 3rem;
    z-index: 100;
}
.nav-brand {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900; font-size: 1rem; letter-spacing: 4px;
    color: #00ff88; text-shadow: 0 0 20px rgba(0,255,136,0.6);
}
.nav-brand span { color: #fff; }
.nav-links { display: flex; gap: 2.5rem; }
.nav-link {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(255,255,255,0.45); text-decoration: none;
    transition: color 0.3s;
}
.nav-link:hover { color: #00ff88; }
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
    padding: 7rem 0 5rem 0; text-align: center;
    position: relative; z-index: 2;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.6rem;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 5px; text-transform: uppercase;
    color: rgba(0,255,136,0.75);
    padding: 0.55rem 1.4rem;
    border: 1px solid rgba(0,255,136,0.25);
    border-radius: 100px;
    margin-bottom: 2.5rem;
    backdrop-filter: blur(10px);
}
.hero-badge::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%;
    background: #00ff88; box-shadow: 0 0 10px #00ff88;
    animation: blink 2s infinite;
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
    font-size: 0.82rem; letter-spacing: 5px;
    text-transform: uppercase; color: rgba(255,255,255,0.35);
    margin-top: 2rem;
}
.hero-desc {
    font-size: 1.08rem; color: rgba(255,255,255,0.55);
    max-width: 620px; margin: 2.5rem auto 0 auto; line-height: 1.9;
}
.hero-buttons {
    display: flex; justify-content: center; gap: 1rem;
    margin-top: 3rem; flex-wrap: wrap;
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
    border-radius: 6px; overflow: hidden;
}
.cell {
    background: #04040a;
    padding: 2.5rem 2rem;
    transition: background 0.4s ease;
    position: relative;
}
.cell:hover { background: rgba(0,255,136,0.035); }
.cell:hover .ico { color: #00ff88; text-shadow: 0 0 20px rgba(0,255,136,0.8); transform: scale(1.1); }
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
    color: #fff; margin-bottom: 0.7rem;
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

/* ═══ STATS ═══ */
.stats {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px; overflow: hidden;
    margin-top: 3rem;
}
.stat {
    background: #04040a; padding: 2.5rem 1.5rem; text-align: center;
}
.stat-n {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.5rem; font-weight: 900;
    color: #00ff88; text-shadow: 0 0 30px rgba(0,255,136,0.5);
    display: block; margin-bottom: 0.5rem;
}
.stat-l {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(255,255,255,0.4);
}

/* ═══ SPECS ═══ */
.specs {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px; overflow: hidden;
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
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem; margin-top: 3rem;
}
.warn {
    border: 1px solid rgba(255,46,99,0.25);
    background: rgba(255,46,99,0.03);
    padding: 2rem; border-radius: 6px;
    position: relative;
}
.warn::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 100%; height: 2px; background: #ff2e63;
    box-shadow: 0 0 20px rgba(255,46,99,0.6);
    border-radius: 6px 6px 0 0;
}
.warn-ico {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff2e63; font-size: 1.4rem;
    font-weight: 800; margin-bottom: 1rem; display: block;
}
.warn-t { font-size: 1rem; font-weight: 700; color: #fff; margin-bottom: 0.7rem; }
.warn-d { font-size: 0.87rem; color: rgba(255,255,255,0.5); line-height: 1.75; }

/* ═══ FAQ ═══ */
.faq {
    border-top: 1px solid rgba(255,255,255,0.06);
    padding: 2rem 0;
    display: grid; grid-template-columns: 40px 1fr;
    gap: 1.5rem; cursor: pointer;
    transition: padding-left 0.3s;
}
.faq:hover { padding-left: 1rem; }
.faq:last-child { border-bottom: 1px solid rgba(255,255,255,0.06); }
.faq-q {
    font-size: 1.05rem; font-weight: 600;
    color: #fff; margin-bottom: 0.5rem;
}
.faq-a {
    font-size: 0.9rem; color: rgba(255,255,255,0.5); line-height: 1.8;
}
.faq-n {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem; color: rgba(0,255,136,0.5);
    letter-spacing: 2px;
}

/* ═══ CTA ═══ */
.cta {
    padding: 6rem 3rem; text-align: center;
    border: 1px solid rgba(0,255,136,0.2);
    background: radial-gradient(ellipse at center, rgba(0,255,136,0.07), transparent 70%);
    border-radius: 6px; position: relative; overflow: hidden;
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
    border-radius: 4px !important;
    padding: 0.9rem 2rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    width: 100% !important;
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
    <div class="nav-links">
        <a href="#demo" class="nav-link">Demo</a>
        <a href="#features" class="nav-link">Features</a>
        <a href="#specs" class="nav-link">Specs</a>
        <a href="#faq" class="nav-link">FAQ</a>
    </div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")


# ═══════════════════════════════════════
# HERO
# ═══════════════════════════════════════
html("""
<div class="hero">
    <div class="hero-badge">System Online — v1.0</div>
    <h1 class="hero-title">ENCRYPT<br>IN STARLIGHT.</h1>
    <p class="hero-sub">[ hide your data in the sound of a dead star ]</p>
    <p class="hero-desc">
        Neutron Cipher transforms your messages into the pulsating rhythm of a neutron star.
        Every byte becomes a pulse. Every word becomes a signal.
        Every secret becomes a dying star, screaming silently across the void.
    </p>
</div>
""")

col1, col2, col3, col4 = st.columns([1, 1.3, 1.3, 1])
with col2:
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True):
        st.switch_page("pages/encrypt.py")
with col3:
    if st.button("◈  DECRYPT AUDIO", use_container_width=True):
        st.switch_page("pages/decrypt.py")

st.markdown("<br>", unsafe_allow_html=True)
html('<div class="div"></div>')


# ═══════════════════════════════════════
# DEMO
# ═══════════════════════════════════════
html("""
<div class="sec" id="demo">
    <div class="sec-label">// live_demo</div>
    <h2 class="sec-title">Try it. <em>Right here.</em></h2>
    <p class="sec-desc">No account. No tracking. Just pure cryptography in your browser.</p>
</div>
""")

col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
with col_d2:
    demo_text = st.text_input("Message", placeholder="Type a test message...", label_visibility="collapsed", key="demo_msg")
    demo_pass = st.text_input("Password", type="password", placeholder="Test password...", label_visibility="collapsed", key="demo_pwd")
    if st.button("⚡  RUN DEMO", use_container_width=True):
        if demo_text and demo_pass:
            st.success("✓ Demo will be functional once the engine is integrated.")
        else:
            st.warning("Please enter both message and password.")


st.markdown("<br><br>", unsafe_allow_html=True)
html('<div class="div"></div>')


# ═══════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════
html("""
<div class="sec" id="features">
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
# STATS
# ═══════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// by_the_numbers</div>
    <h2 class="sec-title">Numbers that <em>matter.</em></h2>
    <div class="stats">
        <div class="stat"><span class="stat-n">10.9</span><span class="stat-l">Pulses / Second</span></div>
        <div class="stat"><span class="stat-n">44.1</span><span class="stat-l">kHz Sample Rate</span></div>
        <div class="stat"><span class="stat-n">2000</span><span class="stat-l">Max Characters</span></div>
        <div class="stat"><span class="stat-n">94%</span><span class="stat-l">Compression</span></div>
        <div class="stat"><span class="stat-n">128</span><span class="stat-l">Bit AES Key</span></div>
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
<div class="sec" id="specs">
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

html('<div class="div"></div>')


# ═══════════════════════════════════════
# FAQ
# ═══════════════════════════════════════
html("""
<div class="sec" id="faq">
    <div class="sec-label">// faq</div>
    <h2 class="sec-title">Questions. <em>Answered.</em></h2>
    <p class="sec-desc">Everything you need to know before you trust us with your secrets.</p>
    <div class="faq"><div class="faq-n">Q1</div><div><div class="faq-q">Is my data stored on your servers?</div><div class="faq-a">Never. Everything happens in your browser's memory. We have no database, no logs, no backups.</div></div></div>
    <div class="faq"><div class="faq-n">Q2</div><div><div class="faq-q">What encryption algorithm do you use?</div><div class="faq-a">Fernet, which combines AES-128-CBC for confidentiality with HMAC-SHA256 for integrity. It is the same protocol used by major financial institutions.</div></div></div>
    <div class="faq"><div class="faq-n">Q3</div><div><div class="faq-q">Can you recover my password if I lose it?</div><div class="faq-a">No. By design, we cannot. Your password never leaves your device. If you lose it, the encrypted message is permanently unreadable.</div></div></div>
    <div class="faq"><div class="faq-n">Q4</div><div><div class="faq-q">Why does the audio have to be FLAC?</div><div class="faq-a">FLAC is lossless — every bit is preserved. Lossy formats like MP3 alter the waveform and break the cryptographic signature, making decryption impossible.</div></div></div>
    <div class="faq"><div class="faq-n">Q5</div><div><div class="faq-q">How long can my message be?</div><div class="faq-a">Up to 2000 characters. This limit keeps file size reasonable while covering the vast majority of real-world messages.</div></div></div>
    <div class="faq"><div class="faq-n">Q6</div><div><div class="faq-q">Is this open source?</div><div class="faq-a">Yes. The entire codebase is published on GitHub for public audit. Cryptographic systems should never be trusted blindly.</div></div></div>
</div>
""")

html('<div class="div"></div>')


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
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True, key="cta1"):
        st.switch_page("pages/encrypt.py")
with col3:
    if st.button("◈  DECRYPT AUDIO", use_container_width=True, key="cta2"):
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
