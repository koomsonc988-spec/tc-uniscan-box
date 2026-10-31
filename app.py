import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TC Universe Scan", page_icon="🌍")
st.title("🌍 TC-Universe-Scan-Box")

API_KEY = st.text_input("Paste FREE Gemini API Key", type="password")
uploaded = st.file_uploader("📸 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    img.thumbnail((512, 512))
    st.image(img, width=500)
    try:
        client = genai.Client(api_key=API_KEY)
        with st.spinner("🧠 Scanning..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["Identify this: name, type, facts, origin. If toy tiger explain it is toy.", img]
            )
        st.success("✅ IDENTIFIED!")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
