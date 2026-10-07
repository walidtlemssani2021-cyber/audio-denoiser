import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cryptorian | Encrypt text into neutron star sound",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html(code: str) -> None:
    """Render raw HTML (indentation stripped so Markdown never treats it as a code block)."""
    st.markdown("".join(line.strip() for line in code.split("\n")), unsafe_allow_html=True)


# Decorative pulse train for the hero (each value = pulse height)
def pulse_path(heights, width=1200, mid=60, gap=70):
    d, x = f"M0 {mid}", 0
    for h in heights:
        d += f" H{x + gap}"
        x += gap
        d += f" L{x + 8} {mid - h} L{x + 16} {mid + h * 0.6} L{x + 24} {mid}"
        x += 24
    return d + f" H{width}"


PULSES = pulse_path([34, 12, 44, 22, 8, 40, 28, 16, 46, 10, 30, 20])

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@300;400;500;600;700&display=swap');

:root {
  --bg: #06080e;
  --ink: #e8eef9;
  --mute: #8d9ab3;
  --beam: #8fd3ff;
  --amber: #ffb45e;
  --line: rgba(232,238,249,.12);
  --serif: 'Instrument Serif', Georgia, serif;
  --sans: 'Manrope', system-ui, sans-serif;
}

html, body, .stApp { background: var(--bg) !important; color: var(--ink); }
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown div { font-family: var(--sans) !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

.block-container { max-width: 1180px !important; padding: 0 2rem 4rem 2rem !important; }

/* faint starfield behind everything */
.stApp::before {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(1px 1px at 12% 18%, #fff8 50%, transparent 51%),
    radial-gradient(1px 1px at 78% 12%, #fff6 50%, transparent 51%),
    radial-gradient(1px 1px at 34% 62%, #fff5 50%, transparent 51%),
    radial-gradient(1px 1px at 90% 70%, #fff7 50%, transparent 51%),
    radial-gradient(1px 1px at 55% 88%, #fff5 50%, transparent 51%),
    radial-gradient(ellipse 60% 50% at 78% 20%, rgba(143,211,255,.10), transparent 70%);
}

/* ── NAV ── */
.nav { display:flex; justify-content:space-between; align-items:center; padding:1.6rem 0; border-bottom:1px solid var(--line); position:relative; z-index:2; }
.brand { font-family:var(--serif); font-size:1.7rem; letter-spacing:.01em; color:var(--ink); display:flex; align-items:center; gap:.6rem; }
.brand i { width:10px; height:10px; border-radius:50%; background:var(--beam); box-shadow:0 0 14px var(--beam), 0 0 32px var(--beam); }
.nav-links { display:flex; gap:2rem; font-size:.9rem; color:var(--mute); }

/* ── HERO ── */
.hero { display:grid; grid-template-columns: 1.15fr .85fr; gap:3rem; align-items:center; padding:5rem 0 3rem 0; position:relative; z-index:2; }
.hero h1 { font-family:var(--serif) !important; font-weight:400; font-size:clamp(3rem, 7vw, 5.6rem); line-height:.98; letter-spacing:-.02em; color:var(--ink); margin:0 0 1.6rem 0; }
.hero h1 em { color:var(--beam); }
.hero p.lead { font-size:1.15rem; line-height:1.75; color:var(--mute); max-width:34rem; margin:0; font-weight:300; }

/* pulsar: the one memorable element */
.pulsar { position:relative; width:min(100%, 440px); aspect-ratio:1; margin-left:auto; transform:rotate(24deg); }
.pulsar .ring { position:absolute; inset:0; margin:auto; border-radius:50%; border:1px solid rgba(143,211,255,.35); width:12%; height:12%; opacity:0; animation:ping 4s cubic-bezier(.2,.6,.3,1) infinite; }
.pulsar .ring:nth-child(2) { animation-delay:1.3s; }
.pulsar .ring:nth-child(3) { animation-delay:2.6s; }
@keyframes ping { 0% { width:12%; height:12%; opacity:.9; } 100% { width:100%; height:100%; opacity:0; } }
.pulsar .beams {
  position:absolute; inset:-8%; border-radius:50%;
  background: conic-gradient(from 0deg, transparent 0 86deg, rgba(143,211,255,.65) 90deg, transparent 94deg 176deg, rgba(143,211,255,.65) 180deg, transparent 184deg 360deg);
  -webkit-mask-image: radial-gradient(circle, #000 0%, transparent 68%);
          mask-image: radial-gradient(circle, #000 0%, transparent 68%);
  animation: spin 5s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
.pulsar .core { position:absolute; inset:0; margin:auto; width:7%; height:7%; border-radius:50%; background:#fff; box-shadow:0 0 18px 6px #fff, 0 0 60px 20px rgba(143,211,255,.8), 0 0 140px 50px rgba(143,211,255,.3); }

/* waveform strip */
.wave { position:relative; z-index:2; border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:1.4rem 0; margin:1rem 0 0 0; overflow:hidden; }
.wave svg { display:block; width:100%; height:120px; }
.wave path { fill:none; stroke:var(--beam); stroke-width:1.5; stroke-linejoin:round; stroke-dasharray:1800; stroke-dashoffset:1800; animation:draw 4s ease-out .3s forwards; filter:drop-shadow(0 0 6px rgba(143,211,255,.6)); }
@keyframes draw { to { stroke-dashoffset:0; } }
.wave-cap { display:flex; justify-content:space-between; font-size:.8rem; color:var(--mute); margin-top:.6rem; }

/* ── SECTIONS ── */
.sec { padding:6rem 0 0 0; position:relative; z-index:2; }
.sec h2 { font-family:var(--serif) !important; font-weight:400; font-size:clamp(2.2rem, 4.6vw, 3.4rem); line-height:1.05; letter-spacing:-.015em; color:var(--ink); margin:0 0 1.2rem 0; max-width:30rem; }
.sec .sub { font-size:1.05rem; line-height:1.75; color:var(--mute); max-width:36rem; margin:0 0 3rem 0; font-weight:300; }

/* steps (a real sequence, so numbered) */
.steps { display:grid; grid-template-columns:repeat(3, 1fr); border-top:1px solid var(--line); }
.step { padding:2rem 2rem 0 0; }
.step + .step { padding-left:2rem; border-left:1px solid var(--line); }
.step b { font-family:var(--serif); font-weight:400; font-size:3.4rem; line-height:1; color:var(--amber); display:block; margin-bottom:1rem; }
.step h3 { font-size:1.15rem; font-weight:600; color:var(--ink); margin:0 0 .6rem 0; }
.step p { font-size:.97rem; line-height:1.7; color:var(--mute); margin:0; font-weight:300; }

/* features as a ruled list, not a card grid */
.feats { display:grid; grid-template-columns:1fr 1fr; column-gap:4rem; }
.feat { display:grid; grid-template-columns:11rem 1fr; gap:1.5rem; padding:1.7rem 0; border-top:1px solid var(--line); }
.feat h3 { font-size:1.05rem; font-weight:600; color:var(--ink); margin:0; }
.feat p { font-size:.97rem; line-height:1.7; color:var(--mute); margin:0; font-weight:300; }

/* specs */
.specs { display:grid; grid-template-columns:repeat(4, 1fr); border:1px solid var(--line); border-radius:6px; margin-top:6rem; position:relative; z-index:2; }
.spec { padding:1.8rem 1.6rem; }
.spec + .spec { border-left:1px solid var(--line); }
.spec b { font-family:var(--serif); font-weight:400; font-size:2.6rem; color:var(--ink); display:block; line-height:1; }
.spec span { font-size:.88rem; color:var(--mute); display:block; margin-top:.6rem; }

/* closing */
.closing { padding:7rem 0 2rem 0; position:relative; z-index:2; }
.closing h2 { font-family:var(--serif) !important; font-weight:400; font-size:clamp(2.4rem, 5vw, 4rem); line-height:1.02; color:var(--ink); margin:0 0 1rem 0; max-width:34rem; }
.closing p { color:var(--mute); font-size:1.05rem; margin:0 0 1.6rem 0; font-weight:300; }

/* ── BUTTON ── */
.stButton > button {
  background: var(--beam) !important; color:#05080f !important; border:none !important; border-radius:8px !important;
  padding:.95rem 1.6rem !important; font-family:var(--sans) !important; font-weight:700 !important; font-size:.98rem !important;
  transition: box-shadow .25s ease, transform .25s ease !important; position:relative; z-index:2;
}
.stButton > button:hover { box-shadow:0 0 0 1px var(--beam), 0 8px 40px rgba(143,211,255,.45) !important; transform:translateY(-2px); color:#05080f !important; }
.stButton > button:focus-visible { outline:2px solid var(--amber) !important; outline-offset:3px; }

/* ── FOOTER ── */
.foot { margin-top:5rem; padding-top:1.8rem; border-top:1px solid var(--line); display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem; font-size:.85rem; color:var(--mute); position:relative; z-index:2; }

/* ── RESPONSIVE ── */
@media (max-width: 860px) {
  .block-container { padding:0 1.25rem 3rem 1.25rem !important; }
  .nav-links { display:none; }
  .hero { grid-template-columns:1fr; padding-top:3rem; gap:1rem; }
  .pulsar { margin:0 auto; width:min(80%, 340px); }
  .steps, .feats, .specs { grid-template-columns:1fr; }
  .step, .step + .step { padding:1.6rem 0 0 0; border-left:none; }
  .feat { grid-template-columns:1fr; gap:.4rem; }
  .spec + .spec { border-left:none; border-top:1px solid var(--line); }
}
@media (prefers-reduced-motion: reduce) {
  .pulsar .beams, .pulsar .ring { animation:none; }
  .pulsar .ring { opacity:.3; width:60%; height:60%; }
  .wave path { animation:none; stroke-dashoffset:0; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────
html("""
<div class="nav">
  <div class="brand"><i></i>Cryptorian</div>
  <div class="nav-links"><span>How it works</span><span>Features</span><span>Specs</span></div>
</div>
""")

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
html("""
<div class="hero">
  <div>
    <h1>Your message,<br>sung by a <em>dead star.</em></h1>
    <p class="lead">Cryptorian turns text into the pulse of a neutron star. It sounds like deep space to everyone, and only the right key can turn it back into words.</p>
  </div>
  <div class="pulsar">
    <div class="ring"></div><div class="ring"></div><div class="ring"></div>
    <div class="beams"></div>
    <div class="core"></div>
  </div>
</div>
""")

c1, c2 = st.columns([1, 3])
with c1:
    if st.button("Start encrypting", use_container_width=True, key="hero_btn"):
        st.info("The encryption page will be added soon.")

html(f"""
<div class="wave">
  <svg viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="{PULSES}"/></svg>
  <div class="wave-cap"><span>Text in</span><span>Neutron star pulses out</span></div>
</div>
""")

# ─────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────
html("""
<div class="sec">
  <h2>Three steps from words to a star.</h2>
  <p class="sub">No account, no upload. Everything happens in your session.</p>
  <div class="steps">
    <div class="step"><b>1</b><h3>Write your message</h3><p>Type up to 2,000 characters. Letters, digits and symbols are all supported.</p></div>
    <div class="step"><b>2</b><h3>Choose a secret key</h3><p>The key reshuffles every character's sound, so the same text sounds different with every key.</p></div>
    <div class="step"><b>3</b><h3>Download the audio</h3><p>Save it as WAV or FLAC and share it anywhere. Only your key can decode it.</p></div>
  </div>
</div>
""")

# ─────────────────────────────────────────────
# FEATURES
# ─────────────────────────────────────────────
html("""
<div class="sec">
  <h2>Built so the audio gives nothing away.</h2>
  <p class="sub">The message is not hidden inside a sound file. The message is the sound.</p>
  <div class="feats">
    <div class="feat"><h3>Neutron star sound</h3><p>Every pulse is modeled on a real neutron star recording, so the result passes as cosmic noise.</p></div>
    <div class="feat"><h3>91 unique signatures</h3><p>Each letter, digit and symbol has its own sonic signature. No two are alike.</p></div>
    <div class="feat"><h3>Key shuffling</h3><p>Your key reorders all signatures. Without it, the audio cannot be read.</p></div>
    <div class="feat"><h3>Built-in length header</h3><p>The message length travels inside the audio, so decryption knows exactly where to stop.</p></div>
    <div class="feat"><h3>WAV or FLAC</h3><p>Use WAV for universal playback or FLAC for files up to 80% smaller.</p></div>
    <div class="feat"><h3>Nothing stored</h3><p>Your text, key and audio are processed in memory and never saved or sent anywhere.</p></div>
  </div>
</div>
""")

# ─────────────────────────────────────────────
# SPECS
# ─────────────────────────────────────────────
html("""
<div class="specs">
  <div class="spec"><b>91</b><span>Character signatures</span></div>
  <div class="spec"><b>2,000</b><span>Characters per message</span></div>
  <div class="spec"><b>80%</b><span>Smaller files with FLAC</span></div>
  <div class="spec"><b>2</b><span>Export formats</span></div>
</div>
""")

# ─────────────────────────────────────────────
# CLOSING
# ─────────────────────────────────────────────
html("""
<div class="closing">
  <h2>Send something only one person can hear.</h2>
  <p>Write a message, pick a key, and let the star carry it.</p>
</div>
""")

c1, c2 = st.columns([1, 3])
with c1:
    if st.button("Encrypt a message", use_container_width=True, key="cta_btn"):
        st.info("The encryption page will be added soon.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
html("""
<div class="foot">
  <span>Cryptorian · 2026</span>
  <span>Sound-based encryption</span>
</div>
""")
