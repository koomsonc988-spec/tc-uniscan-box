import streamlit as st
import time
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TC UniScan Box",
    page_icon="📦",
    layout="centered"
)

st.title("📦 TC UniScan Box")
st.subheader("Upload ANYTHING - AI Scans The Universe!")

# --- SETUP YOUR API KEY ---
# Get free key from: https://aistudio.google.com/app/apikey
API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- UPLOAD ---
uploaded_file = st.file_uploader("Upload ANYTHING", type=["jpg","png","jpeg","webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Upload", use_column_width=True)
    
    if st.button("🔍 SCAN UNIVERSE", type="primary"):
        with st.spinner("Scanning universe..."):
            # RETRY LOGIC FOR 503 ERROR
            for attempt in range(3):
                try:
                    response = model.generate_content([
                        "You are TC UniScan Box. Identify this image, be funny, creative and give universe-level insight. What is it?",
                        image
                    ])
                    st.success("✅ SCAN COMPLETE!")
                    st.write(response.text)
                    break  # Success, exit loop
                    
                except Exception as e:
                    error_text = str(e)
                    if "503" in error_text or "UNAVAILABLE" in error_text:
                        if attempt < 2:
                            st.warning(f"🚀 Universe busy (attempt {attempt+1}/3)... retrying in 2 seconds...")
                            time.sleep(2)
                            continue
                        else:
                            st.error("⚠️ AI is super busy right now (high demand). Please WAIT 30 seconds and click SCAN again. It works on 2nd try!")
                    else:
                        st.error(f"Error: {error_text}")
                        break

st.caption("By Tandoh Caleb | TC AI Ghana | UMaT")
