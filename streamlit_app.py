import base64
import math
import random

import streamlit as st

st.set_page_config(
    page_title="CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html(code):
    clean = " ".join(line.strip() for line in code.split("\n") if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def svg_img(svg, cls, alt):
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<img class="{cls}" alt="{alt}" src="data:image/svg+xml;base64,{b64}"/>'


# ═══════════════════════════════════════════════════════════════
# ART 1 — NEUTRON STAR WITH RADIO WAVES
# ═══════════════════════════════════════════════════════════════
def star_art():
    rnd = random.Random(7)

    # Starfield
    stars = ""
    for _ in range(70):
        x, y = rnd.randint(0, 800), rnd.randint(0, 800)
        r = rnd.uniform(0.4, 1.6)
        o = rnd.uniform(0.2, 0.9)
        stars += f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="#fff" opacity="{o:.2f}"/>'

    # Neutron sphere surface (lat/long lines)
    sph = ""
    for a in range(0, 180, 20):
        rx = 90 * abs(math.cos(math.radians(a)))
        sph += f'<ellipse cx="400" cy="400" rx="{rx:.1f}" ry="90"/>'
    for lat in range(-80, 81, 20):
        r = 90 * math.cos(math.radians(lat))
        y = 400 - 90 * math.sin(math.radians(lat))
        sph += f'<ellipse cx="400" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.22:.1f}"/>'

    # Magnetic dipole field lines
    field = ""
    for s in (150, 220, 300, 380, 460):
        field += f'<path d="M400 310 C{400 + s} 150 {400 + s} 650 400 490" fill="none"/>'
        field += f'<path d="M400 310 C{400 - s} 150 {400 - s} 650 400 490" fill="none"/>'

    # Radio waves (concentric)
    waves = ""
    for i in range(8):
        r = 110 + i * 42
        waves += f'<circle cx="400" cy="400" r="{r}" fill="none" stroke="#00ff88" stroke-opacity="{0.5 - i * 0.05:.2f}" stroke-width="1.2" stroke-dasharray="2 10"/>'

    # Orbiting particles
    particles = ""
    for i in range(12):
        angle = i * 30
        particles += f'<g class="rot-{i % 3}" style="transform-origin:400px 400px"><rect x="{400 + 260}" y="396" width="6" height="6" fill="#00ff88" transform="rotate({angle} 400 400)"/></g>'

    # Sound waveform below
    wave = ""
    for i in range(40):
        h = 8 + int(30 * abs(math.sin(i * 0.6 + rnd.random())))
        x = 80 + i * 16
        wave += f'<rect x="{x}" y="{700 - h / 2:.0f}" width="4" height="{h}" rx="2" fill="#00d4ff" opacity="{0.4 + 0.5 * abs(math.sin(i * 0.4)):.2f}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
<defs>
<radialGradient id="halo"><stop offset="0" stop-color="#00d4ff" stop-opacity=".35"/><stop offset=".55" stop-color="#00ff88" stop-opacity=".12"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>
<radialGradient id="core"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#baffd9"/><stop offset=".55" stop-color="#00ff88" stop-opacity=".9"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>
<filter id="b1"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="b2"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="b3"><feGaussianBlur stdDeviation="2"/></filter>
</defs>
<style>
.rot-0 {{ animation: spin 40s linear infinite; }}
.rot-1 {{ animation: spin 60s linear infinite reverse; }}
.rot-2 {{ animation: spin 80s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.wave1 {{ animation: wavePulse 3s ease-in-out infinite; transform-origin: 400px 400px; }}
.wave2 {{ animation: wavePulse 3s ease-in-out infinite 0.5s; transform-origin: 400px 400px; }}
.wave3 {{ animation: wavePulse 3s ease-in-out infinite 1s; transform-origin: 400px 400px; }}
@keyframes wavePulse {{ 0%,100% {{ opacity: .2; transform: scale(.95); }} 50% {{ opacity: 1; transform: scale(1.05); }} }}
.coreGlow {{ animation: corePulse 2s ease-in-out infinite; transform-origin: 400px 400px; }}
@keyframes corePulse {{ 0%,100% {{ opacity: .85; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.08); }} }}
.soundPulse {{ animation: sp 1.5s ease-in-out infinite; }}
@keyframes sp {{ 0%,100% {{ opacity: .5; }} 50% {{ opacity: 1; }} }}
</style>

<!-- Starfield -->
<g>{stars}</g>

<!-- Outer halo -->
<circle cx="400" cy="400" r="380" fill="url(#halo)" filter="url(#b2)"/>

<!-- Radio waves -->
<g class="wave1">{waves}</g>
<g class="wave2" opacity=".6">{waves}</g>
<g class="wave3" opacity=".4">{waves}</g>

<!-- Magnetic field lines -->
<g stroke="#00d4ff" stroke-opacity=".4" stroke-width="1.2" filter="url(#b3)">{field}</g>
<g stroke="#00ff88" stroke-opacity=".2" stroke-width="1">{field}</g>

<!-- Equatorial ring -->
<ellipse cx="400" cy="400" rx="330" ry="60" fill="none" stroke="#00d4ff" stroke-width="1" opacity=".3" stroke-dasharray="4 8"/>
<ellipse cx="400" cy="400" rx="240" ry="44" fill="none" stroke="#00ff88" stroke-width="1" opacity=".25" stroke-dasharray="2 6"/>

<!-- Orbiting particles -->
<g>{particles}</g>

<!-- Neutron star surface -->
<g fill="none" stroke="#00ff88" stroke-opacity=".9" stroke-width="1.2">{sph}</g>

<!-- Core -->
<circle class="coreGlow" cx="400" cy="400" r="110" fill="url(#core)" filter="url(#b1)"/>
<circle cx="400" cy="400" r="22" fill="#fff"/>
<circle cx="400" cy="400" r="42" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="1"/>

<!-- Sound waveform -->
<g class="soundPulse">{wave}</g>
<line x1="80" y1="700" x2="720" y2="700" stroke="#00d4ff" stroke-opacity=".25" stroke-width="1"/>
<text x="400" y="755" font-family="monospace" font-size="10" fill="#00ff88" opacity=".5" text-anchor="middle" letter-spacing="6">RADIO PULSE SIGNAL</text>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 2 — ENCRYPTION (data particles)
# ═══════════════════════════════════════════════════════════════
def crypto_art():
    rnd = random.Random(5)

    # Data particles (letters/digits) flowing
    particles = ""
    for i in range(60):
        angle = rnd.uniform(0, 360)
        radius = rnd.uniform(80, 220)
        x = 260 + radius * math.cos(math.radians(angle))
        y = 200 + radius * math.sin(math.radians(angle))
        ch = rnd.choice("0123456789ABCDEF")
        size = rnd.uniform(8, 13)
        o = rnd.uniform(0.2, 0.9)
        delay = rnd.uniform(0, 3)
        particles += f'<text x="{x:.0f}" y="{y:.0f}" font-family="monospace" font-size="{size:.1f}" fill="#00ff88" opacity="{o:.2f}" style="animation-delay:{delay:.2f}s">{ch}</text>'

    # Incoming data streams (left)
    left_stream = ""
    for i in range(4):
        y = 60 + i * 40
        for j in range(8):
            ch = rnd.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            left_stream += f'<text x="{20 + j * 18}" y="{y}" font-family="monospace" font-size="12" fill="#00ff88" opacity="{0.2 + j * 0.08:.2f}">{ch}</text>'

    # Outgoing data streams (right)
    right_stream = ""
    for i in range(4):
        y = 60 + i * 40
        for j in range(8):
            ch = rnd.choice("0123456789ABCDEF")
            right_stream += f'<text x="{360 + j * 18}" y="{y}" font-family="monospace" font-size="12" fill="#00d4ff" opacity="{0.2 + j * 0.08:.2f}">{ch}</text>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400">
<defs>
<radialGradient id="glow"><stop offset="0" stop-color="#00ff88" stop-opacity=".55"/><stop offset=".5" stop-color="#00d4ff" stop-opacity=".15"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#00ff88" stop-opacity="0"/><stop offset=".5" stop-color="#00ff88" stop-opacity=".9"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<style>
.streamL text {{ animation: fadeIn 2s ease-in-out infinite alternate; }}
.streamR text {{ animation: fadeIn 2s ease-in-out infinite alternate-reverse; }}
@keyframes fadeIn {{ from {{ opacity: .15; }} to {{ opacity: .8; }} }}
.ring1 {{ transform-origin: 260px 200px; animation: spin 30s linear infinite; }}
.ring2 {{ transform-origin: 260px 200px; animation: spin 20s linear infinite reverse; }}
.ring3 {{ transform-origin: 260px 200px; animation: spin 45s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.corePulse {{ transform-origin: 260px 200px; animation: cp 1.8s ease-in-out infinite; }}
@keyframes cp {{ 0%,100% {{ opacity: .7; transform: scale(.92); }} 50% {{ opacity: 1; transform: scale(1.06); }} }}
.particles text {{ animation: pf 4s ease-in-out infinite; }}
@keyframes pf {{ 0%,100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
</style>

<rect width="520" height="400" fill="#02060a"/>

<!-- Incoming data -->
<g class="streamL" font-family="monospace">{left_stream}</g>

<!-- Central glow -->
<circle cx="260" cy="200" r="200" fill="url(#glow)" filter="url(#bl)"/>

<!-- Encryption rings -->
<circle class="ring1" cx="260" cy="200" r="175" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-dasharray="2 14" opacity=".7"/>
<circle class="ring2" cx="260" cy="200" r="140" fill="none" stroke="#00ff88" stroke-width="1.2" stroke-dasharray="40 8 4 8" opacity=".6"/>
<circle class="ring3" cx="260" cy="200" r="105" fill="none" stroke="#7b2ff7" stroke-width="1.5" stroke-dasharray="6 12" opacity=".55"/>

<!-- Connecting beams -->
<line x1="40" y1="200" x2="180" y2="200" stroke="url(#beam)" stroke-width="2"/>
<line x1="340" y1="200" x2="480" y2="200" stroke="url(#beam)" stroke-width="2"/>

<!-- Central encryption core -->
<circle class="corePulse" cx="260" cy="200" r="70" fill="none" stroke="#00ff88" stroke-width="2"/>
<circle cx="260" cy="200" r="50" fill="none" stroke="#00d4ff" stroke-width="1" opacity=".6"/>
<circle cx="260" cy="200" r="20" fill="#00ff88" opacity=".25"/>
<circle cx="260" cy="200" r="6" fill="#fff"/>

<!-- Outgoing encrypted data -->
<g class="streamR" font-family="monospace">{right_stream}</g>

<!-- Floating data particles -->
<g class="particles" font-family="monospace" font-weight="bold">{particles}</g>

<!-- Frame -->
<rect x="1" y="1" width="518" height="398" fill="none" stroke="#00ff88" stroke-opacity=".25"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 3 — TEXT → SOUND → STAR (bidirectional)
# ═══════════════════════════════════════════════════════════════
def pipeline_art():
    rnd = random.Random(3)

    # Left: text blocks (abstract glyphs, no readable words)
    left_glyphs = ""
    for r in range(5):
        y = 90 + r * 26
        for c in range(6):
            w = rnd.randint(6, 14)
            left_glyphs += f'<rect x="{30 + c * 22}" y="{y}" width="{w}" height="4" rx="2" fill="#00ff88" opacity="{0.25 + 0.15 * c:.2f}"/>'
            left_glyphs += f'<rect x="{30 + c * 22}" y="{y + 8}" width="{rnd.randint(8, 16)}" height="3" rx="1.5" fill="#00ff88" opacity="{0.15 + 0.1 * r:.2f}"/>'

    # Right: sound waveform blocks
    right_glyphs = ""
    for r in range(5):
        y = 90 + r * 26
        for c in range(6):
            h = 4 + int(8 * abs(math.sin(r * 1.7 + c * 0.9)))
            right_glyphs += f'<rect x="{360 + c * 22}" y="{y + (8 - h) / 2:.0f}" width="10" height="{h}" rx="2" fill="#00d4ff" opacity="{0.3 + 0.1 * c:.2f}"/>'
            right_glyphs += f'<rect x="{360 + c * 22 + 2}" y="{y + 12}" width="6" height="3" rx="1.5" fill="#00d4ff" opacity="{0.15 + 0.1 * r:.2f}"/>'

    # Waveform bars in middle (top path)
    bars_top = ""
    for i in range(26):
        h = 6 + int(28 * abs(math.sin(i * 0.6 + rnd.random())))
        x = 60 + i * 16
        bars_top += f'<rect x="{x}" y="{250 - h / 2:.0f}" width="5" height="{h}" rx="2" fill="#00ff88" opacity="{0.35 + 0.5 * abs(math.sin(i * 0.5)):.2f}"/>'

    # Waveform bars in middle (bottom path)
    bars_bot = ""
    for i in range(26):
        h = 6 + int(28 * abs(math.sin(i * 0.6 + rnd.random())))
        x = 60 + i * 16
        bars_bot += f'<rect x="{x}" y="{450 - h / 2:.0f}" width="5" height="{h}" rx="2" fill="#00d4ff" opacity="{0.35 + 0.5 * abs(math.sin(i * 0.4)):.2f}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 560">
<defs>
<radialGradient id="core"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#00ff88" stop-opacity=".85"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>
<linearGradient id="arrT" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#00ff88" stop-opacity="0"/><stop offset=".5" stop-color="#00ff88"/><stop offset="1" stop-color="#00d4ff" stop-opacity="0"/></linearGradient>
<linearGradient id="arrB" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#00d4ff" stop-opacity="0"/><stop offset=".5" stop-color="#00d4ff"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></linearGradient>
<filter id="blurP"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<style>
.flowT {{ animation: flow 3s linear infinite; }}
.flowB {{ animation: flow 3s linear infinite reverse; }}
@keyframes flow {{ to {{ stroke-dashoffset: -30; }} }}
.corePulse {{ transform-origin: 260px 350px; animation: cp 1.8s ease-in-out infinite; }}
@keyframes cp {{ 0%,100% {{ opacity: .75; transform: scale(.9); }} 50% {{ opacity: 1; transform: scale(1.1); }} }}
.rot {{ transform-origin: 260px 350px; animation: spin 12s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.barsT rect {{ animation: barP 1.6s ease-in-out infinite; }}
.barsB rect {{ animation: barP 1.6s ease-in-out infinite reverse; }}
@keyframes barP {{ 0%,100% {{ opacity: .4; }} 50% {{ opacity: 1; }} }}
</style>

<rect width="520" height="560" fill="#02060a"/>

<!-- TOP PATH: TEXT → SOUND -->

<!-- Input text glyphs (top-left) -->
<g>{left_glyphs}</g>
<text x="260" y="55" font-family="monospace" font-size="9" fill="#00ff88" opacity=".55" text-anchor="middle" letter-spacing="5">TEXT DATA</text>

<!-- Arrow right → -->
<line class="flowT" x1="170" y1="130" x2="350" y2="130" stroke="url(#arrT)" stroke-width="2" stroke-dasharray="6 8"/>
<polygon points="350,124 370,130 350,136" fill="#00d4ff"/>

<!-- Output waveform (top-right) -->
<g>{right_glyphs}</g>
<text x="260" y="55" font-family="monospace" font-size="9" fill="#00d4ff" opacity=".55" text-anchor="middle" letter-spacing="5">SOUND DATA</text>

<!-- Middle waveform (top) -->
<rect x="40" y="215" width="440" height="70" fill="none" stroke="#00ff88" stroke-opacity=".2" rx="8"/>
<g class="barsT">{bars_top}</g>
<text x="260" y="300" font-family="monospace" font-size="9" fill="#00ff88" opacity=".5" text-anchor="middle" letter-spacing="5">WAVEFORM</text>

<!-- Central neutron star core -->
<circle class="corePulse" cx="260" cy="350" r="42" fill="url(#core)" filter="url(#blurP)"/>
<circle class="rot" cx="260" cy="350" r="46" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-dasharray="6 5"/>
<circle cx="260" cy="350" r="6" fill="#fff"/>
<text x="260" y="410" font-family="monospace" font-size="9" fill="#00ff88" opacity=".55" text-anchor="middle" letter-spacing="5">STAR CORE</text>

<!-- Middle waveform (bottom) -->
<rect x="40" y="415" width="440" height="70" fill="none" stroke="#00d4ff" stroke-opacity=".2" rx="8"/>
<g class="barsB">{bars_bot}</g>
<text x="260" y="500" font-family="monospace" font-size="9" fill="#00d4ff" opacity=".5" text-anchor="middle" letter-spacing="5">WAVEFORM (reverse)</text>

<!-- BOTTOM PATH: SOUND → TEXT -->

<!-- Arrow left ← -->
<line class="flowB" x1="350" y1="130" x2="170" y2="130" stroke="url(#arrB)" stroke-width="2" stroke-dasharray="6 8"/>

<!-- Frame -->
<rect x="1" y="1" width="518" height="558" fill="none" stroke="#00ff88" stroke-opacity=".25"/>
</svg>"""


STAR = svg_img(star_art(), "hero-art", "Neutron star with radio waves")
NET = svg_img(crypto_art(), "art", "Encryption data flow")
PIPE = svg_img(pipeline_art(), "art", "Text to sound pipeline")

# ═══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp { background:#000 !important; color:#fff; -webkit-font-smoothing:antialiased; overflow-x:hidden; }
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown div { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
.block-container { max-width:1320px !important; padding:0 3rem 5rem 3rem !important; position:relative; z-index:3; }

.bg-layer { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.bg-orb { position:absolute; border-radius:50%; filter:blur(140px); will-change:transform; }
.orb-1 { width:700px; height:700px; background:radial-gradient(circle,#00ff88 0%,transparent 70%); top:-280px; left:-180px; opacity:.38; animation:f1 22s ease-in-out infinite; }
.orb-2 { width:600px; height:600px; background:radial-gradient(circle,#00d4ff 0%,transparent 70%); top:35%; right:-220px; opacity:.26; animation:f2 28s ease-in-out infinite; }
.orb-3 { width:800px; height:800px; background:radial-gradient(circle,#7b2ff7 0%,transparent 70%); bottom:-380px; left:25%; opacity:.22; animation:f3 32s ease-in-out infinite; }
@keyframes f1 { 50% { transform:translate(120px,100px) scale(1.15); } }
@keyframes f2 { 50% { transform:translate(-140px,-120px) scale(1.2); } }
@keyframes f3 { 50% { transform:translate(100px,-100px) scale(1.1); } }
.bg-grid { position:absolute; inset:0; background-image:linear-gradient(rgba(0,255,136,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,136,.05) 1px,transparent 1px); background-size:70px 70px; mask-image:radial-gradient(ellipse 90% 70% at 50% 40%,#000 15%,transparent 80%); animation:gridShift 60s linear infinite; }
@keyframes gridShift { to { background-position:70px 70px; } }
.particle { position:absolute; width:3px; height:3px; background:#00ff88; border-radius:50%; box-shadow:0 0 10px #00ff88; animation:rise linear infinite; }
@keyframes rise { 0% { transform:translateY(100vh) scale(0); opacity:0; } 10%,90% { opacity:1; } 100% { transform:translateY(-100px) scale(1); opacity:0; } }

.nav { display:flex; justify-content:space-between; align-items:center; padding:1.3rem 3rem; margin:0 -3rem; position:relative; z-index:100; backdrop-filter:blur(24px); background:rgba(0,0,0,.6); border-bottom:1px solid rgba(255,255,255,.08); }
.nav-brand { display:flex; align-items:center; gap:.85rem; font-family:'Orbitron', sans-serif; font-weight:900; font-size:1.05rem; letter-spacing:.3em; color:#00ff88; text-shadow:0 0 30px rgba(0,255,136,.9); }
.nav-brand::before { content:''; width:11px; height:11px; background:#00ff88; box-shadow:0 0 25px #00ff88; transform:rotate(45deg); animation:spin 8s linear infinite; }
@keyframes spin { to { transform:rotate(405deg); } }
.nav-status { display:flex; align-items:center; gap:.5rem; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; color:#00ff88; }
.nav-dot { width:7px; height:7px; border-radius:50%; background:#00ff88; box-shadow:0 0 14px #00ff88; animation:blink 1.8s infinite; }
@keyframes blink { 50% { opacity:.3; } }

.hero { padding:6.5rem 0 3rem 0; text-align:center; position:relative; }
.hero-badge { display:inline-flex; align-items:center; gap:.7rem; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.3em; text-transform:uppercase; color:rgba(0,255,136,.9); padding:.7rem 1.8rem; border:1px solid rgba(0,255,136,.3); border-radius:100px; background:rgba(0,255,136,.05); margin-bottom:2.6rem; }
.hero-badge i { width:7px; height:7px; border-radius:50%; background:#00ff88; box-shadow:0 0 14px #00ff88; animation:blink 1.8s infinite; }

.hero-name { font-family:'Orbitron', sans-serif !important; font-weight:900; font-size:clamp(2rem, 9vw, 7rem); line-height:1; letter-spacing:.08em; margin:0 auto 2rem auto; padding:0; white-space:nowrap; background:linear-gradient(180deg,#fff 0%,#00ff88 60%,#00d4ff 100%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 70px rgba(0,255,136,.65)); animation:glow 4s ease-in-out infinite; }
@keyframes glow { 50% { filter:drop-shadow(0 0 110px rgba(0,255,136,.95)); } }

.hero-tagline { font-family:'JetBrains Mono', monospace; font-size:clamp(.7rem, 1.3vw, .9rem); letter-spacing:.22em; text-transform:uppercase; color:rgba(0,255,136,.9); text-shadow:0 0 20px rgba(0,255,136,.6); margin:0 auto 0.9rem auto; max-width:950px; line-height:1.9; }

.hero-art { display:block; width:min(100%,640px); margin:2.5rem auto 0 auto; }
.art { display:block; width:100%; max-width:520px; margin-top:1rem; border-radius:18px; border:1px solid rgba(0,255,136,.2); box-shadow:0 0 70px rgba(0,255,136,.08); }

.stats-strip { display:grid; grid-template-columns:repeat(4,1fr); margin:4rem 0 2rem 0; border:1px solid rgba(0,255,136,.18); border-radius:20px; background:linear-gradient(145deg,rgba(0,255,136,.05),rgba(255,255,255,.01)); backdrop-filter:blur(20px); overflow:hidden; }
.stat-item { text-align:center; padding:2.2rem 1rem; }
.stat-item + .stat-item { border-left:1px solid rgba(255,255,255,.08); }
.stat-val { font-family:'JetBrains Mono', monospace; font-size:2rem; font-weight:800; color:#00ff88; text-shadow:0 0 25px rgba(0,255,136,.6); display:block; margin-bottom:.6rem; }
.stat-lbl { font-family:'JetBrains Mono', monospace; font-size:.65rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.45); }

.sec { padding:7rem 0 0 0; position:relative; }
.sec-grid { display:grid; grid-template-columns:1fr 1.2fr; gap:5rem; align-items:start; }

.sec-title { font-family:'Orbitron', sans-serif !important; font-weight:900; font-size:clamp(1.3rem, 3vw, 2.4rem); line-height:1.2; letter-spacing:.12em; color:#00ff88; text-shadow:0 0 40px rgba(0,255,136,.6), 0 0 80px rgba(0,255,136,.3); margin:0 0 2rem 0; text-transform:uppercase; }

.text-block { font-family:'Space Grotesk', sans-serif; font-size:1.08rem; color:rgba(255,255,255,.72); line-height:2; font-weight:300; margin:0 0 2rem 0; padding-left:1.8rem; border-left:2px solid rgba(0,255,136,.3); transition:all .4s ease; }
.text-block:hover { border-left-color:#00ff88; color:rgba(255,255,255,.95); padding-left:2.4rem; }
.text-block strong { color:#00ff88; font-weight:600; text-shadow:0 0 25px rgba(0,255,136,.6); }

.feat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.4rem; margin-top:3rem; }
.feat { position:relative; padding:2.4rem 2rem; background:linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); border:1px solid rgba(255,255,255,.08); border-radius:16px; overflow:hidden; transition:all .45s cubic-bezier(.4,0,.2,1); }
.feat::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,255,136,.9),transparent); opacity:0; transition:opacity .45s; }
.feat:hover { transform:translateY(-8px); border-color:rgba(0,255,136,.4); box-shadow:0 25px 70px rgba(0,0,0,.6), 0 0 90px rgba(0,255,136,.14); }
.feat:hover::before { opacity:1; }
.feat-icon { width:54px; height:54px; display:flex; align-items:center; justify-content:center; background:linear-gradient(145deg,rgba(0,255,136,.16),rgba(0,255,136,.03)); border:1px solid rgba(0,255,136,.3); border-radius:14px; font-size:1.5rem; color:#00ff88; margin-bottom:1.5rem; text-shadow:0 0 20px rgba(0,255,136,.6); transition:all .45s; }
.feat:hover .feat-icon { box-shadow:0 0 30px rgba(0,255,136,.4); transform:scale(1.08) rotate(-5deg); }
.feat-t { font-family:'JetBrains Mono', monospace; font-size:.9rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#fff; margin-bottom:.9rem; }
.feat-d { font-family:'Space Grotesk', sans-serif; font-size:.97rem; color:rgba(255,255,255,.6); line-height:1.8; font-weight:300; }

.quote { max-width:900px; margin:7rem auto 0 auto; padding:3rem 3rem 3rem 4rem; border-left:4px solid #00ff88; background:linear-gradient(90deg,rgba(0,255,136,.07),transparent); border-radius:0 20px 20px 0; position:relative; }
.quote::before { content:'"'; position:absolute; top:-18px; left:20px; font-family:'Orbitron', sans-serif; font-size:5rem; color:rgba(0,255,136,.3); line-height:1; }
.quote-text { font-family:'Space Grotesk', sans-serif; font-size:1.4rem; font-weight:300; font-style:italic; color:rgba(255,255,255,.88); line-height:1.8; margin-bottom:1.4rem; }
.quote-author { font-family:'JetBrains Mono', monospace; font-size:.75rem; letter-spacing:.3em; text-transform:uppercase; color:rgba(0,255,136,.75); }

.cta { padding:6rem 3rem; text-align:center; border:1px solid rgba(0,255,136,.3); border-radius:28px; background:radial-gradient(ellipse at top,rgba(0,255,136,.18),transparent 60%),linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); position:relative; overflow:hidden; margin-top:7rem; }
.cta::before { content:''; position:absolute; inset:0; background-image:linear-gradient(rgba(0,255,136,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,136,.07) 1px,transparent 1px); background-size:40px 40px; mask-image:radial-gradient(ellipse at center,#000 20%,transparent 70%); }
.cta-t { font-family:'JetBrains Mono', monospace; font-weight:500; font-size:clamp(1.15rem, 2.8vw, 2.1rem); text-transform:uppercase; letter-spacing:.16em; line-height:1.5; color:#00ff88; text-shadow:0 0 28px rgba(0,255,136,.45); margin-bottom:1rem; position:relative; }
.cta-d { font-family:'Space Grotesk', sans-serif; font-size:1.05rem; color:rgba(255,255,255,.62); position:relative; font-weight:300; }

.stButton > button { background:linear-gradient(145deg,rgba(0,255,136,.12),rgba(0,255,136,.03)) !important; color:#00ff88 !important; border:1px solid rgba(0,255,136,.55) !important; border-radius:12px !important; padding:1.1rem 2rem !important; font-family:'JetBrains Mono', monospace !important; font-weight:700 !important; font-size:.8rem !important; letter-spacing:.2em !important; text-transform:uppercase !important; transition:all .4s cubic-bezier(.4,0,.2,1) !important; width:100% !important; position:relative; z-index:3; }
.stButton > button:hover { color:#000 !important; background:#00ff88 !important; border-color:#00ff88 !important; box-shadow:0 0 50px rgba(0,255,136,.7), 0 0 100px rgba(0,255,136,.35) !important; transform:translateY(-3px); }

.foot { margin-top:7rem; padding-top:2.5rem; border-top:1px solid rgba(255,255,255,.08); display:flex; justify-content:space-between; align-items:center; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.35); flex-wrap:wrap; gap:1rem; }
.foot-brand { color:rgba(0,255,136,.95); text-shadow:0 0 25px rgba(0,255,136,.6); font-weight:700; }

::-webkit-scrollbar { width:8px; } ::-webkit-scrollbar-track { background:#000; }
::-webkit-scrollbar-thumb { background:rgba(0,255,136,.4); border-radius:4px; }

@media (max-width:980px) {
  .sec-grid { grid-template-columns:1fr; gap:1rem; }
  .feat-grid { grid-template-columns:1fr 1fr; }
}
@media (max-width:700px) {
  .block-container { padding:0 1.25rem 4rem 1.25rem !important; }
  .nav { padding:1.1rem 1.25rem; margin:0 -1.25rem; }
  .hero { padding-top:4rem; }
  .hero-badge { letter-spacing:.12em; font-size:.62rem; padding:.7rem 1.2rem; line-height:1.7; }
  .hero-name { letter-spacing:.04em; }
  .hero-tagline { letter-spacing:.15em; font-size:.72rem; }
  .stats-strip, .feat-grid { grid-template-columns:1fr; }
  .stat-item + .stat-item { border-left:none; border-top:1px solid rgba(255,255,255,.08); }
  .quote { padding:2rem 1.5rem; }
  .cta { padding:4rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ═══ BACKGROUND ═══
html("""
<div class="bg-layer">
    <div class="bg-grid"></div>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>
    <div class="particle" style="left:10%;animation-duration:12s;animation-delay:0s;"></div>
    <div class="particle" style="left:25%;animation-duration:15s;animation-delay:2s;"></div>
    <div class="particle" style="left:45%;animation-duration:10s;animation-delay:4s;"></div>
    <div class="particle" style="left:65%;animation-duration:14s;animation-delay:1s;"></div>
    <div class="particle" style="left:85%;animation-duration:11s;animation-delay:3s;"></div>
    <div class="particle" style="left:55%;animation-duration:13s;animation-delay:5s;"></div>
    <div class="particle" style="left:35%;animation-duration:16s;animation-delay:6s;"></div>
</div>
""")

# ═══ NAV ═══
html("""
<div class="nav">
    <div class="nav-brand">CRYPTORIAN</div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")

# ═══ HERO ═══
html(f"""
<div class="hero">
    <div class="hero-badge"><i></i>DM SAFELY AND SECURE YOUR PRIVACY WITH</div>
    <h1 class="hero-name">CRYPTORIAN</h1>
    <p class="hero-tagline">TURN YOUR WORDS INTO AN ENCRYPTED DEAD STAR'S SOUND</p>
    {STAR}
</div>
""")

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⚡ GET STARTED", use_container_width=True):
        st.info("The encryption page will be added soon.")

# ═══ STATS ═══
html("""
<div class="stats-strip">
    <div class="stat-item"><span class="stat-val">91</span><span class="stat-lbl">SIGNATURES</span></div>
    <div class="stat-item"><span class="stat-val">2000</span><span class="stat-lbl">MAX CHARS</span></div>
    <div class="stat-item"><span class="stat-val">80%</span><span class="stat-lbl">FLAC SAVING</span></div>
    <div class="stat-item"><span class="stat-val">3</span><span class="stat-lbl">SHAPES</span></div>
</div>
""")

# ═══ WHY ENCRYPTION ═══
html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHY ENCRYPTION MATTERS</h2>
        {NET}
    </div>
    <div>
        <p class="text-block">Every message you send carries a piece of you. Your words, your thoughts, your secrets — they travel through networks you don't control, through servers you don't own, through channels that can be intercepted.</p>
        <p class="text-block"><strong>Encryption is not paranoia.</strong> It is the basic right to keep your private life private. It is the difference between a conversation and a broadcast. It is the line between your message and everyone else's business.</p>
        <p class="text-block">In a world where data is currency, encryption is the only true shield. It doesn't hide the fact that you are communicating — it simply ensures that only the intended recipient can understand what is being said.</p>
    </div>
  </div>
</div>
""")

# ═══ QUOTE ═══
html("""
<div class="quote">
    <p class="quote-text">The only way to keep a secret is to make sure no one knows you have one.</p>
    <p class="quote-author">— CRYPTORIAN PRINCIPLE</p>
</div>
""")

# ═══ WHAT IS CRYPTORIAN ═══
html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHAT IS CRYPTORIAN</h2>
        {PIPE}
    </div>
    <div>
        <p class="text-block">Cryptorian is a sound-based encryption system. It takes your message and transforms it into a waveform modeled after the sound of a neutron star — a dead star that pulses in the void, sending signals no one can read.</p>
        <p class="text-block">Every character you write becomes a unique pulse. Every word becomes a rhythm. The final audio file sounds like cosmic noise to anyone who listens — but to the person who holds the key, it is a clear message.</p>
        <p class="text-block"><strong>Cryptorian does not hide the message inside the audio.</strong> It turns the message into the audio itself. The text is no longer text. It is a star's heartbeat.</p>
    </div>
  </div>
</div>
""")

# ═══ FEATURES ═══
html("""
<div class="sec">
    <h2 class="sec-title">BUILT FOR THE PARANOID MIND</h2>
    <div class="feat-grid">
        <div class="feat"><div class="feat-icon">◉</div><div class="feat-t">Neutron Sound</div><div class="feat-d">Your message becomes a waveform modeled after a neutron star's pulse. It sounds like the cosmos — not like data.</div></div>
        <div class="feat"><div class="feat-icon">▣</div><div class="feat-t">Unique Signatures</div><div class="feat-d">Every character — letter, digit, or symbol — has its own sonic signature. No two are ever alike.</div></div>
        <div class="feat"><div class="feat-icon">⬢</div><div class="feat-t">Key Shuffling</div><div class="feat-d">The secret key reorders every signature. The same character produces a different pulse with every key.</div></div>
        <div class="feat"><div class="feat-icon">◆</div><div class="feat-t">Length Header</div><div class="feat-d">The message length is embedded in the audio itself. Decryption knows exactly where the message ends.</div></div>
        <div class="feat"><div class="feat-icon">▲</div><div class="feat-t">Dual Formats</div><div class="feat-d">Export as uncompressed WAV for universal playback, or as compressed FLAC for a much smaller file.</div></div>
        <div class="feat"><div class="feat-icon">○</div><div class="feat-t">Zero Knowledge</div><div class="feat-d">Nothing is stored. Nothing is sent. The entire process happens in memory — invisible to anyone else.</div></div>
    </div>
</div>
""")

# ═══ CTA ═══
html("""
<div class="cta">
    <div class="cta-t">READY TO BECOME A STAR</div>
    <div class="cta-d">Your message is waiting. Your key is your power.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⚡ ENCRYPT A MESSAGE", use_container_width=True, key="cta_btn"):
        st.info("The encryption page will be added soon.")

# ═══ FOOTER ═══
html("""
<div class="foot">
    <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
    <div>SOUND-BASED ENCRYPTION</div>
</div>
""")
