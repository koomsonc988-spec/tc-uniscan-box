import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TC Universe Scan", page_icon="🌍")
st.title("🌍 TC-Universe-Scan-Box")
st.caption("Take a picture of ANYTHING")

API_KEY = st.text_input("Paste FREE Gemini API Key", type="password")
uploaded = st.file_uploader("📸 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    img.thumbnail((512, 512))
    st.image(img, width=500)
    try:
        client = genai.Client(api_key=API_KEY)
        with st.spinner("🧠 Scanning... 2 sec"):
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=["Identify this fast: name, type, facts in short bullet points.", img]
            )
        st.success("✅ IDENTIFIED!")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
elif uploaded:
    st.warning("Paste API key first")
