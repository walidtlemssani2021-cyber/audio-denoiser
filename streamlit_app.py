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
# ART 1 — NEUTRON STAR
# ═══════════════════════════════════════════════════════════════
def star_art():
    sph = ""
    for a in (0, 20, 40, 60, 80, 100, 120, 140, 160):
        rx = 80 * abs(math.cos(math.radians(a)))
        sph += f'<ellipse cx="400" cy="400" rx="{rx:.1f}" ry="80"/>'
    for lat in (-80, -60, -40, -20, 0, 20, 40, 60, 80):
        r = 80 * math.cos(math.radians(lat))
        y = 400 - 80 * math.sin(math.radians(lat))
        sph += f'<ellipse cx="400" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.22:.1f}"/>'

    field = ""
    for s in (140, 210, 280, 350):
        field += f'<path d="M400 330 C{400 + s} 200 {400 + s} 600 400 470"/>'
        field += f'<path d="M400 330 C{400 - s} 200 {400 - s} 600 400 470"/>'

    stars = ""
    rnd = random.Random(7)
    for _ in range(50):
        x, y = rnd.randint(0, 800), rnd.randint(0, 800)
        r = rnd.uniform(0.5, 1.8)
        o = rnd.uniform(0.2, 0.9)
        stars += f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="#fff" opacity="{o:.2f}"/>'

    pulses = ""
    for i in range(6):
        r = 120 + i * 40
        pulses += f'<circle cx="400" cy="400" r="{r}" fill="none" stroke="#00ff88" stroke-opacity="{0.4 - i * 0.06:.2f}" stroke-width="1" stroke-dasharray="3 9"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
<defs>
<radialGradient id="halo"><stop offset="0" stop-color="#00d4ff" stop-opacity=".40"/><stop offset=".5" stop-color="#00ff88" stop-opacity=".15"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>
<radialGradient id="core"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#baffd9"/><stop offset=".5" stop-color="#00ff88" stop-opacity=".9"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>
<linearGradient id="jet" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#00ff88" stop-opacity="1"/><stop offset=".4" stop-color="#00d4ff" stop-opacity=".6"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></linearGradient>
<linearGradient id="jet2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00ff88" stop-opacity="1"/><stop offset=".4" stop-color="#00d4ff" stop-opacity=".6"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00d4ff"/><stop offset=".5" stop-color="#00ff88"/><stop offset="1" stop-color="#7b2ff7"/></linearGradient>
<filter id="blur1"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="blur2"><feGaussianBlur stdDeviation="12"/></filter>
</defs>
<style>
.rot1{{transform-origin:400px 400px;animation:spin 40s linear infinite}}
.rot2{{transform-origin:400px 400px;animation:spin 25s linear infinite reverse}}
.rot3{{transform-origin:400px 400px;animation:spin 60s linear infinite}}
.pulse1{{transform-origin:400px 400px;animation:pulse 3s ease-in-out infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:.3;transform:scale(.95)}}50%{{opacity:1;transform:scale(1.05)}}}}
.jet-a{{animation:jetA 2.5s ease-in-out infinite alternate}}
@keyframes jetA{{from{{opacity:.6}}to{{opacity:1}}}}
</style>

<!-- Starfield -->
<g opacity=".8">{stars}</g>

<!-- Outer halo -->
<circle cx="400" cy="400" r="380" fill="url(#halo)"/>

<!-- Pulsing waves -->
<g class="pulse1">{pulses}</g>

<!-- Rotating magnetic field lines -->
<g class="rot1" fill="none" stroke="#00d4ff" stroke-opacity=".35" stroke-width="1.2">{field}</g>

<!-- Polar jets -->
<g transform="rotate(20 400 400)">
<polygon class="jet-a" points="400,380 350,-20 450,-20" fill="url(#jet)"/>
<polygon class="jet-a" points="400,420 350,820 450,820" fill="url(#jet2)"/>
</g>

<!-- Equatorial rings -->
<ellipse cx="400" cy="400" rx="340" ry="70" fill="none" stroke="url(#ring)" stroke-width="12" opacity=".35" filter="url(#blur2)"/>
<ellipse class="rot2" cx="400" cy="400" rx="340" ry="70" fill="none" stroke="url(#ring)" stroke-width="3" stroke-dasharray="50 14"/>
<ellipse class="rot3" cx="400" cy="400" rx="260" ry="54" fill="none" stroke="#00ff88" stroke-width="1.5" stroke-dasharray="6 10" opacity=".85"/>

<!-- Neutron star surface -->
<g fill="none" stroke="#00ff88" stroke-opacity=".85" stroke-width="1.2">{sph}</g>

<!-- Core -->
<circle cx="400" cy="400" r="110" fill="url(#core)" filter="url(#blur1)"/>
<circle class="pulse1" cx="400" cy="400" r="110" fill="url(#core)"/>
<circle cx="400" cy="400" r="22" fill="#fff"/>
<circle cx="400" cy="400" r="40" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>

<!-- Orbit particles -->
<g class="rot1">
<rect x="750" y="396" width="8" height="8" fill="#00ff88"/>
<rect x="42" y="396" width="6" height="6" fill="#00d4ff"/>
</g>
<g class="rot2">
<rect x="700" y="396" width="7" height="7" fill="#7b2ff7"/>
<rect x="93" y="396" width="5" height="5" fill="#00ff88"/>
</g>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 2 — ENCRYPTION
# ═══════════════════════════════════════════════════════════════
def crypto_art():
    rnd = random.Random(5)

    # Data columns (left)
    left_cols = ""
    for c in range(8):
        chars = "".join(
            f'<text x="{10 + c * 22}" y="{20 + r * 24}" opacity="{0.15 + 0.4 * rnd.random():.2f}">{rnd.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")}</text>'
            for r in range(14)
        )
        left_cols += f'<g style="animation-delay:{rnd.random() * 3:.2f}s">{chars}</g>'

    # Encrypted columns (right)
    right_cols = ""
    for c in range(8):
        chars = "".join(
            f'<text x="{340 + c * 22}" y="{20 + r * 24}" opacity="{0.15 + 0.4 * rnd.random():.2f}">{rnd.choice("0123456789ABCDEF")}</text>'
            for r in range(14)
        )
        right_cols += f'<g style="animation-delay:{rnd.random() * 3:.2f}s">{chars}</g>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400">
<defs>
<linearGradient id="shield" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#00d4ff"/>
<stop offset=".5" stop-color="#00ff88"/>
<stop offset="1" stop-color="#7b2ff7"/>
</linearGradient>
<radialGradient id="glow">
<stop offset="0" stop-color="#00ff88" stop-opacity=".45"/>
<stop offset="1" stop-color="#00ff88" stop-opacity="0"/>
</radialGradient>
<linearGradient id="beam" x1="0" x2="1" y1="0" y2="0">
<stop offset="0" stop-color="#00d4ff" stop-opacity="0"/>
<stop offset=".5" stop-color="#00ff88" stop-opacity="1"/>
<stop offset="1" stop-color="#00d4ff" stop-opacity="0"/>
</linearGradient>
<filter id="b1"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="b2"><feGaussianBlur stdDeviation="12"/></filter>
</defs>
<style>
.cols-l g, .cols-r g {{animation: flick 3s ease-in-out infinite alternate}}
@keyframes flick {{from{{opacity:.4}}to{{opacity:1}}}}
.shield-glow {{animation: sg 2.5s ease-in-out infinite alternate}}
@keyframes sg {{from{{opacity:.75}}to{{opacity:1}}}}
.rot-ring {{transform-origin:260px 200px;animation: spin 25s linear infinite}}
.rot-ring2 {{transform-origin:260px 200px;animation: spin 40s linear infinite reverse}}
.lock-body {{animation: lock 1.8s steps(2) infinite}}
@keyframes lock {{50%{{opacity:.85}}}}
.beam1 {{animation: beam 2.2s ease-in-out infinite alternate}}
.beam2 {{animation: beam 2.2s ease-in-out infinite alternate-reverse}}
@keyframes beam {{from{{opacity:.3}}to{{opacity:1}}}}
</style>

<!-- Dark base -->
<rect width="520" height="400" fill="#02060a"/>

<!-- Left data (plain) -->
<g class="cols-l" font-family="monospace" font-size="13" fill="#00ff88">{left_cols}</g>

<!-- Right data (encrypted) -->
<g class="cols-r" font-family="monospace" font-size="13" fill="#00d4ff">{right_cols}</g>

<!-- Central glow -->
<circle cx="260" cy="200" r="180" fill="url(#glow)" filter="url(#b2)"/>

<!-- Rotating rings -->
<circle class="rot-ring" cx="260" cy="200" r="165" fill="none" stroke="#00d4ff" stroke-opacity=".55" stroke-width="2" stroke-dasharray="3 12"/>
<circle class="rot-ring2" cx="260" cy="200" r="140" fill="none" stroke="#00ff88" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="20 6 4 6"/>

<!-- Beams converging -->
<line class="beam1" x1="120" y1="200" x2="200" y2="200" stroke="url(#beam)" stroke-width="2"/>
<line class="beam2" x1="320" y1="200" x2="400" y2="200" stroke="url(#beam)" stroke-width="2"/>

<!-- Shield -->
<g class="shield-glow">
<path d="M260 40 L380 90 V200 C380 280 320 340 260 370 C200 340 140 280 140 200 V90 Z"
      fill="none" stroke="url(#shield)" stroke-width="14" opacity=".45" filter="url(#b1)"/>
<path d="M260 40 L380 90 V200 C380 280 320 340 260 370 C200 340 140 280 140 200 V90 Z"
      fill="#02060a" fill-opacity=".95" stroke="url(#shield)" stroke-width="3"/>
<path d="M260 70 L355 110 V200 C355 265 305 315 260 340 C215 315 165 265 165 200 V110 Z"
      fill="none" stroke="#00ff88" stroke-opacity=".3" stroke-width="1.2"/>
</g>

<!-- Padlock -->
<path d="M232 195 V175 a28 28 0 0 1 56 0 V195" fill="none" stroke="#00ff88" stroke-width="6" stroke-linecap="round"/>
<rect x="212" y="195" width="96" height="76" rx="10" fill="#00ff88" fill-opacity=".15" stroke="#00ff88" stroke-width="4"/>
<g class="lock-body">
<circle cx="260" cy="228" r="8" fill="#fff"/>
<rect x="256.5" y="233" width="7" height="22" rx="3" fill="#fff"/>
</g>

<!-- Frame -->
<rect x="1" y="1" width="518" height="398" fill="none" stroke="#00ff88" stroke-opacity=".25"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 3 — TEXT → SOUND → TEXT
# ═══════════════════════════════════════════════════════════════
def pipeline_art():
    # Left text
    left_text = "HELLO WORLD"
    left_chars = ""
    for i, ch in enumerate(left_text):
        x = 20 + i * 15
        left_chars += f'<text x="{x}" y="80" font-family="monospace" font-size="16" fill="#00ff88" opacity="{0.6 + 0.4 * (i % 3 == 0):.2f}">{ch}</text>'

    # Right text
    right_text = "HELLO WORLD"
    right_chars = ""
    for i, ch in enumerate(right_text):
        x = 20 + i * 15
        right_chars += f'<text x="{x}" y="440" font-family="monospace" font-size="16" fill="#00d4ff" opacity="{0.6 + 0.4 * (i % 3 == 0):.2f}">{ch}</text>'

    # Middle waveform bars
    bars = ""
    rnd = random.Random(3)
    n = 30
    for i in range(n):
        h = 10 + int(40 * abs(math.sin(i * 0.7 + rnd.random())))
        x = 20 + i * 16
        o = 0.4 + 0.5 * abs(math.sin(i * 0.5))
        bars += f'<rect x="{x}" y="{250 - h / 2:.0f}" width="6" height="{h}" rx="2" fill="#00ff88" opacity="{o:.2f}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 520">
<defs>
<radialGradient id="core">
<stop offset="0" stop-color="#fff"/>
<stop offset=".3" stop-color="#00ff88" stop-opacity=".85"/>
<stop offset="1" stop-color="#00ff88" stop-opacity="0"/>
</radialGradient>
<linearGradient id="jetL" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#00d4ff" stop-opacity="0"/>
<stop offset=".5" stop-color="#00ff88" stop-opacity=".9"/>
<stop offset="1" stop-color="#00d4ff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="jetR" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#00d4ff" stop-opacity="0"/>
<stop offset=".5" stop-color="#00d4ff" stop-opacity=".9"/>
<stop offset="1" stop-color="#00d4ff" stop-opacity="0"/>
</linearGradient>
<filter id="blur3"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<style>
.f1{{animation:f 1.4s linear infinite}}
.f2{{animation:f 1.4s linear infinite reverse}}
.w1{{stroke-dasharray:800;stroke-dashoffset:800;animation:w 3s ease-out infinite alternate}}
@keyframes w{{to{{stroke-dashoffset:0}}}}
@keyframes f{{to{{stroke-dashoffset:-20}}}}
.core-pulse{{transform-origin:260px:260px;animation:cp 2s ease-in-out infinite alternate}}
@keyframes cp{{from{{opacity:.7;transform:scale(.9)}}to{{opacity:1;transform:scale(1.05)}}}}
</style>

<rect width="520" height="520" fill="#02060a"/>

<!-- Input text -->
<g>{left_chars}</g>
<text x="260" y="110" font-family="monospace" font-size="9" fill="#00ff88" opacity=".5" text-anchor="middle" letter-spacing="4">TEXT INPUT</text>

<!-- Arrow down -->
<line class="f1" x1="260" y1="130" x2="260" y2="165" stroke="#00ff88" stroke-width="2" stroke-dasharray="6 6"/>
<polygon points="250,163 270,163 260,180" fill="#00ff88"/>

<!-- Waveform area -->
<rect x="10" y="185" width="500" height="150" fill="none" stroke="#00ff88" stroke-opacity=".2" rx="8"/>
<g>{bars}</g>
<text x="260" y="215" font-family="monospace" font-size="9" fill="#00ff88" opacity=".5" text-anchor="middle" letter-spacing="4">WAVEFORM</text>

<!-- Arrow down -->
<line class="f1" x1="260" y1="350" x2="260" y2="385" stroke="#00ff88" stroke-width="2" stroke-dasharray="6 6"/>
<polygon points="250,383 270,383 260,400" fill="#00ff88"/>

<!-- Neutron star core -->
<circle class="core-pulse" cx="260" cy="460" r="40" fill="url(#core)" filter="url(#blur3)"/>
<circle cx="260" cy="460" r="45" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-dasharray="6 5"/>
<circle cx="260" cy="460" r="6" fill="#fff"/>
<rect x="257" y="418" width="6" height="84" fill="url(#jetL)"/>
<rect x="257" y="418" width="6" height="84" fill="url(#jetR)" opacity=".5"/>

<!-- Output text -->
<g>{right_chars}</g>
<text x="260" y="500" font-family="monospace" font-size="9" fill="#00d4ff" opacity=".5" text-anchor="middle" letter-spacing="4">SIGNAL OUTPUT</text>

<!-- Frame -->
<rect x="1" y="1" width="518" height="518" fill="none" stroke="#00ff88" stroke-opacity=".25"/>
</svg>"""


STAR = svg_img(star_art(), "hero-art", "Neutron star")
NET = svg_img(crypto_art(), "art", "Encryption shield")
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

.hero-art { display:block; width:min(100%,640px); margin:2.5rem auto 0 auto; mask-image:radial-gradient(circle closest-side,#000 80%,transparent 100%); }
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
