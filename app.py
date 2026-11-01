import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="TC UniScan Box", layout="centered")

# GOLD THEME
st.markdown("""
<style>
.stApp {background:#000;color:#fff;}
.gold-box {background:#111;border:2px solid #D4AF37;border-radius:20px;padding:20px;margin:10px 0;white-space:pre-wrap}
.header {text-align:center}
</style>
""", unsafe_allow_html=True)

# YOUR REAL GOLD LOGO
try:
    st.image("logo.jpg", width=120)
except:
    st.markdown('<div style="width:110px;height:110px;background:linear-gradient(135deg,#FFD700,#B8860B);border-radius:20px;margin:0 auto;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:35px">TC</div>', unsafe_allow_html=True)

st.markdown('<h2 style="color:#D4AF37;text-align:center">TC UniScan Box</h2><p style="text-align:center;color:#aaa">Smart Scanner Like Meta AI</p>', unsafe_allow_html=True)

if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# API KEY INSIDE APP - PASTE HERE
st.markdown("### 🔑 Step 1: Paste Your FREE AI Key (one time)")
st.write("Get FREE key from: https://aistudio.google.com/app/apikey")
api_key_input = st.text_input("Paste your Gemini API Key here", type="password", placeholder="AIza...")

if api_key_input:
    st.session_state.api_key = api_key_input

api_key = st.session_state.get('api_key', '') or st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("👆 Paste your API key above to make it smart like Meta AI")
    st.stop()
else:
    st.success("✅ AI Key connected - Now super smart like Meta AI!")

if st.session_state.unlocked:
    st.success("PREMIUM UNLOCKED")
else:
    st.info(f"FREE: {st.session_state.scan_count}/20")

camera = st.camera_input("📸 Step 2: Take picture of ANYTHING")

if camera:
    img = Image.open(camera)
    st.image(img, caption="Your image", use_container_width=True)
    
    if st.button("🔍 SCAN NOW - IDENTIFY LIKE META AI", type="primary"):
        if st.session_state.scan_count >= 20 and not st.session_state.unlocked:
            st.error("20 FREE used! Pay GHS 50")
            st.link_button("PAY GHS 50 NOW", "https://paystack.shop/pay/qjkz4aszx8")
            code = st.text_input("Enter Code")
            if st.button("UNLOCK"):
                if code == "TC2024GOLD":
                    st.session_state.unlocked = True
                    st.rerun()
        else:
            with st.spinner("🧠 Meta AI is thinking... Identifying your image..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = """You are Meta AI scanner. Identify this image 100% accurately. 
                    Give:
                    1. NAME: exact name
                    2. WHAT IS THIS: 2-3 sentences
                    3. EVERYTHING ABOUT IT: 150+ words detailed with scientific name, facts, history
                    4. USES & FACTS
                    5. ORIGIN & PRICE if product
                    Be accurate like Meta AI. No generic text."""
                    response = model.generate_content([prompt, img])
                    st.markdown(f'<div class="gold-box">{response.text}</div>', unsafe_allow_html=True)
                    st.session_state.scan_count += 1
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Check your API key - make sure you copied correctly from aistudio.google.com")

st.caption("TC UniScan Box | GHS 50 Premium")
