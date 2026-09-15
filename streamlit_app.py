import streamlit as st
import torch
import torchaudio
from speechbrain.inference.enhancement import SpectralMaskEnhancement

st.set_page_config(page_title="إزالة الضوضاء الصوتية", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: #000000 !important;
    font-family: 'Inter', sans-serif;
}

.hero {
    text-align: center;
    padding: 20px 10px 10px;
}
.hero .mark {
    font-family: 'Fraunces', serif;
    color: #ffffff;
    opacity: 0.75;
    font-size: 14px;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 32px;
    color: #ffffff;
    margin: 6px 0 14px;
}
.hero p {
    color: #a3a3a3;
    font-size: 15px;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(160deg, #3fa0f5, #0a2a6b);
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.15);
}
[data-testid="stFileUploader"] * {
    color: #eaf3ff !important;
}

.stDownloadButton button, .stButton button {
    background: #ffffff !important;
    color: #000000 !important;
    border: none !important;
