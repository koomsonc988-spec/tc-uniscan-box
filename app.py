import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TC UniScan Box", page_icon="🚀", layout="wide")

try:
    st.image("logo.png", width=200)
except:
    pass

st.title("TC UniScan Box - AI Universe Scanner")
st.caption("By Tandoh Caleb - TC AI Ghana | Built for UMaT")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Add GOOGLE_API_KEY in Secrets!")
    st.stop()

uploaded = st.file_uploader("📦 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Scanned Image", use_container_width=True)
    
    prompt = "You are TC UniScan Box by Tandoh Caleb. Scan this image and explain EVERYTHING - brand, model, all buttons, functions, how to use it. Be detailed."
    
    with st.spinner("🔵 Scanning Universe..."):
        try:
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, img]
            )
            st.success("✅ TC UniScan Complete!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
