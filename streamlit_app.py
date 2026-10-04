import streamlit as st

# ═══ إعدادات الصفحة ═══
st.set_page_config(
    page_title="Neutron Cipher",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══ CSS مخصص (تصميم عصري) ═══
st.markdown("""
<style>
    /* الخلفية الرئيسية */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1e 100%);
        color: #e0e0e0;
    }
    
    /* إخفاء الهيدر الافتراضي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* العنوان الرئيسي */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #ff2e63);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* البطاقات */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 1rem;
    }
    
    /* الحقول */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem 2rem;
        color: #8892b0;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══ العنوان ═══
st.markdown('<h1 class="main-title">Neutron Cipher</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hide your messages inside the sound of a neutron star</p>', unsafe_allow_html=True)

# ═══ التبويبات ═══
tab1, tab2, tab3 = st.tabs(["🔐  Encrypt", "🔓  Decrypt", "ℹ️  About"])

# ═══ تبويب التشفير ═══
with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">📝 Your Message</h3>', unsafe_allow_html=True)
        message = st.text_area(
            "Enter your secret message",
            placeholder="Type your message here...",
            height=200,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🔑 Password</h3>', unsafe_allow_html=True)
        password = st.text_input(
            "Enter your password",
            type="password",
            placeholder="Choose a strong password",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        encrypt_btn = st.button("🔒  Encrypt Message", use_container_width=True)
    
    if encrypt_btn:
        st.info("🔧 Encryption engine will be integrated soon...")

# ═══ تبويب فك التشفير ═══
with tab2:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🎵 Upload Audio</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your audio file",
            type=["flac", "wav"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title">🔑 Password</h3>', unsafe_allow_html=True)
        decrypt_password = st.text_input(
            "Enter your password",
            type="password",
            placeholder="Enter the decryption password",
            label_visibility="collapsed",
            key="decrypt_pwd"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        decrypt_btn = st.button("🔓  Decrypt Message", use_container_width=True)
    
    if decrypt_btn:
        st.info("🔧 Decryption engine will be integrated soon...")

# ═══ تبويب حول ═══
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🌟 About Neutron Cipher
    
    **Neutron Cipher** is an experimental encryption system that hides 
    your messages inside the sound of a neutron star.
    
    #### 🔬 How it works
    1. Your message is encrypted with **Fernet** (AES-128 + HMAC)
    2. The encrypted bytes are converted into **pulsar-like sound waves**
    3. The result is a `.flac` audio file that sounds like a real neutron star
    
    #### 🛡️ Security
    - **AES-128** encryption
    - **HMAC** for integrity verification
    - **Random IV** for every encryption
    - **Password-based** key derivation (SHA-256)
    
    #### 📊 Features
    - Supports up to **2000 characters**
    - Works with **Arabic**, **English**, and **mixed** text
    - Supports **emojis** and **special characters**
    - High-quality audio (**44.1 kHz**)
    - Compact file size (**FLAC compression**)
    
    #### ⚠️ Important
    - Keep your password safe — **lost passwords cannot be recovered**
    - The audio file must not be modified — **HMAC detects tampering**
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══ التذييل ═══
st.markdown("""
<div style="text-align: center; color: #4a5568; padding: 3rem 0 1rem 0; font-size: 0.9rem;">
    Built with Streamlit · Powered by Astrophysics & Cryptography
</div>
""", unsafe_allow_html=True)
