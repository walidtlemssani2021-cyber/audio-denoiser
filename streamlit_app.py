import streamlit as st

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# HTML HELPER
# ═══════════════════════════════════════════════════════════════
def html(code):
    clean = "".join(line.strip() for line in code.split("\n"))
    st.markdown(clean, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, .stMarkdown, .stMarkdown *, p, div, span, h1, h2, h3, h4, h5 {
    font-family: 'Space Grotesk', 'JetBrains Mono', sans-serif !important;
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
.bg-layer { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.55; will-change: transform; }
.orb-1 { width: 700px; height: 700px; background: radial-gradient(circle, #00ff88 0%, transparent 70%); top: -250px; left: -150px; animation: float1 22s ease-in-out infinite; }
.orb-2 { width: 600px; height: 600px; background: radial-gradient(circle, #00d4ff 0%, transparent 70%); top: 35%; right: -200px; animation: float2 28s ease-in-out infinite; opacity: 0.4; }
.orb-3 { width: 800px; height: 800px; background: radial-gradient(circle, #7b2ff7 0%, transparent 70%); bottom: -350px; left: 25%; animation: float3 32s ease-in-out infinite; opacity: 0.3; }
@keyframes float1 { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(120px, 100px) scale(1.15); } }
@keyframes float2 { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(-140px, -120px) scale(1.2); } }
@keyframes float3 { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(100px, -100px) scale(1.1); } }

.bg-grid {
    position: absolute; inset: 0;
    background-image: linear-gradient(rgba(0,255,136,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,136,0.05) 1px, transparent 1px);
    background-size: 70px 70px;
    mask-image: radial-gradient(ellipse 90% 70% at 50% 40%, black 15%, transparent 80%);
    animation: gridShift 60s linear infinite;
}
@keyframes gridShift { 0% { background-position: 0 0; } 100% { background-position: 70px 70px; } }

/* ═══ NAV ═══ */
.nav {
    position: sticky; top: 0;
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.5rem 0; z-index: 100;
    backdrop-filter: blur(24px) saturate(180%);
    background: rgba(0,0,0,0.7);
    margin: 0 -4rem 0 -4rem;
    padding-left: 4rem; padding-right: 4rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.nav-brand {
    display: flex; align-items: center; gap: 0.85rem;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900; font-size: 1.15rem;
    letter-spacing: 6px; color: #00ff88;
    text-shadow: 0 0 30px rgba(0,255,136,0.9), 0 0 60px rgba(0,255,136,0.5);
}
.nav-brand::before {
    content: ''; width: 12px; height: 12px; background: #00ff88;
    box-shadow: 0 0 25px #00ff88, 0 0 50px rgba(0,255,136,0.6); transform: rotate(45deg);
    animation: spin 8s linear infinite;
}
@keyframes spin { 0% { transform: rotate(45deg); } 100% { transform: rotate(405deg); } }
.nav-links { display: flex; gap: 2.5rem; }
.nav-link {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(255,255,255,0.45); text-decoration: none;
    transition: color 0.3s; position: relative;
}
.nav-link::after { content: ''; position: absolute; bottom: -6px; left: 0; width: 0; height: 1px; background: #00ff88; transition: width 0.3s; }
.nav-link:hover { color: #00ff88; }
.nav-link:hover::after { width: 100%; }
.nav-status { display: flex; align-items: center; gap: 0.5rem; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem; letter-spacing: 3px; color: #00ff88; }
.nav-dot { width: 7px; height: 7px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 14px #00ff88; animation: blink 1.8s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ═══ HERO ═══ */
.hero { padding: 7rem 0 5rem 0; text-align: center; position: relative; }

.hero-name {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(3rem, 10vw, 9rem);
    font-weight: 900;
    line-height: 1;
    letter-spacing: 0.05em;
    margin: 0 0 2rem 0;
    background: linear-gradient(180deg, #ffffff 0%, #00ff88 50%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 100px rgba(0,255,136,0.6)) drop-shadow(0 0 200px rgba(0,255,136,0.3));
    animation: fadeInUp 1.2s ease 0.1s both, glowPulse 4s ease-in-out infinite;
}
@keyframes glowPulse {
    0%, 100% { filter: drop-shadow(0 0 100px rgba(0,255,136,0.6)) drop-shadow(0 0 200px rgba(0,255,136,0.3)); }
    50% { filter: drop-shadow(0 0 130px rgba(0,255,136,0.9)) drop-shadow(0 0 260px rgba(0,255,136,0.5)); }
}

.hero-tagline {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(1rem, 2vw, 1.4rem);
    font-weight: 300;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(0, 255, 136, 0.6);
    margin: 0;
    animation: fadeInUp 1.2s ease 0.4s both;
}

.hero-divider {
    width: 200px; height: 1px;
    margin: 3rem auto;
    background: linear-gradient(90deg, transparent, #00ff88, transparent);
    box-shadow: 0 0 20px #00ff88;
    animation: fadeInUp 1.2s ease 0.6s both;
}

.hero-desc {
    font-size: 1.15rem; color: rgba(255,255,255,0.55);
    max-width: 680px; margin: 0 auto;
    line-height: 1.9; font-weight: 300;
    animation: fadeInUp 1.2s ease 0.8s both;
}
@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

/* ═══ SECTION ═══ */
.sec { padding: 6rem 0; position: relative; }
.sec-label {
    display: inline-flex; align-items: center; gap: 0.75rem;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 5px; text-transform: uppercase;
    color: rgba(0,255,136,0.7); margin-bottom: 1.5rem;
}
.sec-label::before { content: ''; width: 30px; height: 1px; background: #00ff88; box-shadow: 0 0 12px #00ff88; }
.sec-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(2rem, 4.5vw, 3.5rem); font-weight: 700;
    letter-spacing: -0.02em; line-height: 1.15; color: #fff;
    margin: 0 0 1.25rem 0; max-width: 800px;
    text-transform: uppercase;
}
.sec-title em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sec-desc {
    font-size: 1.05rem; color: rgba(255,255,255,0.5);
    max-width: 640px; line-height: 1.9;
    margin: 0 0 4rem 0; font-weight: 300;
}

/* ═══ FEATURES ═══ */
.feat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; }
.feat {
    position: relative; padding: 2.5rem 2rem;
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.08); border-radius: 16px;
    overflow: hidden; transition: all 0.5s cubic-bezier(0.4,0,0.2,1);
    backdrop-filter: blur(20px);
}
.feat::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 1px; background: linear-gradient(90deg, transparent, rgba(0,255,136,0.8), transparent);
    opacity: 0; transition: opacity 0.5s;
}
.feat:hover {
    transform: translateY(-8px); border-color: rgba(0,255,136,0.4);
    box-shadow: 0 25px 70px rgba(0,0,0,0.6), 0 0 100px rgba(0,255,136,0.15);
}
.feat:hover::before { opacity: 1; }
.feat-t {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem; font-weight: 700; color: #fff;
    margin-bottom: 0.9rem; letter-spacing: 0.08em;
    text-transform: uppercase;
}
.feat-t::before { content: '▸'; color: #00ff88; margin-right: 0.7rem; text-shadow: 0 0 20px #00ff88; font-size: 1.1rem; }
.feat-d { font-size: 0.95rem; color: rgba(255,255,255,0.55); line-height: 1.85; font-weight: 300; }

/* ═══ STATS ═══ */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-top: 3rem; }
.stat {
    padding: 3rem 1.5rem; text-align: center;
    background: linear-gradient(145deg, rgba(0,255,136,0.05), rgba(255,255,255,0.01));
    border: 1px solid rgba(0,255,136,0.2); border-radius: 16px;
    transition: all 0.4s;
}
.stat:hover { border-color: rgba(0,255,136,0.6); transform: translateY(-6px); box-shadow: 0 20px 60px rgba(0,255,136,0.15); }
.stat-n {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 3.2rem; font-weight: 900;
    background: linear-gradient(180deg, #fff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    display: block; margin-bottom: 0.85rem;
    filter: drop-shadow(0 0 40px rgba(0,255,136,0.6));
}
.stat-l {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(255,255,255,0.45);
}

/* ═══ WARNINGS ═══ */
.warns { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-top: 3rem; }
.warn {
    padding: 2.25rem;
    background: linear-gradient(145deg, rgba(255,46,99,0.05), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,46,99,0.25); border-radius: 16px;
    position: relative; transition: all 0.4s;
}
.warn:hover { transform: translateY(-6px); border-color: rgba(255,46,99,0.6); box-shadow: 0 25px 60px rgba(255,46,99,0.2); }
.warn-t {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem; font-weight: 700; color: #fff;
    margin-bottom: 0.85rem; letter-spacing: 0.04em;
    text-transform: uppercase;
}
.warn-t::before { content: '▲'; color: #ff2e63; margin-right: 0.7rem; text-shadow: 0 0 20px #ff2e63; font-size: 0.95rem; }
.warn-d { font-size: 0.95rem; color: rgba(255,255,255,0.55); line-height: 1.85; font-weight: 300; }

/* ═══ FAQ ═══ */
.faq {
    padding: 2rem 0;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: grid; grid-template-columns: 80px 1fr; gap: 2rem;
    transition: all 0.3s;
}
.faq:last-child { border-bottom: 1px solid rgba(255,255,255,0.07); }
.faq:hover { padding-left: 1rem; }
.faq-n { font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem; color: rgba(0,255,136,0.7); letter-spacing: 2px; padding-top: 4px; }
.faq-q {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem; font-weight: 700; color: #fff;
    margin-bottom: 0.85rem; letter-spacing: 0.03em;
    text-transform: uppercase;
}
.faq-a { font-size: 0.95rem; color: rgba(255,255,255,0.55); line-height: 1.9; font-weight: 300; }

/* ═══ CTA ═══ */
.cta {
    padding: 7rem 3rem; text-align: center;
    border: 1px solid rgba(0,255,136,0.3); border-radius: 28px;
    background: radial-gradient(ellipse at top, rgba(0,255,136,0.18), transparent 60%), linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    position: relative; overflow: hidden; margin-top: 5rem;
}
.cta::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(rgba(0,255,136,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,136,0.07) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse at center, black 20%, transparent 70%);
}
.cta-t {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 700;
    color: #fff; margin-bottom: 1rem; position: relative;
    letter-spacing: 0.03em; text-transform: uppercase;
}
.cta-t em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cta-d { font-size: 1.05rem; color: rgba(255,255,255,0.55); position: relative; font-weight: 300; }

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: linear-gradient(145deg, rgba(0,255,136,0.1), rgba(0,255,136,0.02)) !important;
    color: #00ff88 !important;
    border: 1px solid rgba(0,255,136,0.5) !important;
    border-radius: 12px !important;
    padding: 1.1rem 2rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
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
    box-shadow: 0 0 50px rgba(0,255,136,0.7), 0 0 100px rgba(0,255,136,0.4) !important;
    transform: translateY(-3px);
}

/* ═══ FOOTER ═══ */
.foot {
    margin-top: 8rem; padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex; justify-content: space-between; align-items: center;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(255,255,255,0.3);
    flex-wrap: wrap; gap: 1rem;
}
.foot-brand { color: rgba(0,255,136,0.9); text-shadow: 0 0 25px rgba(0,255,136,0.6); font-weight: 700; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: rgba(0,255,136,0.4); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,255,136,0.7); }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# BACKGROUND
# ═══════════════════════════════════════════════════════════════
html("""
<div class="bg-layer">
    <div class="bg-grid"></div>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# NAV
# ═══════════════════════════════════════════════════════════════
html("""
<div class="nav">
    <div class="nav-brand">CRYPTORIAN</div>
    <div class="nav-links">
        <a href="#features" class="nav-link">Features</a>
        <a href="#faq" class="nav-link">FAQ</a>
    </div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
html("""
<div class="hero">
    <h1 class="hero-name">CRYPTORIAN</h1>
    <p class="hero-tagline">Encrypt in Starlight</p>
    <div class="hero-divider"></div>
    <p class="hero-desc">
        Cryptorian converts your messages into a modified version of a neutron star's sound.
        Every character becomes a pulse. Every word becomes a signal.
        Every secret becomes a dying star, echoing across the void.
    </p>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec" id="features">
    <div class="sec-label">// CAPABILITIES</div>
    <h2 class="sec-title">BUILT FOR THE <em>PARANOID</em> MIND.</h2>
    <p class="sec-desc">Every layer is designed with one purpose — to make your message indistinguishable from cosmic noise.</p>
    <div class="feat-grid">
        <div class="feat"><div class="feat-t">NEUTRON SOUND</div><div class="feat-d">Your message rides on waves modeled after a neutron star's sound. Each character becomes a unique pulse.</div></div>
        <div class="feat"><div class="feat-t">91 SIGNATURES</div><div class="feat-d">Each character (letter, digit, symbol) has a unique sonic signature. No two signatures are alike.</div></div>
        <div class="feat"><div class="feat-t">KEY SHUFFLING</div><div class="feat-d">The secret key reorders the signatures. Same character, different pulse — every time.</div></div>
        <div class="feat"><div class="feat-t">LENGTH HEADER</div><div class="feat-d">The text length is embedded in the audio. Decryption knows exactly when to stop.</div></div>
        <div class="feat"><div class="feat-t">3 SHAPES</div><div class="feat-d">Each signature has one of 3 pulse shapes. This ensures that similar characters remain distinct.</div></div>
        <div class="feat"><div class="feat-t">WAV & FLAC</div><div class="feat-d">Choose uncompressed WAV for universal playback, or FLAC for 80% size saving.</div></div>
    </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// BY THE NUMBERS</div>
    <h2 class="sec-title">NUMBERS THAT <em>MATTER.</em></h2>
    <div class="stats">
        <div class="stat"><span class="stat-n">91</span><span class="stat-l">SIGNATURES</span></div>
        <div class="stat"><span class="stat-n">44100</span><span class="stat-l">SAMPLE RATE</span></div>
        <div class="stat"><span class="stat-n">2000</span><span class="stat-l">MAX CHARACTERS</span></div>
        <div class="stat"><span class="stat-n">80%</span><span class="stat-l">FLAC SAVING</span></div>
        <div class="stat"><span class="stat-n">3</span><span class="stat-l">PULSE SHAPES</span></div>
    </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# WARNINGS
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// SECURITY NOTICE</div>
    <h2 class="sec-title">READ <em>CAREFULLY.</em></h2>
    <p class="sec-desc">Cryptorian is built on real constraints. That means real consequences.</p>
    <div class="warns">
        <div class="warn"><div class="warn-t">THE KEY IS NEVER SAVED.</div><div class="warn-d">The key is not stored anywhere. If you forget it, the message cannot be recovered. There is no password recovery.</div></div>
        <div class="warn"><div class="warn-t">DO NOT MODIFY THE AUDIO.</div><div class="warn-d">Any modification (trimming, compressing, or converting) will corrupt the encryption. Share the original file as-is.</div></div>
        <div class="warn"><div class="warn-t">SHARE THE KEY SEPARATELY.</div><div class="warn-d">Never send the key together with the audio file. Use a separate secure channel for the key.</div></div>
    </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FAQ
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec" id="faq">
    <div class="sec-label">// FAQ</div>
    <h2 class="sec-title">QUESTIONS. <em>ANSWERED.</em></h2>
    <p class="sec-desc">Everything you need to know before you trust us with your secrets.</p>
    <div class="faq"><div class="faq-n">Q1</div><div><div class="faq-q">WHAT CHARACTERS ARE SUPPORTED?</div><div class="faq-a">Letters (a-z, A-Z), digits (0-9), 29 symbols, and spaces. Arabic characters and emojis are not supported.</div></div></div>
    <div class="faq"><div class="faq-n">Q2</div><div><div class="faq-q">HOW LONG CAN MY MESSAGE BE?</div><div class="faq-a">Up to 2000 characters. Any message longer than that will be rejected by the system.</div></div></div>
    <div class="faq"><div class="faq-n">Q3</div><div><div class="faq-q">WHAT ARE THE KEY RULES?</div><div class="faq-a">The key must contain only letters and spaces. Digits and symbols are rejected. The key is case-sensitive.</div></div></div>
    <div class="faq"><div class="faq-n">Q4</div><div><div class="faq-q">CAN THE KEY BE RECOVERED?</div><div class="faq-a">No. The key is never saved. Without the correct key, the message cannot be decrypted.</div></div></div>
    <div class="faq"><div class="faq-n">Q5</div><div><div class="faq-q">WHY WAV AND FLAC?</div><div class="faq-a">WAV is uncompressed and works on all devices. FLAC is lossless and saves ~80% of the size. Both preserve the encryption.</div></div></div>
    <div class="faq"><div class="faq-n">Q6</div><div><div class="faq-q">CAN I MODIFY THE AUDIO FILE?</div><div class="faq-a">No. Any modification (trimming, compressing, or converting) will corrupt the encryption and make decryption impossible.</div></div></div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# CTA
# ═══════════════════════════════════════════════════════════════
html("""
<div class="cta">
    <div class="cta-t">READY TO BECOME A <em>STAR?</em></div>
    <div class="cta-d">Choose your path below.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CTA BUTTONS
# ═══════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns([1, 1.3, 1.3, 1])
with c2:
    if st.button("ENCRYPT MESSAGE", use_container_width=True):
        st.info("The encryption page will be added soon.")
with c3:
    if st.button("DECRYPT AUDIO", use_container_width=True, key="decrypt_btn"):
        st.info("The decryption page will be added soon.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
html("""
<div class="foot">
    <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
    <div>SOUND-BASED ENCRYPTION</div>
</div>
""")
