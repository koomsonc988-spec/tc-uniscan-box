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

# --- GOLD LOGO FOR IPHONE HOME SCREEN ---
st.markdown("""
<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/koomsonc988-spec/tc-petroscan-box/main/logo.png">
<link rel="apple-touch-icon" sizes="180x180" href="https://raw.githubusercontent.com/koomsonc988-spec/tc-petroscan-box/main/logo.png">
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("💎 TC PETROSCAN BOX")
st.write("AI Rock Classification for Geologists")

uploaded = st.file_uploader("Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Rock")
    # FIX: Classifier needs file bytes, not PIL image
    try:
        uploaded.seek(0)
        result = classify(uploaded)
    except:
        # If classifier wants PIL, try PIL
        result = classify(img)
    st.success(f"Result: {result}")
st.caption("Powered by TC Minerals - Ghana")
