import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def html(code):
    clean = "".join(line.strip() for line in code.split("\n"))
    st.markdown(clean, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, .stMarkdown, .stMarkdown *, p, div, span, h1, h2, h3, h4, h5 {
    font-family: 'Chakra Petch', 'JetBrains Mono', sans-serif !important;
    background-color: transparent;
}

html, body, .stApp {
    background: #000000 !important;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stApp > header { display: none; }

.block-container {
    max-width: 1400px !important;
    padding: 0 4rem 6rem 4rem !important;
    position: relative;
    z-index: 3;
}

/* ═══ BACKGROUND ═══ */
.bg-layer {
    position: fixed; inset: 0;
    z-index: 0; pointer-events: none;
    overflow: hidden;
}
.bg-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.5;
    will-change: transform;
}
.orb-1 {
    width: 600px; height: 600px;
    background: radial-gradient(circle, #00ff88 0%, transparent 70%);
    top: -200px; left: -100px;
    animation: float1 20s ease-in-out infinite;
}
.orb-2 {
    width: 500px; height: 500px;
    background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
    top: 40%; right: -150px;
    animation: float2 25s ease-in-out infinite;
    opacity: 0.35;
}
.orb-3 {
    width: 700px; height: 700px;
    background: radial-gradient(circle, #7b2ff7 0%, transparent 70%);
    bottom: -300px; left: 30%;
    animation: float3 30s ease-in-out infinite;
    opacity: 0.25;
}
@keyframes float1 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(100px, 80px) scale(1.15); }
}
@keyframes float2 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(-120px, -100px) scale(1.2); }
}
@keyframes float3 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(80px, -80px) scale(1.1); }
}

.bg-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(0,255,136,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,0.04) 1px, transparent 1px);
    background-size: 80px 80px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 40%, black 20%, transparent 80%);
    animation: gridShift 60s linear infinite;
}
@keyframes gridShift {
    0% { background-position: 0 0; }
    100% { background-position: 80px 80px; }
}

/* ═══ NAV ═══ */
.nav {
    position: sticky; top: 0;
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.5rem 0;
    z-index: 100;
    backdrop-filter: blur(24px) saturate(180%);
    background: rgba(0,0,0,0.6);
    margin: 0 -4rem 0 -4rem;
    padding-left: 4rem; padding-right: 4rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.nav-brand {
    display: flex; align-items: center; gap: 0.75rem;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900; font-size: 1rem;
    letter-spacing: 4px; color: #00ff88;
    text-shadow: 0 0 24px rgba(0,255,136,0.8);
}
.nav-brand::before {
    content: '';
    width: 10px; height: 10px;
    background: #00ff88;
    box-shadow: 0 0 20px #00ff88;
    transform: rotate(45deg);
    animation: spin 8s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(45deg); }
    100% { transform: rotate(405deg); }
}
.nav-brand span { color: #fff; }
.nav-links { display: flex; gap: 2.5rem; }
.nav-link {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(255,255,255,0.4); text-decoration: none;
    transition: color 0.3s; position: relative;
}
.nav-link::after {
    content: ''; position: absolute; bottom: -6px; left: 0;
    width: 0; height: 1px; background: #00ff88;
    transition: width 0.3s;
}
.nav-link:hover { color: #00ff88; }
.nav-link:hover::after { width: 100%; }
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
    padding: 8rem 0 6rem 0;
    text-align: center;
    position: relative;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.6rem;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 5px; text-transform: uppercase;
    color: rgba(0,255,136,0.9);
    padding: 0.6rem 1.6rem;
    border: 1px solid rgba(0,255,136,0.25);
    border-radius: 100px;
    background: rgba(0,255,136,0.03);
    backdrop-filter: blur(10px);
    margin-bottom: 3rem;
    animation: fadeInDown 1s ease both;
}
.hero-badge::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%;
    background: #00ff88; box-shadow: 0 0 12px #00ff88;
    animation: blink 2s infinite;
}
.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(3rem, 9vw, 8.5rem);
    font-weight: 900;
    line-height: 0.92;
    letter-spacing: -0.03em;
    margin: 0;
    background: linear-gradient(180deg, #ffffff 0%, #a0ffd0 40%, #00ff88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 80px rgba(0,255,136,0.5));
    animation: fadeInUp 1.2s ease 0.2s both;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem; letter-spacing: 6px;
    text-transform: uppercase; color: rgba(255,255,255,0.3);
    margin-top: 2.5rem;
    animation: fadeInUp 1.2s ease 0.4s both;
}
.hero-desc {
    font-size: 1.15rem;
    color: rgba(255,255,255,0.55);
    max-width: 680px;
    margin: 2.5rem auto 0 auto;
    line-height: 1.85;
    font-weight: 300;
    animation: fadeInUp 1.2s ease 0.6s both;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ═══ SECTION ═══ */
.sec {
    padding: 7rem 0;
    position: relative;
}
.sec-label {
    display: inline-flex; align-items: center; gap: 0.75rem;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 5px;
    text-transform: uppercase; color: rgba(0,255,136,0.7);
    margin-bottom: 1.5rem;
}
.sec-label::before {
    content: '';
    width: 30px; height: 1px;
    background: #00ff88;
    box-shadow: 0 0 12px #00ff88;
}
.sec-title {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: clamp(2rem, 4.5vw, 3.5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    color: #fff;
    margin: 0 0 1.25rem 0;
    max-width: 800px;
}
.sec-title em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sec-desc {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.5);
    max-width: 640px;
    line-height: 1.85;
    margin: 0 0 4rem 0;
    font-weight: 300;
}

/* ═══ FEATURES — بدون أرقام أو أيقونات ═══ */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 1.25rem;
}
.feat {
    position: relative;
    padding: 2.5rem 2rem 2.5rem 2rem;
    background: linear-gradient(145deg, rgba(255,255,255,0.035), rgba(255,255,255,0.008));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.5s cubic-bezier(0.4,0,0.2,1);
    backdrop-filter: blur(20px);
}
.feat::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,136,0.7), transparent);
    opacity: 0;
    transition: opacity 0.5s;
}
.feat:hover {
    transform: translateY(-6px);
    border-color: rgba(0,255,136,0.3);
    box-shadow:
        0 20px 60px rgba(0,0,0,0.5),
        0 0 80px rgba(0,255,136,0.12);
}
.feat:hover::before { opacity: 1; }
.feat-t {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.9rem;
    letter-spacing: 0.01em;
}
.feat-t::before {
    content: '▸';
    color: #00ff88;
    margin-right: 0.6rem;
    text-shadow: 0 0 15px #00ff88;
    font-size: 1rem;
}
.feat-d {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.5);
    line-height: 1.8;
    font-weight: 300;
}

/* ═══ STATS ═══ */
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 3rem;
}
.stat {
    padding: 3rem 1.5rem;
    text-align: center;
    background: linear-gradient(145deg, rgba(0,255,136,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 14px;
    transition: all 0.4s;
}
.stat:hover {
    border-color: rgba(0,255,136,0.4);
    transform: translateY(-4px);
}
.stat-n {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(180deg, #fff, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: block;
    margin-bottom: 0.75rem;
    filter: drop-shadow(0 0 30px rgba(0,255,136,0.5));
}
.stat-l {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
}

/* ═══ PROTOCOL STEPS ═══ */
.steps { position: relative; }
.steps::before {
    content: '';
    position: absolute;
    left: 32px; top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(180deg, transparent, rgba(0,255,136,0.3), transparent);
}
.step {
    display: grid;
    grid-template-columns: 65px 1fr;
    gap: 2.5rem;
    padding: 2.5rem 0;
    position: relative;
    transition: padding-left 0.4s;
}
.step:hover { padding-left: 1.5rem; }
.step-n {
    width: 65px; height: 65px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 700;
    color: #00ff88;
    background: #000;
    border: 1px solid rgba(0,255,136,0.4);
    border-radius: 50%;
    position: relative;
    z-index: 1;
    box-shadow: 0 0 30px rgba(0,255,136,0.3), inset 0 0 20px rgba(0,255,136,0.1);
    transition: all 0.4s;
}
.step:hover .step-n {
    background: #00ff88;
    color: #000;
    box-shadow: 0 0 50px rgba(0,255,136,0.8);
    transform: scale(1.1);
}
.step-t {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.35rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.01em;
}
.step-d {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.5);
    line-height: 1.85;
    font-weight: 300;
}

/* ═══ SPECS ═══ */
.specs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.75rem;
}
.spec {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.75rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    transition: all 0.3s;
}
.spec:hover {
    background: rgba(0,255,136,0.04);
    border-color: rgba(0,255,136,0.25);
    transform: translateX(4px);
}
.spec-k {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    font-weight: 500;
}
.spec-v {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem;
    letter-spacing: 1px;
    color: #00ff88;
}

/* ═══ WARNINGS ═══ */
.warns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 3rem;
}
.warn {
    padding: 2rem;
    background: linear-gradient(145deg, rgba(255,46,99,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,46,99,0.2);
    border-radius: 14px;
    position: relative;
    transition: all 0.4s;
}
.warn:hover {
    transform: translateY(-4px);
    border-color: rgba(255,46,99,0.5);
    box-shadow: 0 20px 50px rgba(255,46,99,0.15);
}
.warn-t {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.01em;
}
.warn-t::before {
    content: '▲';
    color: #ff2e63;
    margin-right: 0.6rem;
    text-shadow: 0 0 15px #ff2e63;
    font-size: 0.9rem;
}
.warn-d {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.5);
    line-height: 1.8;
    font-weight: 300;
}

/* ═══ FAQ ═══ */
.faq {
    padding: 2rem 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 2rem;
    transition: all 0.3s;
}
.faq:last-child { border-bottom: 1px solid rgba(255,255,255,0.06); }
.faq:hover { padding-left: 1rem; }
.faq-n {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem;
    color: rgba(0,255,136,0.6);
    letter-spacing: 2px;
    padding-top: 4px;
}
.faq-q {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.01em;
}
.faq-a {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.5);
    line-height: 1.85;
    font-weight: 300;
}

/* ═══ CTA ═══ */
.cta {
    padding: 7rem 3rem;
    text-align: center;
    border: 1px solid rgba(0,255,136,0.25);
    border-radius: 24px;
    background:
        radial-gradient(ellipse at top, rgba(0,255,136,0.15), transparent 60%),
        linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    position: relative;
    overflow: hidden;
    margin-top: 5rem;
}
.cta::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,136,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,0.06) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse at center, black 20%, transparent 70%);
}
.cta-t {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    color: #fff;
    margin-bottom: 1rem;
    position: relative;
    letter-spacing: -0.02em;
}
.cta-t em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cta-d {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.5);
    position: relative;
    font-weight: 300;
}

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: linear-gradient(145deg, rgba(0,255,136,0.08), rgba(0,255,136,0.02)) !important;
    color: #00ff88 !important;
    border: 1px solid rgba(0,255,136,0.4) !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.4s cubic-bezier(0.4,0,0.2,1) !important;
    width: 100% !important;
}
.stButton > button:hover {
    color: #000 !important;
    background: #00ff88 !important;
    border-color: #00ff88 !important;
    box-shadow:
        0 0 40px rgba(0,255,136,0.6),
        0 0 80px rgba(0,255,136,0.3) !important;
    transform: translateY(-3px);
}

/* ═══ INPUTS ═══ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(0,255,136,0.25) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem 1.25rem !important;
    transition: all 0.3s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 30px rgba(0,255,136,0.3) !important;
}

/* ═══ FOOTER ═══ */
.foot {
    margin-top: 8rem;
    padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    flex-wrap: wrap;
    gap: 1rem;
}
.foot-brand {
    color: rgba(0,255,136,0.8);
    text-shadow: 0 0 20px rgba(0,255,136,0.5);
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: rgba(0,255,136,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,255,136,0.5); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# BACKGROUND
# ═══════════════════════════════════════
html("""
<div class="bg-layer">
    <div class="bg-grid"></div>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>
</div>
""")


# ═══════════════════════════════════════
# NAV
# ═══════════════════════════════════════
html("""
<div class="nav">
    <div class="nav-brand">NEUTRON<span>CIPHER</span></div>
    <div class="nav-links">
        <a href="#features" class="nav-link">Features</a>
        <a href="#protocol" class="nav-link">Protocol</a>
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
        Transform your messages into the pulsating rhythm of a neutron star.
        Every byte becomes a pulse. Every word becomes a signal.
        Every secret becomes a dying star, screaming silently across the void.
    </p>
</div>
""")

c1, c2, c3, c4 = st.columns([1, 1.3, 1.3, 1])
with c2:
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True):
        st.switch_page("pages/encrypt.py")
with c3:
    if st.button("◈  DECRYPT AUDIO", use_container_width=True):
        st.switch_page("pages/decrypt.py")


# ═══════════════════════════════════════
# FEATURES — مبسطة
# ═══════════════════════════════════════
html("""
<div class="sec" id="features">
    <div class="sec-label">// capabilities</div>
    <h2 class="sec-title">Built for the <em>paranoid</em> mind.</h2>
    <p class="sec-desc">Every layer is designed with one purpose — to make your message indistinguishable from cosmic noise.</p>
    <div class="feat-grid">
        <div class="feat"><div class="feat-t">AES-128 Encryption</div><div class="feat-d">Military-grade encryption via Fernet. Your message is locked before it ever touches the waveform.</div></div>
        <div class="feat"><div class="feat-t">HMAC Integrity</div><div class="feat-d">Every file carries its own cryptographic signature. Any tampering — even a single pulse — is instantly detected.</div></div>
        <div class="feat"><div class="feat-t">Pulsar Carrier</div><div class="feat-d">Your data rides on waves modeled after the Vela Pulsar — 10.9 pulses per second, echoing across the cosmos.</div></div>
        <div class="feat"><div class="feat-t">Lossless FLAC</div><div class="feat-d">Compressed without losing a single bit. 94% smaller than WAV, yet identical in every measurable way.</div></div>
        <div class="feat"><div class="feat-t">Zero Knowledge</div><div class="feat-d">We never see your password. We never store your data. Everything happens in memory, invisible to us.</div></div>
        <div class="feat"><div class="feat-t">Universal Support</div><div class="feat-d">Arabic, English, emojis, symbols, control characters — every byte is handled with the same precision.</div></div>
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
<div class="sec" id="protocol">
    <div class="sec-label">// protocol</div>
    <h2 class="sec-title">Four layers. <em>One signal.</em></h2>
    <p class="sec-desc">From plain text to cosmic transmission — a transformation in four acts.</p>
    <div class="steps">
        <div class="step"><div class="step-n">01</div><div><div class="step-t">Encryption</div><div class="step-d">Your message is encrypted with Fernet (AES-128-CBC + HMAC-SHA256). A fresh random IV is generated for every operation — the same message produces a different ciphertext every single time.</div></div></div>
        <div class="step"><div class="step-n">02</div><div><div class="step-t">Pulse Mapping</div><div class="step-d">Each encrypted byte (0–255) is translated into a specific pulse intensity. The bytes flow into a continuous stream, spaced 92 milliseconds apart — matching the rhythm of the Vela Pulsar.</div></div></div>
        <div class="step"><div class="step-n">03</div><div><div class="step-t">Waveform Synthesis</div><div class="step-d">The pulses are rendered into an audio waveform at 44.1 kHz, with a sharp exponential envelope that mimics the electromagnetic signature of a real neutron star.</div></div></div>
        <div class="step"><div class="step-n">04</div><div><div class="step-t">Lossless Compression</div><div class="step-d">The waveform is encoded as FLAC — a lossless format that reduces file size by up to 94% without sacrificing a single bit. Your message is now a star.</div></div></div>
    </div>
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
        <div class="warn"><div class="warn-t">Lost passwords cannot be recovered.</div><div class="warn-d">We do not store your password. We cannot reset it. If you forget it, your message is gone — forever, and by design.</div></div>
        <div class="warn"><div class="warn-t">Modified audio will not decrypt.</div><div class="warn-d">Every pulse carries a cryptographic signature. Trimming, compressing, or editing the audio will cause the integrity check to fail.</div></div>
        <div class="warn"><div class="warn-t">Always share the FLAC file.</div><div class="warn-d">Do not convert to MP3. Do not compress. Do not re-encode. Share the original FLAC file exactly as it was produced.</div></div>
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


# ═══════════════════════════════════════
# CTA
# ═══════════════════════════════════════
html("""
<div class="cta">
    <div class="cta-t">Ready to become a <em>star?</em></div>
    <div class="cta-d">Choose your path below.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1.3, 1.3, 1])
with c2:
    if st.button("⚡  ENCRYPT MESSAGE", use_container_width=True, key="cta1"):
        st.switch_page("pages/encrypt.py")
with c3:
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
