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
    st.image(img, width=500)
    try:
        client = genai.Client(api_key=API_KEY)
        with st.spinner("🧠 Scanning..."):
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=["Identify this: If rock give name, type, composition, origin, value. If anything else (animal, plant, food, car, person, object) identify fully with details, facts, origin. Be expert professor.", img]
            )
        st.success("✅ IDENTIFIED!")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If error says 'not found', wait 5 mins - new API keys need time to activate. Or create new key at aistudio.google.com/app/apikey")
elif uploaded:
    st.warning("Paste API key first - get free at aistudio.google.com/app/apikey")
