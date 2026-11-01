import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TC UniScan Box", page_icon="icon.png", layout="centered")

# Header with your custom icon
col1, col2 = st.columns([1, 3])
with col1:
    try:
        st.image("icon.png", width=100)
    except:
        st.markdown("# 🧊")
with col2:
    st.title("TC UniScan Box")
    st.markdown("**By Tandoh Caleb | TC AI Ghana | UMaT**")

st.divider()

# API Key - Supports both AQ... and AIzaSy...
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or ""
    api_key = str(api_key).strip().strip('"').strip("'").strip()
except:
    api_key = ""

if not api_key:
    st.error("❌ API Key not found in Secrets! Add GEMINI_API_KEY")
    st.stop()

# Client that supports AQ keys
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Config Error: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload image to scan...", type=["jpg","jpeg","png","webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=uploaded_file.name, use_container_width=True)
    
    if st.button("🔴 SCAN UNIVERSE", use_container_width=True, type="primary"):
        with st.spinner("🌀 Scanning through the Universe with TC Cube..."):
            try:
                prompt = """You are TC UniScan Box AI - a glowing TC cube scanner.
                Analyze this image deeply. Identify device, give specs, features, network type, battery, usage guide.
                Add Ghana context (UMaT, TC AI Ghana). Use emojis, clear sections, professional style."""
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[prompt, image]
                )
                st.success("✅ Universe Scan Complete!")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("🧊 TC UniScan Box | Powered by Gemini | Built by Tandoh Caleb")
