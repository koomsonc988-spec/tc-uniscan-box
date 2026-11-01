import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(page_title="TC UniScan Box", layout="centered")

st.markdown("""
<style>
.stApp {background:#000;color:#fff;}
.gold-box {background:#111;border:2px solid #D4AF37;border-radius:20px;padding:20px;margin:10px 0;white-space:pre-wrap}
</style>
""", unsafe_allow_html=True)

try:
    st.image("logo.jpg", width=120)
except:
    st.markdown('<div style="width:110px;height:110px;background:linear-gradient(135deg,#FFD700,#B8860B);border-radius:20px;margin:0 auto;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:35px">TC</div>', unsafe_allow_html=True)

st.markdown('<h2 style="color:#D4AF37;text-align:center">TC UniScan Box</h2><p style="text-align:center;color:#aaa">Smart Scanner Like Meta AI</p>', unsafe_allow_html=True)

if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# API key from Secrets (AQ. key works now!)
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("Add GEMINI_API_KEY in Secrets (Manage app > Secrets)")
    st.stop()
else:
    st.success(f"✅ AI Connected - Key type: {api_key[:3]}... (AQ. keys work now!)")

if st.session_state.unlocked:
    st.success("PREMIUM UNLOCKED")
else:
    st.info(f"FREE: {st.session_state.scan_count}/20")

camera = st.camera_input("📸 Take picture of ANYTHING")

if camera:
    img = Image.open(camera)
    st.image(img, use_container_width=True)
    
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
            with st.spinner("🧠 Meta AI is thinking with your AQ. key..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = """You are Meta AI scanner. Identify this image 100% accurately. 
                    Give:
                    1. NAME: exact name
                    2. WHAT IS THIS: 2-3 sentences
                    3. EVERYTHING ABOUT IT: 150+ words detailed with scientific name, facts, history
                    4. USES & FACTS
                    5. ORIGIN & PRICE if product
                    Be accurate like Meta AI."""
                    
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt, img]
                    )
                    st.markdown(f'<div class="gold-box">{response.text}</div>', unsafe_allow_html=True)
                    st.session_state.scan_count += 1
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("If error continues, try deleting key and creating new one at aistudio.google.com/app/apikey")

st.caption("TC UniScan Box | GHS 50 Premium")
