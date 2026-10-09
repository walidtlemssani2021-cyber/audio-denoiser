import base64
import math
import random
import time
from html import escape

import streamlit as st

# ═══════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════
ACC, ACC_RGB = "#3da5ff", "61,165,255"
HOT, HOT_RGB = "#2b6bff", "43,107,255"
INK = "#ffffff"

# ═══════════════════════════════════════════════════════════════
# No-Cache
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
# ART 1 — NEUTRON STAR
# ═══════════════════════════════════════════════════════════════
def star_art():
    rnd = random.Random(7)
    cx, cy, R, W, T, L = 400, 280, 150, 600, 0.9, 540

    stars = "".join(
        f'<circle cx="{rnd.randint(0, 800)}" cy="{rnd.randint(0, 560)}" r="{rnd.uniform(0.4, 1.5):.2f}" fill="#fff" opacity="{rnd.uniform(0.15, 0.85):.2f}"/>'
        for _ in range(110)
    )

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
<rect width="800" height="560" fill="#000"/>
<g>{stars}</g>
<circle class="pulse" cx="{cx}" cy="{cy}" r="300" fill="url(#halo)"/>
<circle cx="{cx}" cy="{cy}" r="{R + 40}" fill="url(#rim)"/>

<g transform="rotate(20 {cx} {cy})">{back}</g>

<circle cx="{cx}" cy="{cy}" r="{R}" fill="#dcecff"/>
<g clip-path="url(#ball)">
<g transform="rotate(20 {cx} {cy})"><g class="tex">{texture}</g></g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#shade)"/>
</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#e6f2ff" stroke-opacity=".7" stroke-width="2"/>
<circle class="fl" cx="{cx}" cy="{cy}" r="{R + 30}" fill="url(#flare)"/>

<g clip-path="url(#out)"><g transform="rotate(20 {cx} {cy})">{front}</g></g>
</svg>"""


# ═══════════════════════════════════════════════════════════════
# ART 2 — ENCRYPTION
# ═══════════════════════════════════════════════════════════════
def crypto_art():
    rnd = random.Random(5)
    symbol_pool = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    letter_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digit_pool = "0123456789"
    pool = symbol_pool + symbol_pool + letter_pool + digit_pool
    colors = [ACC, INK, HOT]

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
<stop offset="0" stop-color="{ACC}" stop-opacity="0.35"/>
<stop offset="0.6" stop-color="{INK}" stop-opacity="0.06"/>
<stop offset="1" stop-color="{HOT}" stop-opacity="0"/>
</radialGradient>
</defs>
<rect width="520" height="400" fill="#000"/>
<circle cx="260" cy="200" r="230" fill="url(#glow)"/>
<g>{chars}</g>
<rect x="1" y="1" width="518" height="398" fill="none" stroke="{ACC}" stroke-opacity="0.3"/>
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

    down = "".join(f'<circle class="dn" style="animation-delay:{i * 0.5}s" cx="185" cy="182" r="3.5" fill="{ACC}"/>' for i in range(3))
    up = "".join(f'<circle class="up" style="animation-delay:{i * 0.5}s" cx="335" cy="298" r="3.5" fill="{INK}"/>' for i in range(3))

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
<rect width="520" height="480" fill="#000"/>

<rect x="40" y="36" width="440" height="130" rx="12" fill="{ACC}" fill-opacity=".04" stroke="{ACC}" stroke-opacity=".45"/>
<text x="60" y="62" font-family="monospace" font-size="11" letter-spacing="6" fill="{ACC}" opacity=".8">TEXT</text>
<text x="60" y="116" font-family="monospace" font-size="22" font-weight="bold" fill="{ACC}">YOUR TEXT<tspan class="cur">_</tspan></text>

<line class="flowD" x1="185" y1="176" x2="185" y2="294" stroke="{ACC}" stroke-width="2.5"/>
<polygon points="173,292 197,292 185,310" fill="{ACC}"/>
{down}
<text x="168" y="244" text-anchor="end" font-family="monospace" font-size="11" letter-spacing="3" fill="{ACC}">ENCRYPT</text>

<line class="flowU" x1="335" y1="304" x2="335" y2="186" stroke="{INK}" stroke-width="2.5"/>
<polygon points="323,188 347,188 335,170" fill="{INK}"/>
{up}
<text x="352" y="244" font-family="monospace" font-size="11" letter-spacing="3" fill="{INK}">DECRYPT</text>

<rect x="40" y="314" width="440" height="130" rx="12" fill="{INK}" fill-opacity=".04" stroke="{INK}" stroke-opacity=".4"/>
<text x="60" y="340" font-family="monospace" font-size="11" letter-spacing="6" fill="{INK}" opacity=".8">SOUND</text>
<path transform="translate(60 0)" d="{wave_d}" fill="none" stroke="{INK}" stroke-opacity=".6" stroke-width="2.2" stroke-linejoin="round"/>
<path class="sc" pathLength="1000" transform="translate(60 0)" d="{wave_d}" fill="none" stroke="{ACC}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="1" y="1" width="518" height="478" fill="none" stroke="{ACC}" stroke-opacity="0.25"/>
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
        rows.append(f'<polygon points="0,{y0} {pts} 1200,{y0}" fill="#000" stroke="{ACC}" stroke-opacity="{0.3 + 0.7 * i / 19:.2f}" stroke-width="1.4" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460"><rect width="1200" height="460" fill="#000"/>'
            f'<defs><radialGradient id="rg" cx="0.5" cy="0.55" r="0.5"><stop offset="0" stop-color="{ACC}" stop-opacity="0.14"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="1200" height="460" fill="url(#rg)"/>' + "".join(rows) + '</svg>')


STAR = svg_img(star_art(), "hero-art", "Neutron star spinning")
NET = svg_img(crypto_art(), "art", "Encryption symbols")
PIPE = svg_img(pipeline_art(), "art", "Text converted to sound and back")
RIDGE = svg_img(ridge_art(), "banner", "Pulse profiles")

# ═══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
ROOT = f"""
<style>
:root {{ --a:{ACC}; --ar:{ACC_RGB}; --h:{HOT}; --hr:{HOT_RGB}; --line:rgba(255,255,255,.12); }}
</style>
"""
st.markdown(ROOT, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Instrument+Serif:ital@0;1&family=Manrope:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

@property --n { syntax:'<integer>'; initial-value:0; inherits:false; }

*, *::before, *::after { box-sizing:border-box; }
html, body, .stApp { background:#000 !important; color:#fff; -webkit-font-smoothing:antialiased; overflow-x:hidden; scroll-behavior:smooth; }
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span { font-family:'Manrope',sans-serif !important; }
.stMarkdown .disp  { font-family:'Big Shoulders Display',sans-serif !important; }
.stMarkdown .serif { font-family:'Instrument Serif',serif !important; }
.stMarkdown .mono  { font-family:'DM Mono',monospace !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stHeaderActionElements"] { display:none !important; }
[data-testid="stVerticalBlock"] { gap:0 !important; }
.block-container { max-width:1260px !important; padding:0 2rem !important; position:relative; z-index:3; }
::selection { background:rgba(var(--ar),.45); color:#fff; }
::-webkit-scrollbar { width:8px; } ::-webkit-scrollbar-track { background:#000; } ::-webkit-scrollbar-thumb { background:rgba(var(--ar),.5); border-radius:4px; }
.bleed { width:100vw; margin-left:calc(50% - 50vw); }

/* ═══ BACKGROUND ═══ */
.bg-layer { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; background:#000; }
.bp { position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(rgba(var(--ar),.11) 1px,transparent 1px),linear-gradient(90deg,rgba(var(--ar),.11) 1px,transparent 1px); background-size:40px 40px,40px 40px,160px 160px,160px 160px; -webkit-mask-image:radial-gradient(ellipse 90% 70% at 60% 25%,#000 10%,transparent 78%); mask-image:radial-gradient(ellipse 90% 70% at 60% 25%,#000 10%,transparent 78%); }
.gl { position:absolute; border-radius:50%; filter:blur(140px); will-change:transform; }
.g1 { width:820px; height:820px; top:-420px; right:-260px; background:radial-gradient(circle,rgba(var(--ar),.5),transparent 70%); animation:drift 26s ease-in-out infinite; }
.g2 { width:700px; height:700px; bottom:-380px; left:-300px; background:radial-gradient(circle,rgba(var(--hr),.32),transparent 70%); animation:drift 34s ease-in-out infinite reverse; }
@keyframes drift { 50% { transform:translate(-90px,70px) scale(1.12); } }
.grain { position:absolute; inset:0; opacity:.08; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
.vig { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 40%,transparent 50%,rgba(0,0,0,.8) 100%); }

/* ═══ NAV ═══ */
.nav { position:fixed; top:0; left:0; right:0; z-index:1000; display:flex; justify-content:space-between; align-items:center; padding:.9rem clamp(1rem,3vw,2.2rem); background:rgba(0,0,0,.55); -webkit-backdrop-filter:blur(16px); backdrop-filter:blur(16px); border-bottom:1px solid rgba(255,255,255,.09); }
.nav-brand { display:flex; align-items:center; gap:.8rem; font-size:1.55rem; font-weight:900; letter-spacing:.22em; line-height:1; }
.nav-brand::before { content:''; width:11px; height:11px; border:2px solid var(--a); box-shadow:0 0 14px var(--a), inset 0 0 8px var(--a); transform:rotate(45deg); animation:blink 2.4s infinite; }
.nav-status { display:flex; align-items:center; gap:.55rem; font-size:.64rem; letter-spacing:.24em; color:rgba(255,255,255,.7); }
.nav-dot { width:7px; height:7px; border-radius:50%; background:var(--a); box-shadow:0 0 12px var(--a); animation:blink 1.6s infinite; }
@keyframes blink { 50% { opacity:.25; } }
.rail { position:fixed; left:12px; top:50%; transform:translateY(-50%) rotate(180deg); writing-mode:vertical-rl; z-index:50; font-size:.58rem; letter-spacing:.42em; color:rgba(255,255,255,.32); text-transform:uppercase; }
@media (max-width:1180px) { .rail { display:none; } }

/* ═══ HERO ═══ */
.hero { position:relative; padding:7.2rem 0 0 0; isolation:isolate; text-align:center; }
@keyframes fadeUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:none; } }
.hero-badge { display:inline-flex; align-items:center; gap:.7rem; font-size:.64rem; letter-spacing:.24em; text-transform:uppercase; color:rgba(255,255,255,.88); padding:.65rem 1.3rem; border:1px solid rgba(var(--ar),.45); background:rgba(var(--ar),.06); box-shadow:0 0 30px rgba(var(--ar),.18), inset 0 0 18px rgba(var(--ar),.08); animation:fadeUp .8s ease both; margin:0 auto; }
.hero-badge i { width:7px; height:7px; border-radius:50%; background:var(--a); box-shadow:0 0 12px var(--a); animation:blink 1.6s infinite; }
.stMarkdown h1.hero-name { font-family:'Big Shoulders Display',sans-serif !important; font-weight:900 !important; font-size:clamp(2.6rem,11vw,9rem) !important; line-height:.88 !important; letter-spacing:.005em !important; margin:1.3rem auto 0 auto !important; padding:0 !important; text-align:center; white-space:nowrap; position:relative;
  background:linear-gradient(105deg,transparent 42%,rgba(255,255,255,.95) 50%,transparent 58%) 150% 0/250% 100% no-repeat, linear-gradient(180deg,#fff 40%,var(--a) 135%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 40px rgba(var(--ar),.45));
  animation:fadeUp .9s ease .1s both, nameShine 5s linear 1.2s infinite; }
@keyframes nameShine { from { background-position:150% 0, 0 0; } to { background-position:-50% 0, 0 0; } }

div[data-testid="stHorizontalBlock"]:has(.star-wrap) { align-items:center; margin-top:1.5rem; }

/* ═══ TAGLINE — DM Mono (same as badge) ═══ */
.stMarkdown p.hero-tag {
    font-family: 'DM Mono', monospace !important;
    font-style: normal;
    font-size: clamp(0.75rem, 1.3vw, 0.95rem) !important;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(var(--ar),0.6);
    margin: 2rem 0 1.8rem 0 !important;
    text-align: center;
    line-height: 1.9;
    animation:fadeUp 1s ease .4s both;
}

.hero-meta { font-size:.62rem; letter-spacing:.26em; color:rgba(255,255,255,.45); margin-top:1.8rem; text-align:center; }

.star-wrap { position:relative; width:100%; max-width:780px; margin:0 auto; animation:fadeUp 1s ease .25s both; }
.star-wrap .hero-art { display:block; width:100%; margin:0; border:0 !important; border-radius:0 !important; box-shadow:none !important; -webkit-mask-image:radial-gradient(ellipse closest-side,#000 58%,transparent 100%); mask-image:radial-gradient(ellipse closest-side,#000 58%,transparent 100%); }

/* ═══ TICKER ═══ */
.ticker { overflow:hidden; margin-top:4.5rem; border-block:1px solid var(--line); background:rgba(var(--ar),.03); }
.tick-track { display:flex; width:max-content; animation:tick 40s linear infinite; padding:1rem 0; }
.tick-track span { font-size:.72rem; letter-spacing:.32em; text-transform:uppercase; color:rgba(255,255,255,.75); padding:0 1.4rem; white-space:nowrap; }
.tick-track b { color:var(--a); font-weight:500; text-shadow:0 0 12px var(--a); }
@keyframes tick { to { transform:translateX(-50%); } }

/* ═══ STATS ═══ */
.stats { display:grid; grid-template-columns:repeat(4,1fr); margin-top:6rem; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.stat { position:relative; padding:2.4rem 1.3rem 2rem 1.5rem; border-left:1px solid var(--line); }
.stat:first-child { border-left:0; padding-left:0; }
.stat::before { content:'+'; position:absolute; top:-.78rem; left:-.45rem; font-family:'DM Mono',monospace; color:var(--a); font-size:1.1rem; text-shadow:0 0 10px var(--a); }
.stat:first-child::before { left:-.45rem; }
.stat-val { display:block; font-weight:900; font-size:clamp(3.2rem,8.5vw,7rem); line-height:.9; letter-spacing:.01em; background:linear-gradient(180deg,#fff 30%,var(--a) 130%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; counter-reset:n var(--n); filter:drop-shadow(0 0 26px rgba(var(--ar),.35)); }
.stat-val::after { content:counter(n); }
.stat-val.pct::after { content:counter(n) "%"; }
.stat-lbl { display:block; margin-top:.9rem; font-size:.62rem; letter-spacing:.26em; text-transform:uppercase; color:rgba(255,255,255,.5); }

/* ═══ SECTIONS ═══ */
.sec { position:relative; padding-top:9rem; }
.stMarkdown h2.sec-title { font-family:'Big Shoulders Display',sans-serif !important; font-weight:900 !important; font-size:clamp(3rem,10.5vw,9rem) !important; line-height:.88 !important; letter-spacing:.005em !important; margin:0 0 3.2rem 0 !important; padding:0 !important; color:#fff !important; text-transform:uppercase !important; text-shadow:0 0 60px rgba(var(--ar),.25); }
.sec-body { display:grid; grid-template-columns:.95fr 1.05fr; gap:4.5rem; align-items:center; }
.rev .frame { order:2; }

.frame { position:relative; overflow:hidden; border:1px solid rgba(var(--ar),.3); background:#000; box-shadow:0 40px 100px rgba(var(--ar),.12); }
.frame::after { content:''; position:absolute; left:0; right:0; top:0; height:2px; z-index:4; pointer-events:none; background:linear-gradient(90deg,transparent,var(--a),transparent); box-shadow:0 0 18px var(--a), 0 0 40px rgba(var(--ar),.6); animation:scan 5s linear infinite; }
@keyframes scan { 0% { top:0; opacity:0; } 8%,92% { opacity:1; } 100% { top:100%; opacity:0; } }
.frame img.art { display:block; width:100%; max-width:none; margin:0; border:0; border-radius:0; box-shadow:none; }

.stMarkdown p.lead { font-family:'Instrument Serif',serif !important; font-size:clamp(1.3rem,2.2vw,1.78rem) !important; line-height:1.38 !important; font-weight:400 !important; color:#fff; margin:0 0 1.8rem 0 !important; }
.stMarkdown p.text-block { font-size:1.02rem !important; line-height:1.85 !important; font-weight:300 !important; color:rgba(255,255,255,.6); margin:0 !important; padding:0 0 0 1.3rem; border-left:2px solid var(--a); }
.stMarkdown p strong { color:#fff; font-weight:600; text-shadow:0 0 22px rgba(var(--ar),.7); }

/* ═══ QUOTE ═══ */
.quote { position:relative; margin:10rem 0 0 0; }
.quote-mark { display:block; font-size:clamp(8rem,22vw,19rem); line-height:.6; height:.45em; color:transparent; -webkit-text-stroke:1px rgba(var(--ar),.7); text-shadow:0 0 60px rgba(var(--ar),.4); }
.stMarkdown p.quote-text { font-family:'Instrument Serif',serif !important; font-style:italic; font-size:clamp(2.3rem,7vw,6.2rem) !important; line-height:1 !important; letter-spacing:-.01em !important; margin:0 !important; color:#fff; max-width:1100px; }
.hl { color:var(--a); text-shadow:0 0 40px rgba(var(--ar),.8); }
.stMarkdown p.quote-author { margin:2.4rem 0 0 0 !important; font-size:.7rem !important; letter-spacing:.34em; text-transform:uppercase; color:rgba(255,255,255,.6); }

/* ═══ FAQ ═══ */
.faq-list { border-top:1px solid var(--line); }
.faq-item { border-bottom:1px solid var(--line); transition:background .3s; counter-increment:q; }
.faq-list { counter-reset:q; }
.faq-item:hover { background:linear-gradient(90deg,rgba(var(--ar),.08),transparent 70%); }
.faq-item summary { display:flex; align-items:center; gap:1.6rem; padding:1.7rem .4rem; cursor:pointer; list-style:none; font-size:clamp(1.1rem,2.3vw,1.7rem); font-weight:500; color:#fff; line-height:1.25; }
.faq-item summary::-webkit-details-marker { display:none; }
.faq-item summary::before { content:counter(q,decimal-leading-zero); font-family:'DM Mono',monospace; font-size:.78rem; letter-spacing:.2em; color:var(--a); text-shadow:0 0 10px rgba(var(--ar),.8); flex:none; }
.faq-item summary::after { content:'+'; margin-left:auto; flex:none; width:38px; height:38px; display:grid; place-items:center; font-size:1.4rem; font-weight:300; color:var(--a); border:1px solid rgba(var(--ar),.5); transition:transform .35s, background .3s, color .3s; }
.faq-item[open] { background:linear-gradient(90deg,rgba(var(--ar),.1),transparent 75%); }
.faq-item[open] summary::after { transform:rotate(45deg); background:var(--a); color:#000; }
.faq-a { padding:0 .4rem 1.9rem 4.6rem; max-width:860px; font-size:1.02rem; line-height:1.85; font-weight:300; color:rgba(255,255,255,.65); }

/* ═══ BANNER ═══ */
.banner-wrap { margin-top:8rem; }
.banner-wrap img.banner { display:block; width:100%; margin:0; border:0; border-radius:0; box-shadow:none; -webkit-mask-image:radial-gradient(ellipse 75% 85% at 50% 50%,#000 35%,transparent 100%); mask-image:radial-gradient(ellipse 75% 85% at 50% 50%,#000 35%,transparent 100%); }
.stMarkdown p.banner-cap { margin:-1rem 0 0 0 !important; text-align:center; font-size:.64rem !important; letter-spacing:.28em; text-transform:uppercase; color:rgba(255,255,255,.4); }

/* ═══ CTA ═══ */
.cta { position:relative; margin-top:8rem; padding:6rem 2rem 9.5rem 2rem; text-align:center; overflow:hidden; isolation:isolate; border:1px solid rgba(var(--ar),.4); background:radial-gradient(70% 90% at 50% 0%,rgba(var(--ar),.26),transparent 70%), #02050c; box-shadow:0 0 120px rgba(var(--ar),.14), inset 0 0 80px rgba(var(--ar),.06); }
.cta::before { content:''; position:absolute; inset:0; z-index:-1; background-image:linear-gradient(rgba(var(--ar),.14) 1px,transparent 1px),linear-gradient(90deg,rgba(var(--ar),.14) 1px,transparent 1px); background-size:44px 44px; -webkit-mask-image:radial-gradient(ellipse at 50% 0%,#000 10%,transparent 72%); mask-image:radial-gradient(ellipse at 50% 0%,#000 10%,transparent 72%); }
.cta-t { font-weight:900; font-size:clamp(3.2rem,12vw,10.5rem); line-height:.86; letter-spacing:.005em; text-transform:uppercase; background:linear-gradient(180deg,#fff 35%,var(--a) 135%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 36px rgba(var(--ar),.5)); }
.cta-d { margin-top:1.8rem; font-family:'Instrument Serif',serif !important; font-style:italic; font-size:clamp(1.3rem,2.4vw,1.9rem); color:rgba(255,255,255,.8); }
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) { margin-top:-6.3rem; position:relative; z-index:6; }

/* ═══ BUTTONS ═══ */
.stButton > button { min-height:3.6rem !important; position:relative; overflow:hidden !important; transition:transform .3s, box-shadow .3s, background .3s !important; }
.stButton > button p { font-family:inherit !important; font-size:inherit !important; font-weight:inherit !important; letter-spacing:inherit !important; text-transform:inherit !important; color:inherit !important; margin:0 !important; line-height:1.2 !important; position:relative; z-index:1; }

/* PRIMARY BUTTON — Big Shoulders Display + BLUE GLOW */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5fb8ff 0%, var(--h) 100%) !important;
    color: #00081a !important;
    border: 1px solid rgba(160,215,255,.9) !important;
    border-radius: 12px !important;
    padding: 1.15rem 2.5rem !important;
    font-family: 'Big Shoulders Display', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.55rem !important;
    letter-spacing: .2em !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 30px rgba(var(--ar),.7), 0 0 70px rgba(var(--ar),.4), inset 0 0 20px rgba(255,255,255,.3) !important;
    animation: btnPulse 2.5s ease-in-out infinite !important;
}
@keyframes btnPulse {
    0%,100% { box-shadow: 0 0 30px rgba(var(--ar),.7), 0 0 70px rgba(var(--ar),.4), inset 0 0 20px rgba(255,255,255,.3); }
    50%     { box-shadow: 0 0 50px rgba(var(--ar),1), 0 0 110px rgba(var(--ar),.6), inset 0 0 30px rgba(255,255,255,.5); }
}
.stButton > button[kind="primary"]::before {
    content:''; position:absolute; top:0; left:-60%; width:40%; height:100%;
    background:linear-gradient(100deg,transparent,rgba(255,255,255,.7),transparent);
    transform:skewX(-20deg); animation:shine 3.4s ease-in-out infinite; pointer-events:none;
}
@keyframes shine { 0% { left:-60%; } 55%,100% { left:130%; } }
.stButton > button[kind="primary"]:hover { transform:translateY(-3px) scale(1.01); filter:brightness(1.1); }

.stButton > button[kind="secondary"] { background:rgba(2,5,12,.9) !important; color:#fff !important; border:1px solid rgba(var(--ar),.7) !important; border-radius:12px !important; padding:1.1rem 2.4rem !important; font-family:'Big Shoulders Display',sans-serif !important; font-weight:900 !important; font-size:1.4rem !important; letter-spacing:.2em !important; text-transform:uppercase !important; box-shadow:0 10px 40px rgba(0,0,0,.6), 0 0 30px rgba(var(--ar),.25) !important; }
.stButton > button[kind="secondary"]:hover { background:var(--a) !important; color:#00081a !important; border-color:#fff !important; transform:translateY(-3px); box-shadow:0 18px 60px rgba(var(--ar),.6) !important; }
.stButton > button:focus-visible { outline:2px solid #fff !important; outline-offset:3px; }

/* ═══ FOOTER ═══ */
.foot { margin-top:7rem; padding-top:2rem; border-top:1px solid var(--line); }
.foot-row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; font-size:.66rem; letter-spacing:.24em; text-transform:uppercase; color:rgba(255,255,255,.42); }
.foot-brand { color:#fff; text-shadow:0 0 20px rgba(var(--ar),.7); }
.foot-copyright { margin-top:1.1rem; font-size:.6rem; letter-spacing:.2em; text-transform:uppercase; color:rgba(255,255,255,.28); }
.foot-mark { margin-top:2.5rem; text-align:center; white-space:nowrap; font-weight:900; font-size:clamp(3rem,19.5vw,17rem); letter-spacing:.005em; line-height:.78; height:.64em; overflow:hidden; user-select:none; background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(var(--ar),.04) 88%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }

.stat-val { animation:cnt 2.6s ease-out both; }
@keyframes cnt { from { --n:0; } }

@media (max-width:900px) {
  .sec-body { grid-template-columns:1fr; gap:2.4rem; }
  .rev .frame { order:0; }
  .stats { grid-template-columns:1fr 1fr; }
  .stat:nth-child(3) { border-left:0; padding-left:0; }
  .stat:nth-child(n+3) { border-top:1px solid var(--line); }
  .faq-a { padding-left:.4rem; }
}
@media (max-width:700px) {
  .block-container { padding:0 1.1rem !important; }
  .hero { padding-top:6rem; }
  .hero-badge { letter-spacing:.12em; font-size:.56rem; padding:.6rem 1rem; line-height:1.7; }
  .sec { padding-top:6rem; }
  .cta { padding:4.5rem 1.2rem 9rem 1.2rem; }
  .quote { margin-top:6rem; }
  .faq-item summary { gap:1rem; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE
# ═══════════════════════════════════════════════════════════════
html("""
<div class="bg-layer"><div class="bp"></div><div class="gl g1"></div><div class="gl g2"></div><div class="grain"></div><div class="vig"></div></div>
<div class="rail mono">CRYPTORIAN — SOUND-BASED ENCRYPTION — 2026</div>
<div class="nav">
    <div class="nav-brand disp">CRYPTORIAN</div>
    <div class="nav-status mono"><div class="nav-dot"></div>OPERATIONAL</div>
</div>
""")

html("""
<div class="hero">
    <div class="hero-badge mono"><i></i>DM SAFELY AND SECURE YOUR PRIVACY WITH</div>
    <h1 class="hero-name">CRYPTORIAN</h1>
</div>
""")

html(f"""
<div class="star-wrap" style="max-width:780px;margin:2.5rem auto 0 auto;">{STAR}</div>
""")

html("""<p class="hero-tag">Using an encrypted modified neutron star sound</p>""")

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("LET'S START!", use_container_width=True, type="primary"):
        st.info("The encryption page will be added soon.")

TICKS = ["NEUTRON SOUND", "UNIQUE SIGNATURES", "KEY SHUFFLING", "LENGTH HEADER", "DUAL FORMATS", "ZERO KNOWLEDGE"]
TICK = "".join(f"<span>{t}</span><span><b>//</b></span>" for t in TICKS) * 2

html(f"""
<div class="bleed ticker mono" style="margin-top:4.5rem;"><div class="tick-track">{TICK}</div></div>

<div class="stats">
    <div class="stat"><span class="stat-val disp" style="--n:91"></span><span class="stat-lbl mono">SIGNATURES</span></div>
    <div class="stat"><span class="stat-val disp" style="--n:2000"></span><span class="stat-lbl mono">MAX CHARS</span></div>
    <div class="stat"><span class="stat-val disp pct" style="--n:80"></span><span class="stat-lbl mono">FLAC SAVING</span></div>
    <div class="stat"><span class="stat-val disp" style="--n:3"></span><span class="stat-lbl mono">SHAPES</span></div>
</div>
""")

html(f"""
<div class="sec">
  <h2 class="sec-title">WHY ENCRYPTION MATTERS</h2>
  <div class="sec-body">
    <div class="frame hud">{NET}</div>
    <div>
        <p class="lead">Before anything else, let it be known that a person who encrypts their messages is not always a criminal, nor is he suffering from paranoia. Every message you send — carrying your words, your thoughts, your secrets — travels through networks you don't know are safe or not, through servers you don't own, and through channels that are easy to intercept. This increases the risk of your data being obtained and exposes you to surveillance or blackmail.</p>
        <p class="text-block"><strong>And here comes the role of encryption</strong> — and not just any type of encryption. A private encryption. Encrypting your message using a complex, uncommon method. Using a special encryption method will guarantee you a great deal of security and legitimate privacy. And here comes the role of Criptorian.</p>
    </div>
  </div>
</div>
""")

html(f"""
<div class="sec rev">
  <h2 class="sec-title">WHAT IS CRYPTORIAN</h2>
  <div class="sec-body">
    <div class="frame hud">{PIPE}</div>
    <div>
        <p class="lead">Criptorian is a modern encryption program built to enhance the preservation of legitimate privacy and to combat the phenomenon of data leakage or unauthorized access by unwanted or disliked individuals or entities. Criptorian takes your written message and converts it into a modified sound wave derived from real sound waves emitted by a neutron star. It can also decrypt the resulting sound wave and convert it back into text.</p>
        <p class="text-block"><strong>The reason for using this type of sound for encryption</strong> is the founder's taste and his fascination with the incomprehensible sound waves emitted by neutron stars.</p>
    </div>
  </div>
</div>

<div class="quote">
    <span class="quote-mark serif">"</span>
    <p class="quote-text">The only way to keep a secret is to make sure no one knows you <span class="hl">have one.</span></p>
    <p class="quote-author mono">- Criptorian founder -</p>
</div>
""")

html("""
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
</div>
""")

html(f"""
<div class="bleed banner-wrap">{RIDGE}</div>
<p class="banner-cap mono">Illustration · stacked pulse profiles</p>

<div class="cta">
    <div class="cta-t disp">READY TO BECOME A STAR</div>
    <div class="cta-d">Your message is waiting. Your key is your power.</div>
</div>
""")

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⚡ ENCRYPT A MESSAGE", use_container_width=True, key="cta_btn", type="secondary"):
        st.info("The encryption page will be added soon.")

html("""
<div class="foot">
    <div class="foot-row mono">
        <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
        <div>SOUND-BASED ENCRYPTION</div>
    </div>
    <div class="foot-copyright mono">© 2026 CRYPTORIAN · ALL RIGHTS RESERVED · BUILT FOR PRIVACY</div>
    <div class="foot-mark disp">CRYPTORIAN</div>
</div>
""")
