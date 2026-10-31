import streamlit as st
from PIL import Image

try:
    from rock_classifier import classify
except Exception as e:
    def classify(img):
        return f"Analysis Error: {e}"

st.set_page_config(
    page_title="TC PETROSCAN BOX - Official",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ULTIMATE HIDE ALL STREAMLIT BRANDING
st.markdown("""
<style>
/* Hide everything Streamlit */
#MainMenu {visibility: hidden !important; display: none !important;}
footer {visibility: hidden !important; display: none !important; height: 0px !important;}
header {visibility: hidden !important; display: none !important;}
.stDeployButton {display:none !important;}
div[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
div[data-testid="stDecoration"] {display:none !important;}
div[data-testid="stStatusWidget"] {display:none !important;}
div[data-testid="stBottom"] {display:none !important;}
.viewerBadge_container__1QSob {display:none !important;}
.viewerBadge_link__1STli {display:none !important;}
a[href^="https://streamlit.io"] {display:none !important;}
footer:after {display:none !important;}
.stApp > footer {display:none !important;}
[data-testid="stAppViewContainer"] > footer {display:none !important;}
/* Hide Made with Streamlit */
iframe {display:none !important;}
</style>
""", unsafe_allow_html=True)

# YOUR TC LOGO - CENTERED BIG
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown("<h2 style='text-align:center; color:#D4AF37; margin-top:0px;'>TC PetroScan Box</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Tandoh Caleb - UMaT<br>AI Rock Classification</p>", unsafe_allow_html=True)
st.divider()

uploaded = st.file_uploader("📸 Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Rock", use_container_width=True)
    uploaded.seek(0)
    try:
        result = classify(uploaded)
    except:
        result = classify(img)
    st.success(f"✅ Result: {result}")
    st.balloons()

st.markdown("<p style='text-align:center; font-size:12px; color:gray; margin-top:50px;'>© 2026 TC Minerals Ghana - All Rights Reserved</p>", unsafe_allow_html=True)
