import base64
import math
import random
import time
from html import escape

import streamlit as st

# ═══════════════════════════════════════════════════════════════
# No-Cache — forces browser to refresh the view instantly
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
""", unsafe_allow_html=True)


def html(code):
    clean = " ".join(line.strip() for line in code.split("\n") if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def svg_img(svg, cls, alt):
    unique_svg = svg.replace("<svg ", f'<svg data-t="{time.time()}" ', 1)
    b64 = base64.b64encode(unique_svg.encode()).decode()
    return f'<img class="{cls}" alt="{alt}" src="data:image/svg+xml;base64,{b64}"/>'


# ═══════════════════════════════════════════════════════════════
# ART 1 — NEUTRON STAR (BLUE/WHITE — TRANSPARENT BACKGROUND)
# ═══════════════════════════════════════════════════════════════
def star_art():
    rnd = random.Random(7)
    cx, cy, R, W, T, L = 400, 280, 150, 600, 0.9, 540

    blob_list = [
        (rnd.uniform(0, W), rnd.uniform(cy - R, cy + R), rnd.uniform(16, 52), rnd.uniform(7, 24),
         rnd.choice(["b1", "b2", "b3"]), rnd.uniform(0.45, 0.95))
        for _ in range(80)
    ]

    def blobs(dx):
        out = ""
        for x, y, rx, ry, g, o in blob_list:
            for ox in (0, *((W,) if x < 60 else ()), *((-W,) if x > W - 60 else ())):
                out += f'<ellipse cx="{250 + x + ox + dx:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#{g})" opacity="{o:.2f}"/>'
        return out

    texture = blobs(0) + blobs(W)

    def half(sign, grad):
        e = cy + sign * L
        return (f'<polygon points="{cx - 9},{cy} {cx + 9},{cy} {cx + 48},{e} {cx - 48},{e}" fill="url(#{grad})" opacity=".3"/>'
                f'<polygon points="{cx - 4},{cy} {cx + 4},{cy} {cx + 21},{e} {cx - 21},{e}" fill="url(#{grad})" opacity=".75"/>'
                f'<polygon points="{cx - 1.5},{cy} {cx + 1.5},{cy} {cx + 7},{e} {cx - 7},{e}" fill="url(#{grad})"/>')

    top, bot = half(-1, "jt"), half(1, "jb")
    back = f'<g class="sw"><g class="fs"><g class="o1">{top}</g><g class="o0">{bot}</g></g></g>'
    front = f'<g class="sw"><g class="fs"><g class="o0">{top}</g><g class="o1">{bot}</g></g></g>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560">
<defs>
<clipPath id="ball"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>
<clipPath id="out"><path clip-rule="evenodd" d="M0 0H800V560H0Z M{cx - R} {cy} a{R} {R} 0 1 0 {2 * R} 0 a{R} {R} 0 1 0 {-2 * R} 0Z"/></clipPath>
<radialGradient id="halo"><stop offset="0" stop-color="#cfe6ff" stop-opacity=".6"/><stop offset=".35" stop-color="#2f8cff" stop-opacity=".25"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></radialGradient>
<radialGradient id="rim"><stop offset="0" stop-color="#e6f2ff" stop-opacity="0"/><stop offset=".78" stop-color="#e6f2ff" stop-opacity="0"/><stop offset=".8" stop-color="#e6f2ff" stop-opacity=".9"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></radialGradient>
<radialGradient id="b1"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<radialGradient id="b2"><stop offset="0" stop-color="#5aa9ff" stop-opacity=".9"/><stop offset="1" stop-color="#5aa9ff" stop-opacity="0"/></radialGradient>
<radialGradient id="b3"><stop offset="0" stop-color="#0b3d91" stop-opacity=".85"/><stop offset="1" stop-color="#0b3d91" stop-opacity="0"/></radialGradient>
<radialGradient id="shade" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".6" stop-color="#02112e" stop-opacity=".2"/><stop offset="1" stop-color="#000a1f" stop-opacity=".85"/></radialGradient>
<radialGradient id="flare"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset=".4" stop-color="#bfe0ff" stop-opacity=".6"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></radialGradient>
<linearGradient id="jt" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f4faff"/><stop offset=".35" stop-color="#8cc8ff" stop-opacity=".65"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></linearGradient>
<linearGradient id="jb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4faff"/><stop offset=".35" stop-color="#8cc8ff" stop-opacity=".65"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></linearGradient>
</defs>
<style>
.tex {{ animation: scroll {T * 0.8:.2f}s linear infinite; }}
@keyframes scroll {{ to {{ transform: translateX(-{W}px); }} }}
.sw {{ transform-origin: {cx}px {cy}px; animation: sw {T / 2}s ease-in-out infinite alternate; }}
@keyframes sw {{ from {{ transform: rotate(50deg); }} to {{ transform: rotate(-50deg); }} }}
.fs {{ transform-origin: {cx}px {cy}px; animation: fs {T / 2}s ease-in-out infinite; }}
@keyframes fs {{ 0%,100% {{ transform: scaleY(1); }} 50% {{ transform: scaleY(.6); }} }}
.o0 {{ animation: o0 {T}s step-end infinite; }}
.o1 {{ animation: o1 {T}s step-end infinite; }}
@keyframes o0 {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
@keyframes o1 {{ 0% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
.fl {{ transform-origin: {cx}px {cy}px; animation: fl {T / 2}s ease-in-out infinite; }}
@keyframes fl {{ 0%,100% {{ opacity: 0; transform: scale(.8); }} 50% {{ opacity: .65; transform: scale(1.15); }} }}
.pulse {{ transform-origin: {cx}px {cy}px; animation: pulse {T / 2}s ease-in-out infinite alternate; }}
@keyframes pulse {{ from {{ opacity: .65; transform: scale(.97); }} to {{ opacity: 1; transform: scale(1.04); }} }}
</style>

<circle class="pulse" cx="{cx}" cy="{cy}" r="300" fill="url(#halo)"/>

<g transform="rotate(20 {cx} {cy})">{back}</g>

<circle cx="{cx}" cy="{cy}" r="{R}" fill="#dcecff"/>
<g clip-path="url(#ball)">
<g transform="rotate(20 {cx} {cy})"><g class="tex">{texture}</g></g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#shade)"/>
</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#e6f2ff" stroke-opacity=".7" stroke-width="2"/>
<circle class="fl" cx="{cx}" cy="{cy}" r="{R + 30}" fill="url(#flare)"/>

<g>{front}</g>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 2 — ENCRYPTION (static, symbols)
# ═══════════════════════════════════════════════════════════════
def crypto_art():
    rnd = random.Random(5)
    symbol_pool = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    letter_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digit_pool = "0123456789"
    pool = symbol_pool + symbol_pool + letter_pool + digit_pool
    colors = ["#3da5ff", "#ffffff", "#2b6bff"]

    chars = ""
    for r in range(14):
        for c in range(22):
            x = 15 + c * 23
            y = 22 + r * 27
            ch = rnd.choice(pool)
            o = rnd.uniform(0.25, 0.95)
            size = rnd.uniform(10, 15)
            color = rnd.choice(colors)
            chars += f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size:.1f}" font-weight="bold" fill="{color}" opacity="{o:.2f}">{escape(ch)}</text>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400">
<defs>
<radialGradient id="glow">
<stop offset="0" stop-color="#3da5ff" stop-opacity="0.35"/>
<stop offset="0.6" stop-color="#ffffff" stop-opacity="0.06"/>
<stop offset="1" stop-color="#2b6bff" stop-opacity="0"/>
</radialGradient>
</defs>
<rect width="520" height="400" fill="#02060a"/>
<circle cx="260" cy="200" r="230" fill="url(#glow)"/>
<g>{chars}</g>
<rect x="1" y="1" width="518" height="398" fill="none" stroke="#3da5ff" stroke-opacity="0.3"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 3 — TEXT ⇄ SOUND
# ═══════════════════════════════════════════════════════════════
def pipeline_art():
    points = []
    n = 80
    for i in range(n + 1):
        x = (i / n) * 400
        amp1 = 20 * math.sin(i * 0.35)
        amp2 = 12 * math.sin(i * 0.78 + 1.2)
        amp3 = 7 * math.cos(i * 1.45 + 0.6)
        amp4 = 4 * math.sin(i * 2.3 + 2.1)
        y = 392 - (amp1 + amp2 + amp3 + amp4)
        points.append(f"{x:.1f},{y:.1f}")
    wave_d = "M" + " L".join(points)

    down = "".join(f'<circle class="dn" style="animation-delay:{i * 0.5}s" cx="185" cy="182" r="3.5" fill="#3da5ff"/>' for i in range(3))
    up = "".join(f'<circle class="up" style="animation-delay:{i * 0.5}s" cx="335" cy="298" r="3.5" fill="#ffffff"/>' for i in range(3))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 480">
<style>
.flowD {{ stroke-dasharray: 8 8; animation: fd 1s linear infinite; }}
.flowU {{ stroke-dasharray: 8 8; animation: fu 1s linear infinite; }}
@keyframes fd {{ to {{ stroke-dashoffset: -32; }} }}
@keyframes fu {{ to {{ stroke-dashoffset: 32; }} }}
.dn {{ animation: dn 1.5s linear infinite; opacity: 0; }}
.up {{ animation: up 1.5s linear infinite; opacity: 0; }}
@keyframes dn {{ 0% {{ transform: translateY(0); opacity: 0; }} 15%,85% {{ opacity: 1; }} 100% {{ transform: translateY(116px); opacity: 0; }} }}
@keyframes up {{ 0% {{ transform: translateY(0); opacity: 0; }} 15%,85% {{ opacity: 1; }} 100% {{ transform: translateY(-116px); opacity: 0; }} }}
.cur {{ animation: cur 1s steps(2) infinite; }}
@keyframes cur {{ 50% {{ opacity: 0; }} }}
.sc {{ stroke-dasharray: 70 930; animation: sc 2s linear infinite; }}
@keyframes sc {{ from {{ stroke-dashoffset: 70; }} to {{ stroke-dashoffset: -930; }} }}
</style>
<rect width="520" height="480" fill="#02060a"/>

<rect x="40" y="36" width="440" height="130" rx="12" fill="#3da5ff" fill-opacity=".04" stroke="#3da5ff" stroke-opacity=".45"/>
<text x="60" y="62" font-family="monospace" font-size="11" letter-spacing="6" fill="#3da5ff" opacity=".8">TEXT</text>
<text x="60" y="116" font-family="monospace" font-size="22" font-weight="bold" fill="#3da5ff">YOUR TEXT<tspan class="cur">_</tspan></text>

<line class="flowD" x1="185" y1="176" x2="185" y2="294" stroke="#3da5ff" stroke-width="2.5"/>
<polygon points="173,292 197,292 185,310" fill="#3da5ff"/>
{down}
<text x="168" y="244" text-anchor="end" font-family="monospace" font-size="11" letter-spacing="3" fill="#3da5ff">ENCRYPT</text>

<line class="flowU" x1="335" y1="304" x2="335" y2="186" stroke="#ffffff" stroke-width="2.5"/>
<polygon points="323,188 347,188 335,170" fill="#ffffff"/>
{up}
<text x="352" y="244" font-family="monospace" font-size="11" letter-spacing="3" fill="#ffffff">DECRYPT</text>

<rect x="40" y="314" width="440" height="130" rx="12" fill="#ffffff" fill-opacity=".04" stroke="#ffffff" stroke-opacity=".4"/>
<text x="60" y="340" font-family="monospace" font-size="11" letter-spacing="6" fill="#ffffff" opacity=".8">SOUND</text>
<path transform="translate(60 0)" d="{wave_d}" fill="none" stroke="#ffffff" stroke-opacity=".6" stroke-width="2.2" stroke-linejoin="round"/>
<path class="sc" pathLength="1000" transform="translate(60 0)" d="{wave_d}" fill="none" stroke="#3da5ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="1" y="1" width="518" height="478" fill="none" stroke="#3da5ff" stroke-opacity="0.25"/>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 4 — RIDGE
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
        rows.append(f'<polygon points="0,{y0} {pts} 1200,{y0}" fill="#02060a" stroke="#3da5ff" stroke-opacity="{0.3 + 0.7 * i / 19:.2f}" stroke-width="1.4" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460"><rect width="1200" height="460" fill="#02060a"/>'
            '<defs><radialGradient id="rg" cx="0.5" cy="0.55" r="0.5"><stop offset="0" stop-color="#3da5ff" stop-opacity="0.16"/><stop offset="1" stop-color="#3da5ff" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="1200" height="460" fill="url(#rg)"/>' + "".join(rows) + '</svg>')


STAR = svg_img(star_art(), "hero-art", "Neutron star spinning")
NET = svg_img(crypto_art(), "art", "Encryption symbols")
PIPE = svg_img(pipeline_art(), "art", "Text converted to sound and back")
RIDGE = svg_img(ridge_art(), "banner", "Pulse profiles")

# ═══════════════════════════════════════════════════════════════
# NASA VIDEO SOURCES
# ═══════════════════════════════════════════════════════════════
NASA_VIDEO = "https://svs.gsfc.nasa.gov/vis/a010000/a010500/a010582/10582_BlinkingStar_MPG4_720x486_29.97.mp4"
NASA_POSTER = "https://svs.gsfc.nasa.gov/vis/a010000/a010500/a010582/BhSURFtv.0019.jpg"

# ═══════════════════════════════════════════════════════════════
# GLOBAL CSS — BLUE THEME + BLUEPRINT BACKGROUND + NASA VIDEO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background:#02060a !important; color:#fff; -webkit-font-smoothing:antialiased; overflow-x:hidden; }
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown div { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
.block-container { max-width:1320px !important; padding:0 3rem 5rem 3rem !important; position:relative; z-index:3; }

/* ═══ BACKGROUND: BLUEPRINT GRID + BLUE GLOW ═══ */
.bg-layer { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; background:#02060a; }
.bp { position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(rgba(61,165,255,.11) 1px,transparent 1px),linear-gradient(90deg,rgba(61,165,255,.11) 1px,transparent 1px); background-size:40px 40px,40px 40px,160px 160px,160px 160px; -webkit-mask-image:radial-gradient(ellipse 90% 70% at 60% 25%,#000 10%,transparent 78%); mask-image:radial-gradient(ellipse 90% 70% at 60% 25%,#000 10%,transparent 78%); }
.gl { position:absolute; border-radius:50%; filter:blur(140px); will-change:transform; }
.g1 { width:820px; height:820px; top:-420px; right:-260px; background:radial-gradient(circle,rgba(61,165,255,.5),transparent 70%); animation:drift 26s ease-in-out infinite; }
.g2 { width:700px; height:700px; bottom:-380px; left:-300px; background:radial-gradient(circle,rgba(43,107,255,.32),transparent 70%); animation:drift 34s ease-in-out infinite reverse; }
@keyframes drift { 50% { transform:translate(-90px,70px) scale(1.12); } }
.grain { position:absolute; inset:0; opacity:.08; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
.vig { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 40%,transparent 50%,rgba(0,0,0,.8) 100%); }

/* ═══ CINEMATIC NASA VIDEO ═══ */
.cine { margin-top:5rem; }
.cine-frame { position:relative; aspect-ratio:16/9; overflow:hidden; border:1px solid rgba(61,165,255,.35); background:radial-gradient(circle at 50% 50%,#08122a,#000 70%); box-shadow:0 50px 120px rgba(61,165,255,.16); }
.cine-video { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; display:block; filter:saturate(1.1) contrast(1.06); }
.cine-shade { position:absolute; inset:0; pointer-events:none; background:linear-gradient(180deg,rgba(0,0,0,.6),transparent 30%,transparent 62%,rgba(0,0,0,.8)), radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.5) 100%); }
.cine-frame::before { content:''; position:absolute; inset:12px; pointer-events:none; z-index:3; background:linear-gradient(#3da5ff,#3da5ff) top left/22px 2px no-repeat, linear-gradient(#3da5ff,#3da5ff) top left/2px 22px no-repeat, linear-gradient(#3da5ff,#3da5ff) top right/22px 2px no-repeat, linear-gradient(#3da5ff,#3da5ff) top right/2px 22px no-repeat, linear-gradient(#3da5ff,#3da5ff) bottom left/22px 2px no-repeat, linear-gradient(#3da5ff,#3da5ff) bottom left/2px 22px no-repeat, linear-gradient(#3da5ff,#3da5ff) bottom right/22px 2px no-repeat, linear-gradient(#3da5ff,#3da5ff) bottom right/2px 22px no-repeat; opacity:.8; }
.cine-tag { position:absolute; top:1.6rem; left:1.8rem; z-index:4; display:flex; align-items:center; gap:.6rem; font-size:.62rem; letter-spacing:.24em; color:#fff; padding:.45rem .9rem; background:rgba(0,0,0,.5); -webkit-backdrop-filter:blur(10px); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,.18); }
.cine-tag i { width:7px; height:7px; border-radius:50%; background:#ff4d4d; box-shadow:0 0 12px #ff4d4d; animation:blink 1.4s infinite; }
.cine-credit { position:absolute; left:1.8rem; right:1.8rem; bottom:1.5rem; z-index:4; font-size:.56rem; letter-spacing:.2em; color:rgba(255,255,255,.6); }

.nav { display:flex; justify-content:space-between; align-items:center; padding:1.3rem 3rem; margin:0 -3rem; position:relative; z-index:100; backdrop-filter:blur(24px); background:rgba(2,6,10,.6); border-bottom:1px solid rgba(255,255,255,.08); }
.nav-brand { display:flex; align-items:center; gap:.85rem; font-family:'Orbitron', sans-serif; font-weight:900; font-size:1.05rem; letter-spacing:.3em; color:#3da5ff; text-shadow:0 0 30px rgba(61,165,255,.9); }
.nav-brand::before { content:''; width:11px; height:11px; background:#3da5ff; box-shadow:0 0 25px #3da5ff; transform:rotate(45deg); animation:spin 8s linear infinite; }
@keyframes spin { to { transform:rotate(405deg); } }
.nav-status { display:flex; align-items:center; gap:.5rem; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; color:#3da5ff; }
.nav-dot { width:7px; height:7px; border-radius:50%; background:#3da5ff; box-shadow:0 0 14px #3da5ff; animation:blink 1.8s infinite; }
@keyframes blink { 50% { opacity:.3; } }

.hero { padding:6.5rem 0 2rem 0; text-align:center; position:relative; }
.hero-badge { display:inline-flex; align-items:center; gap:.7rem; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.3em; text-transform:uppercase; color:rgba(61,165,255,.9); padding:.7rem 1.8rem; border:1px solid rgba(61,165,255,.3); border-radius:100px; background:rgba(61,165,255,.05); margin-bottom:2.6rem; }
.hero-badge i { width:7px; height:7px; border-radius:50%; background:#3da5ff; box-shadow:0 0 14px #3da5ff; animation:blink 1.8s infinite; }

.hero-name { font-family:'Orbitron', sans-serif !important; font-weight:900; font-size:clamp(2rem, 9vw, 7rem); line-height:1; letter-spacing:.08em; margin:0 auto 2rem auto; padding:0; white-space:nowrap; background:linear-gradient(180deg,#fff 0%,#3da5ff 60%,#2b6bff 100%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 70px rgba(61,165,255,.65)); animation:glow 4s ease-in-out infinite; }
@keyframes glow { 50% { filter:drop-shadow(0 0 110px rgba(61,165,255,.95)); } }

.hero-tagline {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(0.75rem, 1.3vw, 0.95rem);
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(61,165,255,0.95);
    text-shadow: 0 0 20px rgba(61,165,255,0.6);
    margin: 1.5rem auto 0 auto;
    max-width: 950px;
    line-height: 1.9;
    font-weight: 400;
}

.hero-art { display:block; width:min(100%,640px); margin:2.5rem auto 0 auto; border-radius:20px; border:1px solid rgba(61,165,255,.25); box-shadow:0 0 90px rgba(61,165,255,.15); }
.art { display:block; width:100%; max-width:520px; margin-top:1rem; border-radius:18px; border:1px solid rgba(61,165,255,.2); box-shadow:0 0 70px rgba(61,165,255,.08); }
.banner { display:block; width:100%; margin-top:5rem; border-radius:20px; border:1px solid rgba(61,165,255,.2); box-shadow:0 0 90px rgba(61,165,255,.08); }
.banner-cap { font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.4); text-align:center; margin-top:1rem; }

.stats-strip { display:grid; grid-template-columns:repeat(4,1fr); margin:3rem 0 2rem 0; border:1px solid rgba(61,165,255,.18); border-radius:20px; background:linear-gradient(145deg,rgba(61,165,255,.05),rgba(255,255,255,.01)); backdrop-filter:blur(20px); overflow:hidden; }
.stat-item { text-align:center; padding:2.2rem 1rem; }
.stat-item + .stat-item { border-left:1px solid rgba(255,255,255,.08); }
.stat-val { font-family:'JetBrains Mono', monospace; font-size:2rem; font-weight:800; color:#3da5ff; text-shadow:0 0 25px rgba(61,165,255,.6); display:block; margin-bottom:.6rem; }
.stat-lbl { font-family:'JetBrains Mono', monospace; font-size:.65rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.45); }

.sec { padding:7rem 0 0 0; position:relative; }
.sec-grid { display:grid; grid-template-columns:1fr 1.2fr; gap:5rem; align-items:start; }
.sec-title { font-family:'Orbitron', sans-serif !important; font-weight:900; font-size:clamp(1.3rem, 3vw, 2.4rem); line-height:1.2; letter-spacing:.12em; color:#3da5ff; text-shadow:0 0 40px rgba(61,165,255,.6), 0 0 80px rgba(61,165,255,.3); margin:0 0 2rem 0; text-transform:uppercase; }
.text-block { font-family:'Space Grotesk', sans-serif; font-size:1.08rem; color:rgba(255,255,255,.72); line-height:2; font-weight:300; margin:0 0 2rem 0; padding-left:1.8rem; border-left:2px solid rgba(61,165,255,.3); transition:all .4s ease; }
.text-block:hover { border-left-color:#3da5ff; color:rgba(255,255,255,.95); padding-left:2.4rem; }
.text-block strong { color:#3da5ff; font-weight:600; text-shadow:0 0 25px rgba(61,165,255,.6); }

/* ═══ FAQ — ACCORDION STYLE ═══ */
.faq-list { display: flex; flex-direction: column; gap: 1rem; margin-top: 2rem; }
.faq-item {
    border: 1px solid rgba(61,165,255,0.2);
    border-radius: 12px;
    background: linear-gradient(145deg, rgba(61,165,255,0.03), rgba(0, 0, 0, 0.2));
    transition: all .3s ease;
    overflow: hidden;
}
.faq-item[open] { border-color: rgba(61,165,255,0.6); box-shadow: 0 0 35px rgba(61,165,255,0.2); }
.faq-item:hover { border-color: rgba(61,165,255,0.5); box-shadow: 0 0 25px rgba(61,165,255,0.12); }
.faq-item summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem; font-weight: 700; color: #3da5ff;
    text-shadow: 0 0 15px rgba(61,165,255,0.5);
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 1.4rem 1.8rem; cursor: pointer; list-style: none;
    display: flex; justify-content: space-between; align-items: center;
    transition: all .3s ease;
}
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after { content: '+'; font-size: 1.4rem; color: rgba(61,165,255,0.7); transition: transform .3s ease; line-height: 1; }
.faq-item[open] summary::after { content: '−'; transform: rotate(180deg); }
.faq-item summary:hover { background: rgba(61,165,255,0.04); }
.faq-a {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.98rem; color: rgba(255, 255, 255, 0.7);
    line-height: 1.8; font-weight: 300;
    padding: 0 1.8rem 1.4rem 1.8rem;
    border-top: 1px solid rgba(61,165,255,0.12);
    margin-top: 0; padding-top: 1.2rem;
}

/* ═══ BIG QUOTE ═══ */
.big-quote {
    position: relative; max-width: 900px; margin: 6rem auto 0 auto;
    padding: 4.5rem 3rem 3rem 4rem;
    border: 1px solid rgba(61,165,255,0.25); border-radius: 20px;
    background: linear-gradient(145deg, rgba(61,165,255,0.04), rgba(0, 0, 0, 0.2));
    overflow: hidden;
}
.big-quote::before {
    content: '"'; position: absolute; top: -20px; left: 20px;
    font-family: 'Space Grotesk', sans-serif; font-size: 10rem; font-weight: 700;
    color: rgba(61,165,255,0.25);
    text-shadow: 0 0 30px rgba(61,165,255,0.8), 0 0 60px rgba(61,165,255,0.4);
    line-height: 1; pointer-events: none;
    animation: quoteGlow 3s ease-in-out infinite;
}
.big-quote::after {
    content: '"'; position: absolute; bottom: -60px; right: 20px;
    font-family: 'Space Grotesk', sans-serif; font-size: 10rem; font-weight: 700;
    color: rgba(61,165,255,0.25);
    text-shadow: 0 0 30px rgba(61,165,255,0.8), 0 0 60px rgba(61,165,255,0.4);
    line-height: 1; pointer-events: none;
    animation: quoteGlow 3s ease-in-out infinite;
}
@keyframes quoteGlow {
    0%, 100% { text-shadow: 0 0 30px rgba(61,165,255,0.8), 0 0 60px rgba(61,165,255,0.4); }
    50%      { text-shadow: 0 0 50px rgba(61,165,255,1), 0 0 100px rgba(61,165,255,0.6); }
}
.big-quote-text {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(1.2rem, 2.5vw, 1.8rem); font-weight: 500;
    color: #ffffff; line-height: 1.6; margin: 0 0 2.5rem 0;
    position: relative; z-index: 1; padding-top: 0.5rem;
}
.big-quote-text .highlight { color: #3da5ff; font-weight: 600; text-shadow: 0 0 20px rgba(61,165,255,0.5); }
.big-quote-author {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem; letter-spacing: 0.35em; text-transform: uppercase;
    color: rgba(255, 255, 255, 0.7);
    display: flex; align-items: center; justify-content: center; gap: 1rem;
    position: relative; z-index: 1;
}
.big-quote-author::before, .big-quote-author::after {
    content: ''; height: 1px;
    background: rgba(61,165,255,0.4); box-shadow: 0 0 10px rgba(61,165,255,0.6);
    width: 40px;
}

.cta { padding:6rem 3rem; text-align:center; border:1px solid rgba(61,165,255,.3); border-radius:28px; background:radial-gradient(ellipse at top,rgba(61,165,255,.18),transparent 60%),linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); position:relative; overflow:hidden; margin-top:7rem; }
.cta::before { content:''; position:absolute; inset:0; background-image:linear-gradient(rgba(61,165,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(61,165,255,.07) 1px,transparent 1px); background-size:40px 40px; mask-image:radial-gradient(ellipse at center,#000 20%,transparent 70%); }
.cta-t { font-family:'JetBrains Mono', monospace; font-weight:500; font-size:clamp(1.15rem, 2.8vw, 2.1rem); text-transform:uppercase; letter-spacing:.16em; line-height:1.5; color:#3da5ff; text-shadow:0 0 28px rgba(61,165,255,.45); margin-bottom:1rem; position:relative; }
.cta-d { font-family:'Space Grotesk', sans-serif; font-size:1.05rem; color:rgba(255,255,255,.62); position:relative; font-weight:300; }

.main-cta .stButton > button,
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3da5ff 0%, #2b6bff 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(61,165,255,.8) !important;
    border-radius: 12px !important;
    padding: 1.2rem 2.5rem !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.15rem !important;
    letter-spacing: .28em !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 25px rgba(61,165,255,.5), 0 0 50px rgba(61,165,255,.25), inset 0 0 15px rgba(255,255,255,.2) !important;
    transition: all .4s cubic-bezier(.4,0,.2,1) !important;
    width: 100% !important;
    position: relative; z-index: 3;
    animation: btnPulse 2.5s ease-in-out infinite;
}
@keyframes btnPulse {
    0%,100% { box-shadow: 0 0 25px rgba(61,165,255,.5), 0 0 50px rgba(61,165,255,.25), inset 0 0 15px rgba(255,255,255,.2); }
    50%     { box-shadow: 0 0 40px rgba(61,165,255,.8), 0 0 80px rgba(61,165,255,.4), inset 0 0 25px rgba(255,255,255,.3); }
}
.stButton > button:hover { transform: translateY(-3px) scale(1.01); filter: brightness(1.1); }

.stButton > button[kind="secondary"] {
    background: linear-gradient(145deg, rgba(61,165,255,.12), rgba(61,165,255,.03)) !important;
    color: #3da5ff !important;
    border: 1px solid rgba(61,165,255,.55) !important;
    border-radius: 12px !important;
    padding: 1.2rem 2rem !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1rem !important;
    letter-spacing: .25em !important;
    text-transform: uppercase !important;
    text-shadow: 0 0 20px rgba(61,165,255,.6) !important;
    transition: all .4s cubic-bezier(.4,0,.2,1) !important;
    width: 100% !important;
    position: relative; z-index: 3;
}
.stButton > button[kind="secondary"]:hover {
    color: #ffffff !important;
    background: #3da5ff !important;
    border-color: #3da5ff !important;
    text-shadow: none !important;
    box-shadow: 0 0 50px rgba(61,165,255,.7), 0 0 100px rgba(61,165,255,.35) !important;
    transform: translateY(-3px);
}

.foot { margin-top:7rem; padding-top:2.5rem; border-top:1px solid rgba(255,255,255,.08); display:flex; flex-direction:column; align-items:center; gap:1.2rem; font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.35); }
.foot-row { display:flex; justify-content:space-between; align-items:center; width:100%; flex-wrap:wrap; gap:1rem; }
.foot-brand { color:rgba(61,165,255,.95); text-shadow:0 0 25px rgba(61,165,255,.6); font-weight:700; }
.foot-copyright { font-size:.65rem; color:rgba(255,255,255,.3); letter-spacing:.2em; text-align:center; padding-top:.8rem; border-top:1px solid rgba(255,255,255,.05); width:100%; }

::-webkit-scrollbar { width:8px; } ::-webkit-scrollbar-track { background:#02060a; }
::-webkit-scrollbar-thumb { background:rgba(61,165,255,.4); border-radius:4px; }

@media (max-width:980px) { .sec-grid { grid-template-columns:1fr; gap:1rem; } }
@media (max-width:700px) {
  .block-container { padding:0 1.25rem 4rem 1.25rem !important; }
  .nav { padding:1.1rem 1.25rem; margin:0 -1.25rem; }
  .hero { padding-top:4rem; }
  .hero-badge { letter-spacing:.12em; font-size:.62rem; padding:.7rem 1.2rem; line-height:1.7; }
  .hero-name { letter-spacing:.04em; }
  .hero-tagline { letter-spacing:.15em; font-size:.72rem; }
  .stats-strip { grid-template-columns:1fr; }
  .stat-item + .stat-item { border-left:none; border-top:1px solid rgba(255,255,255,.08); }
  .big-quote { padding: 3.5rem 1.5rem 2rem 2rem; }
  .big-quote::before { font-size: 7rem; top: -10px; left: 10px; }
  .big-quote::after { font-size: 7rem; bottom: -40px; right: 10px; }
  .big-quote-text { font-size: 1rem; }
  .cta { padding:4rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE
# ═══════════════════════════════════════════════════════════════
html("""
<div class="bg-layer">
    <div class="bp"></div>
    <div class="gl g1"></div>
    <div class="gl g2"></div>
    <div class="grain"></div>
    <div class="vig"></div>
</div>
""")

html("""
<div class="nav">
    <div class="nav-brand">CRYPTORIAN</div>
    <div class="nav-status"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")

html(f"""
<div class="hero">
    <div class="hero-badge"><i></i>DM SAFELY AND SECURE YOUR PRIVACY WITH</div>
    <h1 class="hero-name">CRYPTORIAN</h1>
    {STAR}
    <p class="hero-tagline">USING AN ENCRYPTED MODIFIED NEUTRON STAR SOUND</p>
</div>
""")

st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("LET'S START!", use_container_width=True, type="primary"):
        st.info("The encryption page will be added soon.")

html("""
<div class="stats-strip">
    <div class="stat-item"><span class="stat-val">91</span><span class="stat-lbl">SIGNATURES</span></div>
    <div class="stat-item"><span class="stat-val">2000</span><span class="stat-lbl">MAX CHARS</span></div>
    <div class="stat-item"><span class="stat-val">80%</span><span class="stat-lbl">FLAC SAVING</span></div>
    <div class="stat-item"><span class="stat-val">3</span><span class="stat-lbl">SHAPES</span></div>
</div>
""")

html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHY ENCRYPTION MATTERS</h2>
        {NET}
    </div>
    <div>
        <p class="text-block">Before anything else, let it be known that a person who encrypts their messages is not always a criminal, nor is he suffering from paranoia. Every message you send — carrying your words, your thoughts, your secrets — travels through networks you don't know are safe or not, through servers you don't own, and through channels that are easy to intercept. This increases the risk of your data being obtained and exposes you to surveillance or blackmail.</p>
        <p class="text-block"><strong>And here comes the role of encryption</strong> — and not just any type of encryption. A private encryption. Encrypting your message using a complex, uncommon method. Using a special encryption method will guarantee you a great deal of security and legitimate privacy. And here comes the role of Criptorian.</p>
    </div>
  </div>
</div>
""")

html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHAT IS CRYPTORIAN</h2>
        {PIPE}
    </div>
    <div>
        <p class="text-block">Criptorian is a modern encryption program built to enhance the preservation of legitimate privacy and to combat the phenomenon of data leakage or unauthorized access by unwanted or disliked individuals or entities. Criptorian takes your written message and converts it into a modified sound wave derived from real sound waves emitted by a neutron star. It can also decrypt the resulting sound wave and convert it back into text.</p>
        <p class="text-block"><strong>The reason for using this type of sound for encryption</strong> is the founder's taste and his fascination with the incomprehensible sound waves emitted by neutron stars.</p>
    </div>
  </div>
</div>

<div class="big-quote">
    <p class="big-quote-text">The only way to keep a secret is to make sure no one knows you <span class="highlight">have one.</span></p>
    <p class="big-quote-author">- Criptorian founder -</p>
</div>
""")

html(f"""
<div class="sec">
    <h2 class="sec-title">FREQUENTLY ASKED QUESTIONS</h2>
    <div class="faq-list">
        <details class="faq-item">
            <summary>What is Cryptorian?</summary>
            <div class="faq-a">Cryptorian is a sound-based encryption system that transforms your text messages into a waveform modeled after a neutron star's pulse. It sounds like cosmic noise to anyone who listens — but to the person who holds the key, it is a clear message.</div>
        </details>
        <details class="faq-item">
            <summary>How does the encryption work?</summary>
            <div class="faq-a">Every character you write becomes a unique sonic signature. The secret key reorders these signatures, so the same character produces a different pulse with every key. The message length is embedded in the audio itself for decryption.</div>
        </details>
        <details class="faq-item">
            <summary>Is my data stored or sent anywhere?</summary>
            <div class="faq-a">No. Nothing is stored. Nothing is sent. The entire process happens in memory — invisible to anyone else. Your message and your key never leave your device.</div>
        </details>
        <details class="faq-item">
            <summary>What audio formats are supported?</summary>
            <div class="faq-a">You can export as uncompressed WAV for universal playback, or as compressed FLAC for a much smaller file size without losing quality.</div>
        </details>
        <details class="faq-item">
            <summary>Can anyone decrypt my message without the key?</summary>
            <div class="faq-a">No. Without the exact key, the audio sounds like random cosmic noise. The encryption is mathematically tied to the key, making it virtually impossible to decrypt without it.</div>
        </details>
        <details class="faq-item">
            <summary>How many characters can I encrypt?</summary>
            <div class="faq-a">Cryptorian supports up to 2000 characters per message, with 91 unique sonic signatures available for encoding.</div>
        </details>
    </div>
    {RIDGE}
    <p class="banner-cap">Illustration · stacked pulse profiles</p>
</div>
""")

# ═══ NASA VIDEO SECTION ═══
html(f"""
<div class="cine">
  <div class="cine-frame">
    <video class="cine-video" autoplay muted loop playsinline preload="metadata" poster="{NASA_POSTER}"><source src="{NASA_VIDEO}" type="video/mp4"></video>
    <div class="cine-shade"></div>
    <div class="cine-tag mono"><i></i>PULSAR · SEEN FROM A DISTANCE</div>
    <div class="cine-credit mono">ANIMATION: NASA'S GODDARD SPACE FLIGHT CENTER · DANA BERRY, SKYWORKS DIGITAL</div>
  </div>
</div>
""")

html("""
<div class="cta">
    <div class="cta-t">READY TO BECOME A STAR</div>
    <div class="cta-d">Your message is waiting. Your key is your power.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⚡ ENCRYPT A MESSAGE", use_container_width=True, key="cta_btn", type="secondary"):
        st.info("The encryption page will be added soon.")

html("""
<div class="foot">
    <div class="foot-row">
        <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
        <div>SOUND-BASED ENCRYPTION</div>
    </div>
    <div class="foot-copyright">© 2026 CRYPTORIAN · ALL RIGHTS RESERVED · BUILT FOR PRIVACY</div>
</div>
""")
