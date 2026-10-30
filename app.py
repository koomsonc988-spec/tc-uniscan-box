import streamlit as st
import os
from PIL import Image

# Try to import your classifier, if fails don't crash
try:
    from rock_classifier import classify
except:
    def classify(img):
        return "Unknown Rock - Classifier loading..."

st.set_page_config(
    page_title="TC PETROSCAN BOX",
    page_icon="💎",
    layout="centered"
)

# === HIDE STREAMLIT BRANDING - SAFE VERSION ===
st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# LOGO
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h2 style='text-align:center;color:#FFD700;'>TC PETROSCAN BOX</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Geologist AI Brain | Phone Camera Mode</p>", unsafe_allow_html=True)
st.markdown("---")

# CAMERA
camera_file = st.camera_input("Take a photo of a rock")

if camera_file is not None:
    image = Image.open(camera_file)
    st.image(image, caption="Captured", use_container_width=True)
    with st.spinner("Analyzing..."):
        try:
            result = classify(image)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check rock_classifier.py")
