import streamlit as st
from PIL import Image
from google import genai

# --- BRANDING ---
st.set_page_config(
    page_title="TC UniScan Box",
    page_icon="🌌",
    layout="centered"
)

# Custom header
st.markdown("""
<h1 style='text-align: center;'>🌌 TC UniScan Box</h1>
<h3 style='text-align: center; color: #FFD700;'>AI Universe Scanner by Tandoh Caleb</h3>
<p style='text-align: center; color: gray;'>Powered by TC AI Ghana | UMaT</p>
<hr>
""", unsafe_allow_html=True)

st.write("📸 **Scan ANYTHING in the Universe - Rock, Watch, Phone, Animal, Food**")

API_KEY = st.text_input("🔑 Paste FREE Gemini API Key", type="password", help="Get free at aistudio.google.com/app/apikey")
uploaded = st.file_uploader("📤 Upload Image", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    img.thumbnail((512, 512))
    st.image(img, use_column_width=True)
    try:
        client = genai.Client(api_key=API_KEY)
        with st.spinner("🌌 TC AI Scanning Universe..."):
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=["You are TC UniScan Box - AI Universe Scanner by Tandoh Caleb, powered by TC AI Ghana. Identify this image in detail: what it is, type, origin, use, composition, value, interesting facts. Be expert but simple.", img]
            )
        st.success("✅ Universe Scan Complete!")
        st.markdown(response.text)
        st.caption("🌌 TC UniScan Box | AI Universe Scanner by Tandoh Caleb | Powered by TC AI Ghana")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If model busy (503), change to gemini-3.6-flash")
elif uploaded:
    st.warning("👆 Paste API key first")

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px;'>© 2026 Tandoh Caleb - TC AI Ghana - UMaT</p>", unsafe_allow_html=True)
