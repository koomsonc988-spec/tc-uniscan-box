import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="TC PetroScan Box - Official", page_icon="💎", layout="centered")

# HIDE ALL STREAMLIT BRANDING - STRONGEST CODE 2026
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden !important; display: none !important;}
.viewerBadge_container__1QSob, .viewerBadge_link__1S137, .stDeployButton {display: none !important;}
[data-testid="stToolbar"], div[data-testid="stDecoration"], a[href*="streamlit.io"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# LOGO - GUARANTEED TO SHOW
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>TC</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">
<h2 style="color:#D4AF37;">TC PetroScan Box</h2>
<p style="color:gray;">Tandoh Caleb - UMaT</p>
</div>
""", unsafe_allow_html=True)

st.divider()
uploaded = st.file_uploader("📸 Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    st.image(Image.open(uploaded), use_container_width=True)
    st.success("✅ Rock Scanned!")

st.caption("© TC Minerals Ghana")
