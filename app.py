import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="TC Universe Scan", page_icon="🌍")
st.title("🌍 TC-Universe-Scan-Box")
st.caption("Take a picture of ANYTHING")

API_KEY = st.text_input("Paste FREE Gemini API Key", type="password")
uploaded = st.file_uploader("📸 Upload ANYTHING", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    img = Image.open(uploaded)
    st.image(img, width=500)
    
    try:
        genai.configure(api_key=API_KEY)
        
        # Show what models are available - to debug
        st.write("Checking models...")
        
        # Try every possible name - one MUST work
        possible_models = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-latest",
            "models/gemini-1.5-flash",
            "gemini-pro",
            "gemini-2.0-flash"
        ]
        
        found = False
        for m_name in possible_models:
            try:
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(["Identify this image in detail: what is it, type, origin, use, facts. If rock: name, composition. Be expert.", img])
                st.success(f"✅ IDENTIFIED with {m_name}!")
                st.markdown(response.text)
                found = True
                break
            except Exception as e:
                st.write(f"❌ {m_name} failed: {e}")
                continue
        
        if not found:
            st.error("All models failed. Your API key is new - wait 5 minutes and try again. Or create new key at aistudio.google.com/app/apikey")
            
    except Exception as e:
        st.error(f"Full error: {e}")
else:
    if uploaded:
        st.warning("Paste API key first")
