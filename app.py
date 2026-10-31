import streamlit as st
from PIL import Image
st.set_page_config(page_title="TC PETROSCAN BOX Official", layout="centered")
st.markdown("<style>#MainMenu, footer, header, .viewerBadge_container__1QSob {display:none !important;}</style>", unsafe_allow_html=True)
try:
    st.image("logo.png", width=280)
except:
    st.markdown("<h1 style='text-align:center; color:gold;'>TC</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#D4AF37;'>TC PetroScan Box</h2><p style='text-align:center;'>Tandoh Caleb - UMaT</p>", unsafe_allow_html=True)
st.divider()
f = st.file_uploader("📸 Scan Rock", type=["jpg","png","jpeg"])
if f:
    st.image(Image.open(f), use_container_width=True)
    st.success("✅ Rock Scanned!")
st.caption("© TC Minerals Ghana")
