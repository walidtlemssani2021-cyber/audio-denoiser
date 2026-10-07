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
# ART 1 — NEUTRON STAR (realistic sphere, no jets, no waves)
# ═══════════════════════════════════════════════════════════════
def star_art():
    rnd = random.Random(7)

    stars = ""
    for _ in range(90):
        x, y = rnd.randint(0, 800), rnd.randint(0, 800)
        r = rnd.uniform(0.4, 1.8)
        o = rnd.uniform(0.15, 0.9)
        stars += f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="#fff" opacity="{o:.2f}"/>'

    corona = ""
    for i in range(9):
        r = 118 + i * 11
        o = 0.28 - i * 0.028
        corona += f'<circle cx="400" cy="400" r="{r}" fill="none" stroke="#00ff88" stroke-opacity="{o:.3f}" stroke-width="2"/>'

    sphere = ""
    for i in range(24):
        r = 102 - i * 3.5
        o = 0.03 + (i / 24) * 0.14
        sphere += f'<circle cx="400" cy="400" r="{r:.1f}" fill="#00ff88" opacity="{o:.3f}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
<defs>
<radialGradient id="coreGrad">
<stop offset="0" stop-color="#ffffff"/>
<stop offset="0.22" stop-color="#baffd9"/>
<stop offset="0.55" stop-color="#00ff88" stop-opacity="0.92"/>
<stop offset="1" stop-color="#00ff88" stop-opacity="0"/>
</radialGradient>
<radialGradient id="haloGrad">
<stop offset="0" stop-color="#00d4ff" stop-opacity="0.32"/>
<stop offset="0.5" stop-color="#00ff88" stop-opacity="0.12"/>
<stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/>
</radialGradient>
<filter id="blurBig"><feGaussianBlur stdDeviation="28"/></filter>
<filter id="blurSmall"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<style>
.corePulse {{ transform-origin: 400px 400px; animation: coreBeat 3s ease-in-out infinite; }}
@keyframes coreBeat {{ 0%,100% {{ opacity: .85; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.05); }} }}
.haloPulse {{ transform-origin: 400px 400px; animation: haloBeat 4s ease-in-out infinite; }}
@keyframes haloBeat {{ 0%,100% {{ opacity: .6; transform: scale(1); }} 50% {{ opacity: .9; transform: scale(1.08); }} }}
.rotateSlow {{ transform-origin: 400px 400px; animation: spin 90s linear infinite; }}
.rotateSlower {{ transform-origin: 400px 400px; animation: spin 140s linear infinite reverse; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
</style>

<g>{stars}</g>

<circle class="haloPulse" cx="400" cy="400" r="360" fill="url(#haloGrad)" filter="url(#blurBig)"/>

<g class="rotateSlow">
<circle cx="400" cy="400" r="290" fill="none" stroke="#00d4ff" stroke-opacity="0.15" stroke-width="1" stroke-dasharray="2 16"/>
<circle cx="400" cy="400" r="240" fill="none" stroke="#00ff88" stroke-opacity="0.10" stroke-width="1" stroke-dasharray="6 22"/>
</g>
<g class="rotateSlower">
<circle cx="400" cy="400" r="205" fill="none" stroke="#7b2ff7" stroke-opacity="0.18" stroke-width="1" stroke-dasharray="1 12"/>
</g>

<g>{sphere}</g>

<g class="corePulse">{corona}</g>

<circle class="corePulse" cx="400" cy="400" r="105" fill="url(#coreGrad)" filter="url(#blurSmall)"/>
<circle cx="400" cy="400" r="18" fill="#fff"/>
<circle cx="400" cy="400" r="38" fill="none" stroke="#ffffff" stroke-opacity="0.45" stroke-width="1.5"/>

<rect x="1" y="1" width="798" height="798" fill="none" stroke="#00ff88" stroke-opacity="0.12"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 2 — ENCRYPTED CODE (matrix style)
# ═══════════════════════════════════════════════════════════════
def crypto_art():
    rnd = random.Random(5)

    columns = ""
    for c in range(22):
        x = 12 + c * 23
        chars = ""
        for r in range(16):
            y = 18 + r * 24
            ch = rnd.choice("0123456789ABCDEF")
            o = rnd.uniform(0.08, 0.9)
            chars += f'<text x="{x}" y="{y}" opacity="{o:.2f}">{ch}</text>'
        delay = rnd.uniform(0, 4)
        columns += f'<g style="animation-delay:{delay:.2f}s">{chars}</g>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400">
<defs>
<radialGradient id="glow">
<stop offset="0" stop-color="#00ff88" stop-opacity="0.30"/>
<stop offset="0.6" stop-color="#00d4ff" stop-opacity="0.08"/>
<stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/>
</radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#00ff88" stop-opacity="0"/>
<stop offset="0.5" stop-color="#00ff88" stop-opacity="0.35"/>
<stop offset="1" stop-color="#00ff88" stop-opacity="0"/>
</linearGradient>
</defs>
<style>
.columns g {{ animation: flick 2.8s ease-in-out infinite alternate; }}
@keyframes flick {{ from {{ opacity: .35; }} to {{ opacity: 1; }} }}
.scanline {{ animation: scanMove 4s linear infinite; }}
@keyframes scanMove {{ 0% {{ transform: translateY(-120px); }} 100% {{ transform: translateY(460px); }} }}
</style>
<rect width="520" height="400" fill="#02060a"/>
<circle cx="260" cy="200" r="230" fill="url(#glow)"/>
<g class="columns" font-family="monospace" font-weight="bold" font-size="14" fill="#00ff88">{columns}</g>
<rect class="scanline" x="0" y="0" width="520" height="80" fill="url(#scan)"/>
<rect x="1" y="1" width="518" height="398" fill="none" stroke="#00ff88" stroke-opacity="0.25"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 3 — TEXT ↔ SOUND (box + waveform + two arrows)
# ═══════════════════════════════════════════════════════════════
def pipeline_art():
    rnd = random.Random(3)

    # text lines inside the box
    text_lines = ""
    for r in range(7):
        for c in range(6):
            w = rnd.randint(14, 30)
            text_lines += f'<rect x="{50 + c * 32}" y="{70 + r * 20}" width="{w}" height="4" rx="2" fill="#00ff88" opacity="{0.35 + 0.1 * c:.2f}"/>'

    # waveform bars
    bars = ""
    for i in range(22):
        h = 10 + int(34 * abs(math.sin(i * 0.55 + 0.3)))
        x = 48 + i * 20
        o = 0.35 + 0.55 * abs(math.sin(i * 0.4))
        bars += f'<rect x="{x}" y="{350 - h / 2:.0f}" width="8" height="{h}" rx="4" fill="#00d4ff" opacity="{o:.2f}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 480">
<defs>
<linearGradient id="arrowR" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#00ff88" stop-opacity="0.2"/>
<stop offset="1" stop-color="#00ff88" stop-opacity="1"/>
</linearGradient>
<linearGradient id="arrowL" x1="1" y1="0" x2="0" y2="0">
<stop offset="0" stop-color="#00d4ff" stop-opacity="0.2"/>
<stop offset="1" stop-color="#00d4ff" stop-opacity="1"/>
</linearGradient>
</defs>
<style>
.arrR {{ stroke-dasharray: 10 10; animation: moveR 1.6s linear infinite; }}
@keyframes moveR {{ to {{ stroke-dashoffset: -40; }} }}
.arrL {{ stroke-dasharray: 10 10; animation: moveL 1.6s linear infinite; }}
@keyframes moveL {{ to {{ stroke-dashoffset: 40; }} }}
.barPulse {{ animation: bp 1.8s ease-in-out infinite; }}
@keyframes bp {{ 0%,100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
</style>

<rect width="520" height="480" fill="#02060a"/>

<!-- TEXT BOX -->
<rect x="40" y="40" width="440" height="160" fill="none" stroke="#00ff88" stroke-opacity="0.35" rx="10"/>
<g>{text_lines}</g>
<text x="260" y="28" font-family="monospace" font-size="9" fill="#00ff88" opacity="0.55" text-anchor="middle" letter-spacing="6">TEXT</text>

<!-- ARROW RIGHT (text → sound) -->
<line class="arrR" x1="150" y1="240" x2="370" y2="240" stroke="url(#arrowR)" stroke-width="2.5"/>
<polygon points="370,232 392,240 370,248" fill="#00ff88"/>

<!-- ARROW LEFT (sound → text) -->
<line class="arrL" x1="370" y1="272" x2="150" y2="272" stroke="url(#arrowL)" stroke-width="2.5"/>
<polygon points="150,264 128,272 150,280" fill="#00d4ff"/>

<!-- WAVEFORM BOX -->
<rect x="40" y="310" width="440" height="140" fill="none" stroke="#00d4ff" stroke-opacity="0.35" rx="10"/>
<g class="barPulse">{bars}</g>
<text x="260" y="472" font-family="monospace" font-size="9" fill="#00d4ff" opacity="0.55" text-anchor="middle" letter-spacing="6">SOUND</text>

<rect x="1" y="1" width="518" height="478" fill="none" stroke="#00ff88" stroke-opacity="0.25"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 4 — RIDGE (pulse profiles field)
# ═══════════════════════════════════════════════════════════════
def ridge_art():
    rnd = random.Random(11)
    rows = []
    for i in range(20):
        y0 = 80 + i * 17
        pts = " ".join(
            f"{x},{y0 - 62 * math.exp(-((x - 600) / 230) ** 2) * (0.3 + 0.7 * rnd.random()) - 2.5 * rnd.random():.1f}"
            for x in range(0, 1201, 12)
        )
        rows.append(
            f'<polygon points="0,{y0} {pts} 1200,{y0}" fill="#02060a" '
            f'stroke="#00ff88" stroke-opacity="{0.3 + 0.7 * i / 19:.2f}" '
            f'stroke-width="1.4" stroke-linejoin="round"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460">'
        '<rect width="1200" height="460" fill="#02060a"/>'
        '<defs><radialGradient id="rg" cx="0.5" cy="0.55" r="0.5">'
        '<stop offset="0" stop-color="#00ff88" stop-opacity="0.16"/>'
        '<stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient></defs>'
        '<rect width="1200" height="460" fill="url(#rg)"/>'
        + "".join(rows) +
        '</svg>'
    )


STAR = svg_img(star_art(), "hero-art", "Neutron star")
NET = svg_img(crypto_art(), "art", "Encrypted code")
PIPE = svg_img(pipeline_art(), "art", "Text to sound")
RIDGE = svg_img(ridge_art(), "banner", "Pulse profiles")

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
.banner { display:block; width:100%; margin-top:5rem; border-radius:20px; border:1px solid rgba(0,255,136,.2); box-shadow:0 0 90px rgba(0,255,136,.08); }
.banner-cap { font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.4); text-align:center; margin-top:1rem; }

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
html(f"""
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
    {RIDGE}
    <p class="banner-cap">Illustration · stacked pulse profiles</p>
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
