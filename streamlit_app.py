import streamlit as st

st.set_page_config(
    page_title="FONT PREVIEW — CRYPTORIAN",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Roboto+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

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

h1, h2, h3, p, div, span { background-color: transparent; }

.title {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    color: #00ff88;
    text-shadow: 0 0 30px rgba(0,255,136,0.6);
    text-align: center;
    margin-bottom: 3rem;
    text-transform: uppercase;
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
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
    margin-bottom: 1.5rem;
    letter-spacing: 0.1em;
}

.para {
    font-size: 1.08rem;
    line-height: 2;
    color: rgba(255,255,255,0.72);
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

/* ═══ FONTS ═══ */
.font-inter { font-family: 'Inter', sans-serif !important; }
.font-plex { font-family: 'IBM Plex Sans', sans-serif !important; }
.font-roboto-mono { font-family: 'Roboto Mono', monospace !important; }
.font-space { font-family: 'Space Grotesk', sans-serif !important; }
.font-fira { font-family: 'Fira Code', monospace !important; }
.font-share { font-family: 'Share Tech Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="title">FONT PREVIEW</div>', unsafe_allow_html=True)

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
    ("Inter", "font-inter", "Modern · Clean · Used by Vercel, Linear, GitHub"),
    ("IBM Plex Sans", "font-plex", "Technical · Elegant · Made by IBM"),
    ("Roboto Mono", "font-roboto-mono", "Monospace · Softer than Share Tech Mono"),
    ("Space Grotesk", "font-space", "Modern · Distinctive · Used by Vercel, Linear"),
    ("Fira Code", "font-fira", "Programming font · Clear technical character"),
    ("Share Tech Mono", "font-share", "Current font · Monospace · Tech feel"),
]

# ═══════════════════════════════════════════════════════════════
# DISPLAY EACH FONT
# ═══════════════════════════════════════════════════════════════
for name, cls, note in fonts:
    st.markdown(f'<div class="font-label">{name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="font-note">{note}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="para {cls}">{sample}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
