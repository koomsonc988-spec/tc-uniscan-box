import streamlit as st
from PIL import Image

# Import classifier
try:
    from rock_classifier import classify
except Exception as e:
    def classify(img):
        return f"Classifier Error: {e}"

st.set_page_config(
    page_title="TC PETROSCAN BOX",
    page_icon="💎",
    layout="centered"
)

st.markdown("""
<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/koomsonc988-spec/tc-petroscan-box/main/logo.png">
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("TC PETROSCAN BOX")
st.write("AI Rock Classification for Geologists")

uploaded = st.file_uploader("Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Rock")
    
    # FIX FOR YOUR ERROR
    uploaded.seek(0)
    try:
        result = classify(uploaded)
    except AttributeError:
        # If it fails, try with PIL image
        result = classify(img)
    
    st.success(f"Result: {result}")

st.caption("Powered by TC Minerals - Ghana")
