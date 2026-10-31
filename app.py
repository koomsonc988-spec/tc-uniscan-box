import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title=","TC UniScan Box," page_icon="TC,")
st.image("logo.png", width=200)
st.markdown("<h1 style='text-align:center;'>TC UniScan Box</h1><h3 style='text-align:center; color:#FFD700;'>AI Universe Scanner by Tandoh Caleb</h3><p style='text-align:center;'>Powered by TC AI Ghana</p><hr>", unsafe_allow_html=True)

API_KEY = st.text_input("Paste FREE Gemini API Key", type="password")
uploaded = st.file_uploader("📸 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    img.thumbnail((512, 512))
    st.image(img)
    client = genai.Client(api_key=API_KEY)
    with st.spinner("🌌 Scanning Universe..."):
        response = client.models.generate_content(model="gemini-3.8-flash", contents=["Identify this: name, type, origin, facts.", img])
    st.success("✅ TC UniScan Complete!")
    st.markdown(response.text)
