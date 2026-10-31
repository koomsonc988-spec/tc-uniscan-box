import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="TC PETROSCAN BOX",
    page_icon="💎",
    layout="centered"
)

# HIDE ALL STREAMLIT BADGES
st.markdown("""
<style>
#MainMenu, footer, header {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}
a[href*="streamlit"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# SHOW LOGO - SAFE WAY
try:
    st.image("logo.png", width=250)
except:
    try:
        st.image("logo.PNG", width=250)
    except:
        st.markdown("<h1 style='text-align:center; color:gold;'>TC</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#D4AF37;'>TC PetroScan Box</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Tandoh Caleb - UMaT</p>", unsafe_allow_html=True)

st.divider()

file = st.file_uploader("📸 Scan Rock", type=["jpg","png","jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    st.success("✅ Rock Scanned! Ready for AI Analysis")
    st.balloons()

st.markdown("<p style='text-align:center; font-size:12px; color:gray; margin-top:50px;'>© TC Minerals Ghana</p>", unsafe_allow_html=True)
