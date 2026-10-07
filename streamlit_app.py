import streamlit as st

st.set_page_config(
    page_title="FONT PREVIEW — CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Roboto+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500;600;700&family=Share+Tech+Mono&family=JetBrains+Mono:wght@300;400;500;600;700&family=Source+Code+Pro:wght@300;400;500;600;700&family=Inconsolata:wght@300;400;500;600;700&family=Ubuntu+Mono:wght@400;700&family=PT+Mono&family=Cousine:wght@400;700&family=Anonymous+Pro:wght@400;700&family=Overpass+Mono:wght@300;400;500;600;700&family=Red+Hat+Mono:wght@300;400;500;600;700&family=Noto+Sans+Mono:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&family=Major+Mono+Display&family=Nova+Mono&family=Share+Tech&family=Audiowide&display=swap');

html, body, .stApp {
    background: #000000 !important;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stApp > header { display: none; }

.block-container {
    max-width: 1100px !important;
    padding: 3rem 3rem 5rem 3rem !important;
}

.title {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    color: #00ff88;
    text-shadow: 0 0 30px rgba(0,255,136,0.6);
    text-align: center;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.3em;
    color: rgba(255,255,255,0.4);
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 4rem;
}

.font-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    color: #00ff88;
    text-transform: uppercase;
    margin: 3rem 0 1rem 0;
    padding: 0.5rem 1rem;
    border-left: 3px solid #00ff88;
    background: rgba(0,255,136,0.05);
    display: block;
}

.font-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.35);
    margin-bottom: 1.2rem;
    letter-spacing: 0.1em;
}

.para {
    font-size: 1.08rem;
    line-height: 2;
    color: rgba(255,255,255,0.75);
    font-weight: 300;
    padding-left: 1.8rem;
    border-left: 2px solid rgba(0,255,136,0.3);
    max-width: 900px;
}

.para strong {
    color: #00ff88;
    font-weight: 600;
    text-shadow: 0 0 25px rgba(0,255,136,0.6);
}

/* ═══ SANS-SERIF ═══ */
.f1 { font-family: 'Inter', sans-serif !important; }
.f2 { font-family: 'IBM Plex Sans', sans-serif !important; }
.f3 { font-family: 'Space Grotesk', sans-serif !important; }

/* ═══ MONOSPACE — MODERN ═══ */
.f4 { font-family: 'JetBrains Mono', monospace !important; }
.f5 { font-family: 'IBM Plex Mono', monospace !important; }
.f6 { font-family: 'Roboto Mono', monospace !important; }
.f7 { font-family: 'Space Mono', monospace !important; }
.f8 { font-family: 'Fira Code', monospace !important; }
.f9 { font-family: 'Source Code Pro', monospace !important; }
.f10 { font-family: 'Inconsolata', monospace !important; }
.f11 { font-family: 'Ubuntu Mono', monospace !important; }
.f12 { font-family: 'PT Mono', monospace !important; }
.f13 { font-family: 'Cousine', monospace !important; }
.f14 { font-family: 'Anonymous Pro', monospace !important; }
.f15 { font-family: 'Overpass Mono', monospace !important; }
.f16 { font-family: 'Red Hat Mono', monospace !important; }
.f17 { font-family: 'Noto Sans Mono', monospace !important; }
.f18 { font-family: 'DM Mono', monospace !important; }

/* ═══ DISPLAY / TECH ═══ */
.f19 { font-family: 'Major Mono Display', monospace !important; }
.f20 { font-family: 'Nova Mono', monospace !important; }
.f21 { font-family: 'Share Tech Mono', monospace !important; }
.f22 { font-family: 'Share Tech', sans-serif !important; }
.f23 { font-family: 'Audiowide', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="title">FONT PREVIEW</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">23 FONTS · CHOOSE THE BEST</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SAMPLE PARAGRAPH
# ═══════════════════════════════════════════════════════════════
sample = """
Every message you send carries a piece of you. Your words, your thoughts, your secrets —
they travel through networks you don't control, through servers you don't own,
through channels that can be intercepted. <strong>Encryption is not paranoia.</strong>
It is the basic right to keep your private life private. It is the difference between
a conversation and a broadcast. It is the line between your message and everyone
else's business.
"""

fonts = [
    # SANS-SERIF
    ("01 · Inter", "f1", "SANS-SERIF · Modern · Vercel, Linear, GitHub"),
    ("02 · IBM Plex Sans", "f2", "SANS-SERIF · Technical · IBM"),
    ("03 · Space Grotesk", "f3", "SANS-SERIF · Modern · Vercel, Linear"),

    # MONOSPACE — MODERN
    ("04 · JetBrains Mono", "f4", "MONO · Modern · Programming"),
    ("05 · IBM Plex Mono", "f5", "MONO · Technical · IBM"),
    ("06 · Roboto Mono", "f6", "MONO · Soft · Google"),
    ("07 · Space Mono", "f7", "MONO · Quirky · Google"),
    ("08 · Fira Code", "f8", "MONO · Programming"),
    ("09 · Source Code Pro", "f9", "MONO · Adobe"),
    ("10 · Inconsolata", "f10", "MONO · Clean"),
    ("11 · Ubuntu Mono", "f11", "MONO · Ubuntu"),
    ("12 · PT Mono", "f12", "MONO · ParaType"),
    ("13 · Cousine", "f13", "MONO · Courier-like"),
    ("14 · Anonymous Pro", "f14", "MONO · Mark Simonson"),
    ("15 · Overpass Mono", "f15", "MONO · Red Hat"),
    ("16 · Red Hat Mono", "f16", "MONO · Red Hat"),
    ("17 · Noto Sans Mono", "f17", "MONO · Google"),
    ("18 · DM Mono", "f18", "MONO · DeepMind"),

    # DISPLAY / TECH
    ("19 · Major Mono Display", "f19", "DISPLAY · Mono style"),
    ("20 · Nova Mono", "f20", "DISPLAY · Tech"),
    ("21 · Share Tech Mono", "f21", "CURRENT FONT"),
    ("22 · Share Tech", "f22", "TECH · Sans"),
    ("23 · Audiowide", "f23", "TECH · Wide"),
]

# ═══════════════════════════════════════════════════════════════
# DISPLAY EACH FONT
# ═══════════════════════════════════════════════════════════════
for name, cls, note in fonts:
    st.markdown(f'<div class="font-label">{name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="font-note">{note}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="para {cls}">{sample}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
