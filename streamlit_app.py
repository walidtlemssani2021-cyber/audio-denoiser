import base64
import math
import random

import streamlit as st

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html(code):
    clean = " ".join(line.strip() for line in code.split("\n") if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DIGITAL ARTWORK
# ═══════════════════════════════════════════════════════════════
def svg_img(svg, cls, alt):
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<img class="{cls}" alt="{alt}" src="data:image/svg+xml;base64,{b64}"/>'


def pulse_path(heights, width=520, mid=235, gap=16):
    d, x = f"M0 {mid}", 0
    for h in heights:
        d += f" H{x + gap}"
        x += gap
        d += f" L{x + 8} {mid - h} L{x + 16} {mid + h * 0.6} L{x + 24} {mid}"
        x += 24
    return d + f" H{width}"


def star_art():
    sph = ""
    for a in (0, 30, 60, 90, 120, 150):
        sph += f'<ellipse cx="400" cy="400" rx="{70 * abs(math.cos(math.radians(a))):.1f}" ry="70"/>'
    for lat in (-60, -30, 0, 30, 60):
        r = 70 * math.cos(math.radians(lat))
        y = 400 - 70 * math.sin(math.radians(lat))
        sph += f'<ellipse cx="400" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.28:.1f}"/>'
    field = "".join(
        f'<path d="M400 345 C{400 + s} 230 {400 + s} 570 400 455"/><path d="M400 345 C{400 - s} 230 {400 - s} 570 400 455"/>'
        for s in (110, 180, 250)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
<defs>
<radialGradient id="h"><stop offset="0" stop-color="#00d4ff" stop-opacity=".30"/><stop offset=".6" stop-color="#7b2ff7" stop-opacity=".12"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>
<radialGradient id="c"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#00ff88" stop-opacity=".85"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>
<linearGradient id="jt" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#00ff88" stop-opacity=".95"/><stop offset=".5" stop-color="#00d4ff" stop-opacity=".35"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></linearGradient>
<linearGradient id="jb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00ff88" stop-opacity=".95"/><stop offset=".5" stop-color="#00d4ff" stop-opacity=".35"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></linearGradient>
<linearGradient id="dg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#00d4ff"/><stop offset=".5" stop-color="#00ff88"/><stop offset="1" stop-color="#7b2ff7"/></linearGradient>
<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
</defs>
<style>
.r{{transform-origin:400px 400px;animation:s 50s linear infinite}}
.r2{{transform-origin:400px 400px;animation:s 80s linear infinite reverse}}
.o{{transform-origin:400px 400px;animation:s 14s linear infinite}}
.o2{{transform-origin:400px 400px;animation:s 22s linear infinite reverse}}
@keyframes s{{to{{transform:rotate(360deg)}}}}
.jet{{animation:p 2.2s ease-in-out infinite alternate}}
@keyframes p{{from{{opacity:.4}}to{{opacity:1}}}}
.d1{{animation:d 5s linear infinite}} .d2{{animation:d 9s linear infinite reverse}}
@keyframes d{{to{{stroke-dashoffset:-208}}}}
.core{{transform-origin:400px 400px;animation:b 2.2s ease-in-out infinite alternate}}
@keyframes b{{from{{transform:scale(.85)}}to{{transform:scale(1.2)}}}}
</style>
<circle cx="400" cy="400" r="395" fill="url(#h)"/>
<circle class="r" cx="400" cy="400" r="375" fill="none" stroke="#00d4ff" stroke-opacity=".55" stroke-width="10" stroke-dasharray="1 15"/>
<circle class="r2" cx="400" cy="400" r="330" fill="none" stroke="#00ff88" stroke-opacity=".35" stroke-width="2" stroke-dasharray="3 11"/>
<circle class="r" cx="400" cy="400" r="260" fill="none" stroke="#00ff88" stroke-opacity=".25" stroke-width="1" stroke-dasharray="40 8 4 8"/>
<g class="o"><rect x="656" y="396" width="9" height="9" fill="#00ff88"/></g>
<g class="o2"><rect x="725" y="396" width="7" height="7" fill="#00d4ff"/></g>
<g class="o"><rect x="136" y="396" width="6" height="6" fill="#7b2ff7"/></g>
<g transform="rotate(25 400 400)">
<polygon class="jet" points="400,392 318,0 482,0" fill="url(#jt)"/>
<polygon class="jet" points="400,408 318,800 482,800" fill="url(#jb)"/>
<g fill="none" stroke="#00d4ff" stroke-opacity=".35" stroke-width="1.2">{field}</g>
<ellipse cx="400" cy="400" rx="300" ry="62" fill="none" stroke="url(#dg)" stroke-width="9" opacity=".35" filter="url(#g)"/>
<ellipse class="d1" cx="400" cy="400" rx="300" ry="62" fill="none" stroke="url(#dg)" stroke-width="3" stroke-dasharray="40 12"/>
<ellipse class="d2" cx="400" cy="400" rx="205" ry="42" fill="none" stroke="#00ff88" stroke-width="1.5" stroke-dasharray="4 8" opacity=".8"/>
<g fill="none" stroke="#00ff88" stroke-opacity=".8" stroke-width="1">{sph}</g>
</g>
<circle class="core" cx="400" cy="400" r="95" fill="url(#c)"/>
<circle cx="400" cy="400" r="20" fill="#fff"/>
</svg>"""


def crypto_art():
    rnd = random.Random(5)
    cols = ""
    for c in range(18):
        chars = "".join(
            f'<text x="{16 + c * 28}" y="{22 + r * 27}" opacity="{.08 + .3 * rnd.random():.2f}">{rnd.choice("0123456789ABCDEF")}</text>'
            for r in range(14)
        )
        cols += f'<g style="animation-delay:{rnd.random() * 3:.2f}s">{chars}</g>'
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400">'
        '<defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00d4ff"/><stop offset=".6" stop-color="#00ff88"/><stop offset="1" stop-color="#7b2ff7"/></linearGradient>'
        '<radialGradient id="gl"><stop offset="0" stop-color="#00ff88" stop-opacity=".35"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>'
        '<filter id="b" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter></defs>'
        '<style>.m g{animation:fl 3s ease-in-out infinite alternate}@keyframes fl{from{opacity:.3}to{opacity:1}}'
        '.sh{animation:gl 2.4s ease-in-out infinite alternate}@keyframes gl{from{opacity:.75}to{opacity:1}}'
        '.rg{transform-origin:260px 205px;animation:s 30s linear infinite}@keyframes s{to{transform:rotate(360deg)}}'
        '.k{animation:k 1.6s steps(2) infinite}@keyframes k{50%{opacity:.2}}</style>'
        '<rect width="520" height="400" fill="#02060a"/>'
        '<g class="m" font-family="monospace" font-size="14" fill="#00ff88">' + cols + '</g>'
        '<circle cx="260" cy="205" r="170" fill="url(#gl)"/>'
        '<circle class="rg" cx="260" cy="205" r="172" fill="none" stroke="#00d4ff" stroke-opacity=".6" stroke-width="2" stroke-dasharray="2 12"/>'
        '<g class="sh">'
        '<path d="M260 62 L370 104 V205 C370 272 322 318 260 345 C198 318 150 272 150 205 V104 Z" fill="none" stroke="url(#sg)" stroke-width="10" opacity=".5" filter="url(#b)"/>'
        '<path d="M260 62 L370 104 V205 C370 272 322 318 260 345 C198 318 150 272 150 205 V104 Z" fill="#02060a" fill-opacity=".92" stroke="url(#sg)" stroke-width="3"/>'
        '<path d="M260 88 L346 121 V205 C346 258 309 296 260 318 C211 296 174 258 174 205 V121 Z" fill="none" stroke="#00ff88" stroke-opacity=".25"/>'
        '<path d="M236 196 V176 a24 24 0 0 1 48 0 V196" fill="none" stroke="#00ff88" stroke-width="5" stroke-linecap="round"/>'
        '<rect x="218" y="196" width="84" height="66" rx="9" fill="#00ff88" fill-opacity=".12" stroke="#00ff88" stroke-width="4"/>'
        '<g class="k"><circle cx="260" cy="224" r="7" fill="#fff"/><rect x="257.5" y="228" width="5" height="18" rx="2" fill="#fff"/></g>'
        '</g>'
        '<rect x="0" y="360" width="520" height="40" fill="#02060a" fill-opacity=".94"/>'
        '<g font-family="monospace" font-size="14"><text x="22" y="385" fill="#fff" fill-opacity=".85">MEET ME AT DAWN</text>'
        '<text x="260" y="385" fill="#00d4ff" text-anchor="middle">&#9658;&#9658;</text>'
        '<text x="498" y="385" fill="#00ff88" text-anchor="end">7F3A 9CE1 0B5D 42</text></g>'
        '<rect x="1" y="1" width="518" height="398" fill="none" stroke="#00ff88" stroke-opacity=".25"/></svg>'
    )


def pipeline_art():
    glyphs = ""
    for r in range(3):
        for c in range(14):
            h = 10 + int(14 * abs(math.sin(r * 7.3 + c * 1.7)))
            glyphs += (f'<rect x="{30 + c * 32}" y="{28 + r * 34 + (24 - h) / 2:.0f}" width="20" height="{h}" rx="2" '
                       f'fill="#00ff88" opacity="{.35 + .5 * abs(math.sin(r * 3 + c)):.2f}"/>')
    wave = pulse_path([22, 8, 28, 14, 6, 26, 18, 10, 30, 7, 20, 12])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 460">
<defs><radialGradient id="c"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#00ff88" stop-opacity=".8"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient>
<linearGradient id="j" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00d4ff" stop-opacity="0"/><stop offset=".5" stop-color="#00ff88" stop-opacity=".9"/><stop offset="1" stop-color="#00d4ff" stop-opacity="0"/></linearGradient></defs>
<style>.f{{animation:f 1.2s linear infinite}}@keyframes f{{to{{stroke-dashoffset:-20}}}}
.w{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:w 3s ease-out infinite alternate}}@keyframes w{{to{{stroke-dashoffset:0}}}}</style>
<rect width="520" height="460" fill="#02060a"/>
<g>{glyphs}</g>
<line class="f" x1="260" y1="140" x2="260" y2="180" stroke="#00ff88" stroke-width="2" stroke-dasharray="6 6"/>
<polygon points="250,178 270,178 260,194" fill="#00ff88"/>
<path class="w" d="{wave}" fill="none" stroke="#00ff88" stroke-width="2"/>
<line class="f" x1="260" y1="275" x2="260" y2="315" stroke="#00ff88" stroke-width="2" stroke-dasharray="6 6"/>
<polygon points="250,313 270,313 260,329" fill="#00ff88"/>
<circle cx="260" cy="395" r="48" fill="url(#c)"/>
<rect x="257" y="338" width="6" height="114" fill="url(#j)"/>
<ellipse cx="260" cy="395" rx="80" ry="14" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-dasharray="6 5"/>
<circle cx="260" cy="395" r="7" fill="#fff"/>
<rect x="1" y="1" width="518" height="458" fill="none" stroke="#00ff88" stroke-opacity=".25"/>
</svg>"""


def ridge_art():
    rnd = random.Random(11)
    rows = []
    for i in range(20):
        y0 = 80 + i * 17
        pts = " ".join(
            f"{x},{y0 - 62 * math.exp(-((x - 600) / 230) ** 2) * (0.3 + 0.7 * rnd.random()) - 2.5 * rnd.random():.1f}"
            for x in range(0, 1201, 12)
        )
        rows.append(f'<polygon points="0,{y0} {pts} 1200,{y0}" fill="#02060a" stroke="#00ff88" stroke-opacity="{.3 + .7 * i / 19:.2f}" stroke-width="1.4" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460"><rect width="1200" height="460" fill="#02060a"/>'
            '<defs><radialGradient id="g" cx=".5" cy=".55" r=".5"><stop offset="0" stop-color="#00ff88" stop-opacity=".16"/><stop offset="1" stop-color="#00ff88" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="1200" height="460" fill="url(#g)"/>' + "".join(rows) + '</svg>')


STAR = svg_img(star_art(), "hero-art", "Digital neutron star with polar jets")
NET = svg_img(crypto_art(), "art", "Padlock shield turning a plain message into encrypted code")
PIPE = svg_img(pipeline_art(), "art", "Text converted into pulses, then into a star")
RIDGE = svg_img(ridge_art(), "banner", "Stacked pulse profiles of a pulsar")

# ═══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

:root {
  --g: #00ff88; --c: #00d4ff; --p: #7b2ff7;
  --line: rgba(255,255,255,.08);
  --display: 'Orbitron', 'Space Grotesk', sans-serif;
  --head: 'JetBrains Mono', monospace;
  --sans: 'Space Grotesk', 'JetBrains Mono', sans-serif;
  --mono: 'JetBrains Mono', monospace;
}

html, body, .stApp { background:#000 !important; color:#fff; -webkit-font-smoothing:antialiased; overflow-x:hidden; }
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown div { font-family:var(--sans) !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
.block-container { max-width:1320px !important; padding:0 3rem 5rem 3rem !important; position:relative; z-index:3; }

h1, h2, h3 { font-family:var(--head) !important; text-transform:uppercase; }

.bg-layer { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.bg-orb { position:absolute; border-radius:50%; filter:blur(140px); will-change:transform; }
.orb-1 { width:700px; height:700px; background:radial-gradient(circle,var(--g) 0%,transparent 70%); top:-280px; left:-180px; opacity:.38; animation:f1 22s ease-in-out infinite; }
.orb-2 { width:600px; height:600px; background:radial-gradient(circle,var(--c) 0%,transparent 70%); top:35%; right:-220px; opacity:.26; animation:f2 28s ease-in-out infinite; }
.orb-3 { width:800px; height:800px; background:radial-gradient(circle,var(--p) 0%,transparent 70%); bottom:-380px; left:25%; opacity:.22; animation:f3 32s ease-in-out infinite; }
@keyframes f1 { 50% { transform:translate(120px,100px) scale(1.15); } }
@keyframes f2 { 50% { transform:translate(-140px,-120px) scale(1.2); } }
@keyframes f3 { 50% { transform:translate(100px,-100px) scale(1.1); } }
.bg-grid { position:absolute; inset:0; background-image:linear-gradient(rgba(0,255,136,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,136,.05) 1px,transparent 1px); background-size:70px 70px; -webkit-mask-image:radial-gradient(ellipse 90% 70% at 50% 40%,#000 15%,transparent 80%); mask-image:radial-gradient(ellipse 90% 70% at 50% 40%,#000 15%,transparent 80%); animation:gridShift 60s linear infinite; }
@keyframes gridShift { to { background-position:70px 70px; } }
.particle { position:absolute; width:3px; height:3px; background:var(--g); border-radius:50%; box-shadow:0 0 10px var(--g); animation:rise linear infinite; }
@keyframes rise { 0% { transform:translateY(100vh) scale(0); opacity:0; } 10%,90% { opacity:1; } 100% { transform:translateY(-100px) scale(1); opacity:0; } }

.nav { display:flex; justify-content:space-between; align-items:center; padding:1.3rem 3rem; margin:0 -3rem; position:relative; z-index:100; backdrop-filter:blur(24px) saturate(180%); -webkit-backdrop-filter:blur(24px) saturate(180%); background:rgba(0,0,0,.6); border-bottom:1px solid var(--line); }
.nav-brand { display:flex; align-items:center; gap:.85rem; font-family:var(--display); font-weight:900; font-size:1.05rem; letter-spacing:.3em; color:var(--g); text-shadow:0 0 30px rgba(0,255,136,.9); }
.nav-brand::before { content:''; width:11px; height:11px; background:var(--g); box-shadow:0 0 25px var(--g); transform:rotate(45deg); animation:spin 8s linear infinite; }
@keyframes spin { to { transform:rotate(405deg); } }
.nav-status { display:flex; align-items:center; gap:.5rem; font-family:var(--mono); font-size:.7rem; letter-spacing:.25em; color:var(--g); }
.nav-dot { width:7px; height:7px; border-radius:50%; background:var(--g); box-shadow:0 0 14px var(--g); animation:blink 1.8s infinite; }
@keyframes blink { 50% { opacity:.3; } }

.hero { padding:6.5rem 0 3rem 0; text-align:center; position:relative; }
.hero-badge { display:inline-flex; align-items:center; gap:.7rem; font-family:var(--mono); font-size:.7rem; letter-spacing:.3em; text-transform:uppercase; color:rgba(0,255,136,.9); padding:.7rem 1.8rem; border:1px solid rgba(0,255,136,.3); border-radius:100px; background:rgba(0,255,136,.05); margin-bottom:2.6rem; }
.hero-badge i { width:7px; height:7px; border-radius:50%; background:var(--g); box-shadow:0 0 14px var(--g); animation:blink 1.8s infinite; }

.hero-name {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900;
    font-size: clamp(2rem, 9vw, 7rem);
    line-height: 1;
    letter-spacing: .08em;
    margin: 0 auto 2rem auto;
    padding: 0;
    white-space: nowrap;
    background: linear-gradient(180deg, #fff 0%, #00ff88 60%, #00d4ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 70px rgba(0,255,136,.65));
    animation: glow 4s ease-in-out infinite;
}
@keyframes glow { 50% { filter: drop-shadow(0 0 110px rgba(0,255,136,.95)); } }

.hero-tagline {
    font-family: var(--mono);
    font-size: clamp(.7rem, 1.3vw, .9rem);
    letter-spacing: .22em;
    text-transform: uppercase;
    color: rgba(0,255,136,.9);
    text-shadow: 0 0 20px rgba(0,255,136,.6);
    margin: 0 auto 0.9rem auto;
    max-width: 950px;
    line-height: 1.9;
}

.hero-art { display:block; width:min(100%,640px); margin:2.5rem auto 0 auto; -webkit-mask-image:radial-gradient(circle closest-side,#000 80%,transparent 100%); mask-image:radial-gradient(circle closest-side,#000 80%,transparent 100%); }
.art { display:block; width:100%; max-width:520px; margin-top:1rem; border-radius:18px; border:1px solid rgba(0,255,136,.2); box-shadow:0 0 70px rgba(0,255,136,.08); }
.banner { display:block; width:100%; margin-top:5rem; border-radius:20px; border:1px solid rgba(0,255,136,.2); box-shadow:0 0 90px rgba(0,255,136,.08); }
.banner-cap { font-family:var(--mono); font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.4); text-align:center; margin-top:1rem; }

.stats-strip { display:grid; grid-template-columns:repeat(4,1fr); margin:4rem 0 2rem 0; border:1px solid rgba(0,255,136,.18); border-radius:20px; background:linear-gradient(145deg,rgba(0,255,136,.05),rgba(255,255,255,.01)); backdrop-filter:blur(20px); overflow:hidden; }
.stat-item { text-align:center; padding:2.2rem 1rem; }
.stat-item + .stat-item { border-left:1px solid var(--line); }
.stat-val { font-family:var(--head); font-size:2rem; font-weight:800; color:var(--g); text-shadow:0 0 25px rgba(0,255,136,.6); display:block; margin-bottom:.6rem; }
.stat-lbl { font-family:var(--mono); font-size:.65rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.45); }

.sec { padding:7rem 0 0 0; position:relative; }
.sec-grid { display:grid; grid-template-columns:1fr 1.2fr; gap:5rem; align-items:start; }

.sec-title {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900;
    font-size: clamp(1.3rem, 3vw, 2.4rem);
    line-height: 1.2;
    letter-spacing: .12em;
    color: #00ff88;
    text-shadow: 0 0 40px rgba(0,255,136,.6), 0 0 80px rgba(0,255,136,.3);
    margin: 0 0 2rem 0;
    text-transform: uppercase;
}

.text-block { font-size:1.08rem; color:rgba(255,255,255,.72); line-height:2; font-weight:300; margin:0 0 2rem 0; padding-left:1.8rem; border-left:2px solid rgba(0,255,136,.3); transition:all .4s ease; }
.text-block:hover { border-left-color:var(--g); color:rgba(255,255,255,.95); padding-left:2.4rem; }
.text-block strong { color:var(--g); font-weight:600; text-shadow:0 0 25px rgba(0,255,136,.6); }

.feat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.4rem; margin-top:3rem; }
.feat { position:relative; padding:2.4rem 2rem; background:linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); border:1px solid var(--line); border-radius:16px; overflow:hidden; transition:all .45s cubic-bezier(.4,0,.2,1); }
.feat::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,255,136,.9),transparent); opacity:0; transition:opacity .45s; }
.feat:hover { transform:translateY(-8px); border-color:rgba(0,255,136,.4); box-shadow:0 25px 70px rgba(0,0,0,.6), 0 0 90px rgba(0,255,136,.14); }
.feat:hover::before { opacity:1; }
.feat-icon { width:54px; height:54px; display:flex; align-items:center; justify-content:center; background:linear-gradient(145deg,rgba(0,255,136,.16),rgba(0,255,136,.03)); border:1px solid rgba(0,255,136,.3); border-radius:14px; font-size:1.5rem; color:var(--g); margin-bottom:1.5rem; text-shadow:0 0 20px rgba(0,255,136,.6); transition:all .45s; }
.feat:hover .feat-icon { box-shadow:0 0 30px rgba(0,255,136,.4); transform:scale(1.08) rotate(-5deg); }
.feat-t { font-family:var(--head); font-size:.9rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#fff; margin-bottom:.9rem; }
.feat-d { font-size:.97rem; color:rgba(255,255,255,.6); line-height:1.8; font-weight:300; }

.quote { max-width:900px; margin:7rem auto 0 auto; padding:3rem 3rem 3rem 4rem; border-left:4px solid var(--g); background:linear-gradient(90deg,rgba(0,255,136,.07),transparent); border-radius:0 20px 20px 0; position:relative; }
.quote::before { content:'"'; position:absolute; top:-18px; left:20px; font-family:var(--display); font-size:5rem; color:rgba(0,255,136,.3); line-height:1; }
.quote-text { font-size:1.4rem; font-weight:300; font-style:italic; color:rgba(255,255,255,.88); line-height:1.8; margin-bottom:1.4rem; }
.quote-author { font-family:var(--mono); font-size:.75rem; letter-spacing:.3em; text-transform:uppercase; color:rgba(0,255,136,.75); }

.cta { padding:6rem 3rem; text-align:center; border:1px solid rgba(0,255,136,.3); border-radius:28px; background:radial-gradient(ellipse at top,rgba(0,255,136,.18),transparent 60%),linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); position:relative; overflow:hidden; margin-top:7rem; }
.cta::before { content:''; position:absolute; inset:0; background-image:linear-gradient(rgba(0,255,136,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,136,.07) 1px,transparent 1px); background-size:40px 40px; -webkit-mask-image:radial-gradient(ellipse at center,#000 20%,transparent 70%); mask-image:radial-gradient(ellipse at center,#000 20%,transparent 70%); }
.cta-t { font-family:var(--head); font-weight:500; font-size:clamp(1.15rem, 2.8vw, 2.1rem); text-transform:uppercase; letter-spacing:.16em; line-height:1.5; color:var(--g); text-shadow:0 0 28px rgba(0,255,136,.45); margin-bottom:1rem; position:relative; }
.cta-d { font-size:1.05rem; color:rgba(255,255,255,.62); position:relative; font-weight:300; }

.stButton > button { background:linear-gradient(145deg,rgba(0,255,136,.12),rgba(0,255,136,.03)) !important; color:var(--g) !important; border:1px solid rgba(0,255,136,.55) !important; border-radius:12px !important; padding:1.1rem 2rem !important; font-family:var(--head) !important; font-weight:700 !important; font-size:.8rem !important; letter-spacing:.2em !important; text-transform:uppercase !important; transition:all .4s cubic-bezier(.4,0,.2,1) !important; width:100% !important; position:relative; z-index:3; }
.stButton > button:hover { color:#000 !important; background:var(--g) !important; border-color:var(--g) !important; box-shadow:0 0 50px rgba(0,255,136,.7), 0 0 100px rgba(0,255,136,.35) !important; transform:translateY(-3px); }
.stButton > button:focus-visible { outline:2px solid var(--c) !important; outline-offset:3px; }

.foot { margin-top:7rem; padding-top:2.5rem; border-top:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; font-family:var(--mono); font-size:.7rem; letter-spacing:.25em; text-transform:uppercase; color:rgba(255,255,255,.35); flex-wrap:wrap; gap:1rem; }
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
  .stat-item + .stat-item { border-left:none; border-top:1px solid var(--line); }
  .quote { padding:2rem 1.5rem; }
  .cta { padding:4rem 1.5rem; }
}
@media (prefers-reduced-motion:reduce) {
  .bg-orb, .bg-grid, .particle, .hero-name, .nav-brand::before { animation:none; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# BACKGROUND + PARTICLES
# ═══════════════════════════════════════════════════════════════
html("""
<div class="bg-layer">
    <div class="bg-grid"></div>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>
    <div class="particle" style="left: 10%; animation-duration: 12s; animation-delay: 0s;"></div>
    <div class="particle" style="left: 25%; animation-duration: 15s; animation-delay: 2s;"></div>
    <div class="particle" style="left: 45%; animation-duration: 10s; animation-delay: 4s;"></div>
    <div class="particle" style="left: 65%; animation-duration: 14s; animation-delay: 1s;"></div>
    <div class="particle" style="left: 85%; animation-duration: 11s; animation-delay: 3s;"></div>
    <div class="particle" style="left: 55%; animation-duration: 13s; animation-delay: 5s;"></div>
    <div class="particle" style="left: 35%; animation-duration: 16s; animation-delay: 6s;"></div>
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

# ═══════════════════════════════════════════════════════════════
# STATS STRIP
# ═══════════════════════════════════════════════════════════════
html("""
<div class="stats-strip">
    <div class="stat-item"><span class="stat-val">91</span><span class="stat-lbl">SIGNATURES</span></div>
    <div class="stat-item"><span class="stat-val">2000</span><span class="stat-lbl">MAX CHARS</span></div>
    <div class="stat-item"><span class="stat-val">80%</span><span class="stat-lbl">FLAC SAVING</span></div>
    <div class="stat-item"><span class="stat-val">3</span><span class="stat-lbl">SHAPES</span></div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# WHY ENCRYPTION MATTERS
# ═══════════════════════════════════════════════════════════════
html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHY ENCRYPTION MATTERS</h2>
        {NET}
    </div>
    <div>
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
  </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# QUOTE
# ═══════════════════════════════════════════════════════════════
html("""
<div class="quote">
    <p class="quote-text">The only way to keep a secret is to make sure no one knows you have one.</p>
    <p class="quote-author">— CRYPTORIAN PRINCIPLE</p>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# WHAT IS CRYPTORIAN
# ═══════════════════════════════════════════════════════════════
html(f"""
<div class="sec">
  <div class="sec-grid">
    <div>
        <h2 class="sec-title">WHAT IS CRYPTORIAN</h2>
        {PIPE}
    </div>
    <div>
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
  </div>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════════════
html(f"""
<div class="sec">
    <h2 class="sec-title">BUILT FOR THE PARANOID MIND</h2>
    <div class="feat-grid">
        <div class="feat">
            <div class="feat-icon">◉</div>
            <div class="feat-t">Neutron Sound</div>
            <div class="feat-d">Your message becomes a waveform modeled after a neutron star's pulse. It sounds like the cosmos — not like data.</div>
        </div>
        <div class="feat">
            <div class="feat-icon">▣</div>
            <div class="feat-t">Unique Signatures</div>
            <div class="feat-d">Every character — letter, digit, or symbol — has its own sonic signature. No two are ever alike.</div>
        </div>
        <div class="feat">
            <div class="feat-icon">⬢</div>
            <div class="feat-t">Key Shuffling</div>
            <div class="feat-d">The secret key reorders every signature. The same character produces a different pulse with every key.</div>
        </div>
        <div class="feat">
            <div class="feat-icon">◆</div>
            <div class="feat-t">Length Header</div>
            <div class="feat-d">The message length is embedded in the audio itself. Decryption knows exactly where the message ends.</div>
        </div>
        <div class="feat">
            <div class="feat-icon">▲</div>
            <div class="feat-t">Dual Formats</div>
            <div class="feat-d">Export as uncompressed WAV for universal playback, or as compressed FLAC for a much smaller file.</div>
        </div>
        <div class="feat">
            <div class="feat-icon">○</div>
            <div class="feat-t">Zero Knowledge</div>
            <div class="feat-d">Nothing is stored. Nothing is sent. The entire process happens in memory — invisible to anyone else.</div>
        </div>
    </div>
    {RIDGE}
    <p class="banner-cap">Illustration · stacked pulses of a rotating neutron star</p>
</div>
""")

# ═══════════════════════════════════════════════════════════════
# FINAL CTA
# ═══════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
html("""
<div class="foot">
    <div><span class="foot-brand">CRYPTORIAN</span> · V2.0 · 2026</div>
    <div>SOUND-BASED ENCRYPTION</div>
</div>
""")
