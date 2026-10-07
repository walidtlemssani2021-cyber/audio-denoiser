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

/* BACKGROUND */
.bg-layer { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.5; will-change: transform; }
.orb-1 { width: 700px; height: 700px; background: radial-gradient(circle, #00ff88 0%, transparent 70%); top: -250px; left: -150px; animation: float1 22s ease-in-out infinite; }
.orb-2 { width: 600px; height: 600px; background: radial-gradient(circle, #00d4ff 0%, transparent 70%); top: 35%; right: -200px; animation: float2 28s ease-in-out infinite; opacity: 0.35; }
.orb-3 { width: 800px; height: 800px; background: radial-gradient(circle, #7b2ff7 0%, transparent 70%); bottom: -350px; left: 25%; animation: float3 32s ease-in-out infinite; opacity: 0.25; }
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

/* NAV */
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
    font-weight: 900; font-size: 1.1rem;
    letter-spacing: 5px; color: #00ff88;
    text-shadow: 0 0 30px rgba(0,255,136,0.9);
}
.nav-brand::before {
    content: ''; width: 11px; height: 11px; background: #00ff88;
    box-shadow: 0 0 25px #00ff88; transform: rotate(45deg);
    animation: spin 8s linear infinite;
}
@keyframes spin { 0% { transform: rotate(45deg); } 100% { transform: rotate(405deg); } }
.nav-status { display: flex; align-items: center; gap: 0.5rem; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem; letter-spacing: 3px; color: #00ff88; }
.nav-dot { width: 7px; height: 7px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 14px #00ff88; animation: blink 1.8s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* HERO */
.hero { padding: 7rem 0 5rem 0; text-align: center; position: relative; }

.hero-name {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(2.5rem, 8vw, 7rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: 0.1em;
    margin: 0 auto 2rem auto;
    padding: 0;
    white-space: nowrap;
    background: linear-gradient(180deg, #ffffff 0%, #00ff88 55%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 100px rgba(0,255,136,0.7)) drop-shadow(0 0 200px rgba(0,255,136,0.4));
    animation: fadeInUp 1.2s ease 0.1s both, glowPulse 4s ease-in-out infinite;
}
@keyframes glowPulse {
    0%, 100% { filter: drop-shadow(0 0 100px rgba(0,255,136,0.7)) drop-shadow(0 0 200px rgba(0,255,136,0.4)); }
    50% { filter: drop-shadow(0 0 140px rgba(0,255,136,1)) drop-shadow(0 0 280px rgba(0,255,136,0.6)); }
}

.hero-tagline {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(1rem, 2vw, 1.35rem);
    font-weight: 300;
    letter-spacing: 0.1em;
    color: rgba(255, 255, 255, 0.75);
    margin: 2rem auto 0 auto;
    max-width: 700px;
    line-height: 1.7;
    animation: fadeInUp 1.2s ease 0.4s both;
}

.hero-divider {
    width: 250px; height: 1px;
    margin: 3rem auto;
    background: linear-gradient(90deg, transparent, #00ff88, transparent);
    box-shadow: 0 0 25px #00ff88;
    animation: fadeInUp 1.2s ease 0.6s both;
}

@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

/* SECTION */
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
    margin: 0 0 2rem 0; max-width: 900px;
}
.sec-title em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* TEXT BLOCKS */
.text-block {
    max-width: 800px;
    font-size: 1.1rem;
    color: rgba(255,255,255,0.65);
    line-height: 2;
    font-weight: 300;
    margin-bottom: 2rem;
}
.text-block strong {
    color: #00ff88;
    font-weight: 600;
}

/* FEATURES */
.feat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-top: 3rem; }
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
.feat-num {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.85rem;
    font-weight: 700;
    color: rgba(0,255,136,0.5);
    letter-spacing: 3px;
    margin-bottom: 1.5rem;
    display: block;
}
.feat-t {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.25rem; font-weight: 700; color: #fff;
    margin-bottom: 1rem; letter-spacing: 0.02em;
}
.feat-d { font-size: 0.98rem; color: rgba(255,255,255,0.6); line-height: 1.85; font-weight: 300; }

/* CTA */
.cta {
    padding: 6rem 3rem; text-align: center;
    border: 1px solid rgba(0,255,136,0.3); border-radius: 28px;
    background: radial-gradient(ellipse at top, rgba(0,255,136,0.18), transparent 60%), linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    position: relative; overflow: hidden; margin-top: 4rem;
}
.cta::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(rgba(0,255,136,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,136,0.07) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse at center, black 20%, transparent 70%);
}
.cta-t {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem); font-weight: 700;
    color: #fff; margin-bottom: 1rem; position: relative;
    letter-spacing: 0.02em;
}
.cta-t em {
    font-style: normal;
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cta-d { font-size: 1.05rem; color: rgba(255,255,255,0.6); position: relative; font-weight: 300; }

/* BUTTONS */
.stButton > button {
    background: linear-gradient(145deg, rgba(0,255,136,0.1), rgba(0,255,136,0.02)) !important;
    color: #00ff88 !important;
    border: 1px solid rgba(0,255,136,0.5) !important;
    border-radius: 12px !important;
    padding: 1.1rem 2rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
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

/* FOOTER */
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
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
html("""
<div class="hero">
    <h1 class="hero-name">CRYPTORIAN</h1>
    <p class="hero-tagline">Secure your privacy with Cryptorian</p>
    <div class="hero-divider"></div>
</div>
""")

# Start button
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("GET STARTED", use_container_width=True):
        st.info("The encryption page will be added soon.")

# ═══════════════════════════════════════════════════════════════
# WHY ENCRYPTION MATTERS
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// WHY IT MATTERS</div>
    <h2 class="sec-title">WHY ENCRYPTION <em>MATTERS.</em></h2>
    <p class="text-block">
        Every message you send carries a piece of you. Your words, your thoughts, your secrets —
        they travel through networks you don't control, through servers you don't own,
        through channels that can be intercepted.
    </p>
    <p class="text-block">
        <strong>Encryption is not paranoia.</strong> It is the basic right to keep your
        private life private. It is the difference between a conversation and a broadcast.
        It is the line between your message and everyone else's business.
    </p>
    <p class="text-block">
        In a world where data is currency, encryption is the only true shield.
        It doesn't hide the fact that you are communicating — it simply ensures that
        only the intended recipient can understand what is being said.
    </p>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# WHAT IS CRYPTORIAN
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// THE SYSTEM</div>
    <h2 class="sec-title">WHAT IS <em>CRYPTORIAN?</em></h2>
    <p class="text-block">
        Cryptorian is a sound-based encryption system. It takes your message and transforms it
        into a waveform modeled after the sound of a neutron star — a dead star that pulses
        in the void, sending signals no one can read.
    </p>
    <p class="text-block">
        Every character you write becomes a unique pulse. Every word becomes a rhythm.
        The final audio file sounds like cosmic noise to anyone who listens — but to the
        person who holds the key, it is a clear message.
    </p>
    <p class="text-block">
        <strong>Cryptorian does not hide the message inside the audio.</strong> It turns
        the message into the audio itself. The text is no longer text. It is a star's heartbeat.
    </p>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════════════
html("""
<div class="sec">
    <div class="sec-label">// CAPABILITIES</div>
    <h2 class="sec-title">BUILT FOR THE <em>PARANOID</em> MIND.</h2>
    <div class="feat-grid">
        <div class="feat">
            <span class="feat-num">/ 01</span>
            <div class="feat-t">Neutron Sound</div>
            <div class="feat-d">Your message becomes a waveform modeled after a neutron star's pulse. It sounds like the cosmos — not like data.</div>
        </div>
        <div class="feat">
            <span class="feat-num">/ 02</span>
            <div class="feat-t">Unique Signatures</div>
            <div class="feat-d">Every character — letter, digit, or symbol — has its own sonic signature. No two are ever alike.</div>
        </div>
        <div class="feat">
            <span class="feat-num">/ 03</span>
            <div class="feat-t">Key Shuffling</div>
            <div class="feat-d">The secret key reorders every signature. The same character produces a different pulse with every key.</div>
        </div>
        <div class="feat">
            <span class="feat-num">/ 04</span>
            <div class="feat-t">Length Header</div>
            <div class="feat-d">The message length is embedded in the audio itself. Decryption knows exactly where the message ends.</div>
        </div>
        <div class="feat">
            <span class="feat-num">/ 05</span>
            <div class="feat-t">Dual Formats</div>
            <div class="feat-d">Export as uncompressed WAV for universal playback, or as compressed FLAC for a much smaller file.</div>
        </div>
        <div class="feat">
            <span class="feat-num">/ 06</span>
            <div class="feat-t">Zero Knowledge</div>
            <div class="feat-d">Nothing is stored. Nothing is sent. The entire process happens in memory — invisible to anyone else.</div>
        </div>
    </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FINAL CTA
# ═══════════════════════════════════════════════════════════════
html("""
<div class="cta">
    <div class="cta-t">READY TO BECOME A <em>STAR?</em></div>
    <div class="cta-d">Your message is waiting. Your key is your power.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("ENCRYPT A MESSAGE", use_container_width=True, key="cta_btn"):
        st.info("The encryption page will be added soon.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
html("""
<div class="foot">
    <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
    <div>SOUND-BASED ENCRYPTION</div>
</div>
""")
