import streamlit as st
from PIL import Image

# Import classifier
try:
    from rock_classifier import classify
except Exception as e:
    def classify(img):
        return f"Analysis Error: {e}"

st.set_page_config(
    page_title="TC PETROSCAN BOX - Official",
    page_icon="💎",
    layout="centered"
)

# REMOVE STREAMLIT BRANDING
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stToolbar"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# SHOW YOUR LOGO
st.image("logo.png", width=250)

st.markdown("""
<h2 style='text-align:center; color:#D4AF37;'>TC PetroScan Box</h2>
<p style='text-align:center;'>Tandoh Caleb - UMaT<br>AI Rock Classification</p>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Rock", use_container_width=True)
    uploaded.seek(0)
    try:
        result = classify(uploaded)
    except:
        result = classify(img)
    st.success(f"Result: {result}")

st.caption("© TC Minerals Ghana")
