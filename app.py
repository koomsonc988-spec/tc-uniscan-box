import streamlit as st
from PIL import Image

# Import classifier
try:
    from rock_classifier import classify
except Exception as e:
    def classify(img):
        return f"Classifier Error: {e}"

st.set_page_config(
    page_title="TC PETROSCAN BOX - Official",
    page_icon="💎",
    layout="centered",
    menu_items={
        'About': "© TC Minerals Ghana - Professional Geological AI"
    }
)

# --- REMOVE STREAMLIT BRANDING ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            [data-testid="stDecoration"] {visibility: hidden !important;}
            [data-testid="stStatusWidget"] {visibility: hidden !important;}
            .viewerBadge_container__1QSob {display: none !important;}
            .styles_viewerBadge__1yB5_ {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("💎 TC PETROSCAN BOX")
st.write("AI Rock Classification for Geologists")

uploaded = st.file_uploader("Scan Rock", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Rock")
    uploaded.seek(0)
    try:
        result = classify(uploaded)
    except:
        result = classify(img)
    st.success(f"Result: {result}")

st.caption("Powered by TC Minerals - Ghana")
