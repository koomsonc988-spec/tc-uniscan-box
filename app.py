import streamlit as st
from PIL import Image
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="TC UniScan Box", page_icon="📦", layout="centered")

st.title("📦 TC UniScan Box")
st.markdown("**By Tandoh Caleb | TC AI Ghana | UMaT**")
st.divider()

# --- FIXED API KEY LOGIC ---
api_key = ""
try:
    # Try both names
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = ""
    # Clean it - remove spaces, new lines
    api_key = str(api_key).strip().replace("\n", "").replace("\r", "").replace(" ", "").replace('"', '').replace("'", "")
except Exception as e:
    api_key = ""

if not api_key:
    st.error("❌ API Key not found! Add GEMINI_API_KEY in Streamlit Secrets")
    st.info("Go to: Manage app -> Settings -> Secrets -> Add: GEMINI_API_KEY = \"AIzaSy...\"")
    st.stop()

# Check if key is wrong type (AQ key)
if api_key.startswith("AQ"):
    st.error("❌ This AQ... key will NOT work for Gemini!")
    st.warning("You need AIzaSy... key from aistudio.google.com/app/apikey")
    st.info("Go to aistudio.google.com/app/apikey -> Create API Key -> Copy AIzaSy key -> Paste in Secrets")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config Error: {e}")
    st.stop()

# Upload
uploaded_file = st.file_uploader("Upload image to scan...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"{uploaded_file.name} | {uploaded_file.size / 1024 / 1024:.1f}MB", use_column_width=True)
    
    if st.button("🔴 SCAN UNIVERSE", use_container_width=True):
        with st.spinner("Scanning through the Universe..."):
            try:
                prompt = """
                You are TC UniScan Box AI. Analyze this image deeply.
                Identify the device/object.
                If it's a Mifi/Router/Phone, give specs, features, network type, battery, how to use it.
                Be helpful, technical, and add Ghana context (UMaT, TC AI Ghana).
                Format with emojis and clear sections.
                """
                response = model.generate_content([prompt, image])
                st.success("✅ Scan Complete!")
                st.markdown(response.text)
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg or "400" in error_msg:
                    st.error("❌ API Key Invalid! Your AIzaSy key is wrong or not enabled.")
                    st.info("1. Go to aistudio.google.com/app/apikey\n2. Create NEW key (must start with AIzaSy)\n3. Paste in Streamlit Secrets as GEMINI_API_KEY\n4. Enable API: console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
                else:
                    st.error(f"Error: {error_msg}")

st.divider()
st.caption("Powered by Gemini 1.5 Flash | Built by Tandoh Caleb")
