import streamlit as st
import os
from PIL import Image
from rock_classifier import classify

st.set_page_config(page_title="TC PETROSCAN BOX", page_icon="💎", layout="centered")

# === HIDE STREAMLIT BRANDING ===
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    a[href^="https://streamlit.io"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# LOGO ON TOP - CENTER
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align:center;'>💎</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;color:#FFD700;'>TC PETROSCAN BOX</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Geologist AI Brain | Phone Camera Mode</p>", unsafe_allow_html=True)
