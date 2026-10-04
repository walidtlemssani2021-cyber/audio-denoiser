import streamlit as st

st.set_page_config(
    page_title="NEUTRON CIPHER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;800&family=Orbitron:wght@400;700;900&display=swap');

    /* ═══ الأساسيات ═══ */
    * { font-family: 'JetBrains Mono', monospace !important; }

    .stApp {
        background: #000000;
        background-image:
            radial-gradient(ellipse at top, rgba(0, 255, 136, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom, rgba(0, 150, 255, 0.05) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 136, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #00ff88;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ═══ العنوان الرئيسي ═══ */
    .cyber-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        color: #00ff88;
        text-shadow:
            0 0 10px #00ff88,
            0 0 20px #00ff88,
            0 0 40px #00ff88,
            0 0 80px rgba(0, 255, 136, 0.5);
        letter-spacing: 8px;
        margin: 2rem 0 0.5rem 0;
        animation: flicker 3s infinite alternate;
    }

    @keyframes flicker {
        0%, 100% { opacity: 1; }
        95% { opacity: 1; }
        96% { opacity: 0.7; }
        97% { opacity: 1; }
        98% { opacity: 0.85; }
    }

    .cyber-subtitle {
        text-align: center;
        color: #00ff88;
        opacity: 0.6;
        font-size: 0.9rem;
        letter-spacing: 4px;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .cyber-line {
        width: 60%;
        height: 1px;
        margin: 1rem auto 3rem auto;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        box-shadow: 0 0 15px #00ff88;
    }

    /* ═══ البطاقات ═══ */
    .cyber-card {
        background: rgba(0, 10, 5, 0.8);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        box-shadow:
            0 0 20px rgba(0, 255, 136, 0.1),
            inset 0 0 20px rgba(0, 255, 136, 0.02);
    }

    .cyber-card::before {
        content: '';
        position: absolute;
        top: -1px; left: -1px;
        width: 20px; height: 20px;
        border-top: 2px solid #00ff88;
        border-left: 2px solid #00ff88;
    }

    .cyber-card::after {
        content: '';
        position: absolute;
        bottom: -1px; right: -1px;
        width: 20px; height: 20px;
        border-bottom: 2px solid #00ff88;
        border-right: 2px solid #00ff88;
    }

    .cyber-label {
        font-size: 0.75rem;
        color: #00ff88;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }

    .cyber-label::before {
        content: '▸ ';
        color: #00ff88;
    }

    /* ═══ الحقول ═══ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.4) !important;
        border-radius: 2px !important;
        color: #00ff88 !important;
        font-family: 'JetBrains Mono', monospace !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        caret-color: #00ff88 !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5) !important;
    }

    /* ═══ الأزرار ═══ */
    .stButton > button {
        background: transparent !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
        border-radius: 2px !important;
        padding: 0.9rem 2rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        background: #00ff88 !important;
        color: #000000 !important;
        box-shadow:
            0 0 20px #00ff88,
            0 0 40px rgba(0, 255, 136, 0.5) !important;
    }

    /* ═══ التبويبات ═══ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        justify-content: center;
        border-bottom: 1px solid rgba(0, 255, 136, 0.2);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 1rem 2.5rem;
        color: #00ff88;
        opacity: 0.5;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #00ff88 !important;
        opacity: 1 !important;
        border-bottom: 2px solid #00ff88 !important;
        text-shadow: 0 0 10px #00ff88;
    }

    /* ═══ الحالة ═══ */
    .cyber-status {
        background: rgba(0, 255, 136, 0.05);
        border-left: 3px solid #00ff88;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    .cyber-status-ok { color: #00ff88; }
    .cyber-status-err { color: #ff2e63; border-left-color: #ff2e63; background: rgba(255, 46, 99, 0.05); }

    /* ═══ شريط المعلومات ═══ */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px dashed rgba(0, 255, 136, 0.15);
        font-size: 0.8rem;
    }

    .info-key { color: rgba(0, 255, 136, 0.6); }
    .info-val { color: #00ff88; }

    /* ═══ الفوتر ═══ */
    .cyber-footer {
        text-align: center;
        color: rgba(0, 255, 136, 0.3);
        padding: 3rem 0 1rem 0;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ═══ File Uploader ═══ */
    .stFileUploader > div {
        background: rgba(0, 0, 0, 0.6) !important;
        border: 1px dashed rgba(0, 255, 136, 0.4) !important;
        border-radius: 2px !important;
    }

    .stFileUploader label {
        color: #00ff88 !important;
    }

    /* ═══ Alert ═══ */
    .stAlert {
        background: rgba(0, 255, 136, 0.05) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #00ff88 !important;
        border-radius: 2px !important;
    }

    /* ═══ Audio Player ═══ */
    audio {
        width: 100%;
        filter: invert(1) hue-rotate(90deg);
    }
</style>
""", unsafe_allow_html=True)

# ═══ العنوان ═══
st.markdown('<h1 class="cyber-title">NEUTRON CIPHER</h1>', unsafe_allow_html=True)
st.markdown('<p class="cyber-subtitle">[ hide your data in the sound of a dead star ]</p>', unsafe_allow_html=True)
st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

# ═══ التبويبات ═══
tab1, tab2, tab3 = st.tabs(["ENCRYPT", "DECRYPT", "SYSTEM"])

# ═══ تبويب التشفير ═══
with tab1:
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="cyber-label">payload_input</div>', unsafe_allow_html=True)
        message = st.text_area(
            "message",
            placeholder="> enter your secret message_",
            height=220,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="cyber-label">encryption_key</div>', unsafe_allow_html=True)
        password = st.text_input(
            "password",
            type="password",
            placeholder="> ••••••••",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        encrypt_btn = st.button("⚡ ENCRYPT", use_container_width=True)

    if encrypt_btn:
        st.markdown(
            '<div class="cyber-status">[ SYSTEM ] encryption engine not yet integrated...</div>',
            unsafe_allow_html=True
        )

# ═══ تبويب فك التشفير ═══
with tab2:
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="cyber-label">audio_source</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "upload",
            type=["flac", "wav"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="cyber-label">decryption_key</div>', unsafe_allow_html=True)
        decrypt_password = st.text_input(
            "password2",
            type="password",
            placeholder="> ••••••••",
            label_visibility="collapsed",
            key="decrypt_pwd"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        decrypt_btn = st.button("🔓 DECRYPT", use_container_width=True)

    if decrypt_btn:
        st.markdown(
            '<div class="cyber-status">[ SYSTEM ] decryption engine not yet integrated...</div>',
            unsafe_allow_html=True
        )

# ═══ تبويب النظام ═══
with tab3:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown('<div class="cyber-label">system_info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-row"><span class="info-key">PROTOCOL</span><span class="info-val">FERNET / AES-128-CBC</span></div>
    <div class="info-row"><span class="info-key">INTEGRITY</span><span class="info-val">HMAC-SHA256</span></div>
    <div class="info-row"><span class="info-key">KEY_DERIVATION</span><span class="info-val">SHA-256</span></div>
    <div class="info-row"><span class="info-key">IV</span><span class="info-val">RANDOM / PER-SESSION</span></div>
    <div class="info-row"><span class="info-key">CARRIER</span><span class="info-val">NEUTRON_STAR_PULSE</span></div>
    <div class="info-row"><span class="info-key">SAMPLE_RATE</span><span class="info-val">44100 HZ</span></div>
    <div class="info-row"><span class="info-key">CODEC</span><span class="info-val">FLAC / LOSSLESS</span></div>
    <div class="info-row"><span class="info-key">MAX_PAYLOAD</span><span class="info-val">2000 CHARACTERS</span></div>
    <div class="info-row"><span class="info-key">STATUS</span><span class="info-val">● OPERATIONAL</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown('<div class="cyber-label">warning</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: rgba(255, 46, 99, 0.8); font-size: 0.85rem; line-height: 1.8;">
    > LOST PASSWORDS CANNOT BE RECOVERED<br>
    > TAMPERED AUDIO WILL FAIL INTEGRITY CHECK<br>
    > AUDIO MUST NOT BE COMPRESSED OR CONVERTED<br>
    > SHARE THE .FLAC FILE, NEVER THE PASSWORD
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══ الفوتر ═══
st.markdown("""
<div class="cyber-footer">
    [ NEUTRON CIPHER v1.0 ] · ASTRONOMY × CRYPTOGRAPHY · 2026
</div>
""", unsafe_allow_html=True)
