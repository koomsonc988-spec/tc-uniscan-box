import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="TC PETROSCAN BOX Official", page_icon="💎", layout="centered")

# HIDE STREAMLIT INSIDE APP
st.markdown("""
<style>
#MainMenu, footer, header, .viewerBadge_container__1QSob {display:none !important;}
</style>
""", unsafe_allow_html=True)

# SHOW LOGO - GUARANTEED
try:
    # Try to load your uploaded logo
    st.image("logo.png", width=280)
except:
    st.markdown("""
    <div style='text-align:center; background:black; padding:20px; border:2px solid #D4AF37; border-radius:15px;'>
    <h1 style='color:#D4AF37; font-size:60px; margin:0;'>TC</h1>
    <p style='color:gold;'>💎 TC MINERALS 💎</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#D4AF37;'>TC PetroScan Box</h2><p style='text-align:center;'>Tandoh Caleb - UMaT</p>", unsafe_allow_html=True)
st.divider()

f = st.file_uploader("📸 Scan Rock", type=["jpg","png","jpeg"])
if f:
    st.image(Image.open(f), use_container_width=True)
    st.success("✅ Rock Scanned!")

st.caption("© TC Minerals Ghana")
