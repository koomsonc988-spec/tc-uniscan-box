import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

st.set_page_config(page_title="TC UniScan Box", page_icon="🚀", layout="wide")

try:
    st.image("logo.png", width=200)
except:
    pass

st.markdown("<h1 style='text-align:center;'>TC UniScan Box - AI Universe Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>By Tandoh Caleb - TC AI Ghana | Built for UMaT</p>", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    API_KEY = st.text_input("Paste Gemini API Key", type="password")

uploaded = st.file_uploader("📦 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Image", use_container_width=True)
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = "You are TC UniScan Box by Tandoh Caleb. Scan this image and explain EVERYTHING - brand, model, all buttons, functions, how to use it. Be detailed like you scan the universe."
    
    with st.spinner("🔵 Scanning Universe..."):
        try:
            response = model.generate_content([prompt, img])
            st.success("✅ TC UniScan Complete!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}. Wait 30 sec and try again.")
else:
    if uploaded:
        st.warning("Add GOOGLE_API_KEY in Secrets!")
