import streamlit as st
from PIL import Image
from google import genai
import time
from google.genai.errors import ServerError

st.set_page_config(page_title="TC UniScan Box", page_icon="🚀", layout="wide")

# Logo
try:
    st.image("logo.png", width=200)
except:
    pass

st.markdown("<h1 style='text-align:center;'>TC UniScan Box - AI Universe Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>By Tandoh Caleb - Powered by TC AI Ghana | Built for UMaT</p>", unsafe_allow_html=True)

# Get API Key from Secrets (you already posted it)
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    API_KEY = st.text_input("Paste FREE Gemini API Key", type="password")
    
uploaded = st.file_uploader("📦 Upload ANYTHING - Remote, TV, Box, Cable, Product", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    img.thumbnail((512, 512))
    st.image(img, caption="Scanned Image", use_container_width=True)
    
    client = genai.Client(api_key=API_KEY)
    
    prompt = """You are TC UniScan Box - AI Universe Scanner by Tandoh Caleb.
    Identify this object completely. Tell brand, model, buttons, functions, 
    and everything you can. Explain like you are scanning the universe."""
    
    with st.spinner("🔵 Scanning Universe..."):
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt, img]
                )
                break
            except ServerError:
                if attempt < 2:
                    time.sleep(3)
                else:
                    st.error("Google AI is busy (503). Wait 1 minute and click Upload again.")
                    st.stop()
    
    st.success("✅ TC UniScan Complete!")
    st.markdown(response.text)
    
elif uploaded and not API_KEY:
    st.warning("Add GOOGLE_API_KEY in Streamlit Secrets!")
