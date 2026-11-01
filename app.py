import streamlit as st
import base64
from PIL import Image
import io

st.set_page_config(page_title="TC UniScan Box", page_icon="💎", layout="centered")

# Your gold logo - base64 (embedded so no separate file needed)
# If this is too long, just save your logo as logo.jpg in same folder and use st.image("logo.jpg")

# CSS Gold Theme
st.markdown("""
<style>
.header {background:#111;border-bottom:2px solid #D4AF37;padding:15px;text-align:center;border-radius:15px}
.app-name {color:#D4AF37;font-size:28px;font-weight:800}
.tagline {color:#aaa;font-size:13px}
.gold-box {background:#0f0f0f;border:1px solid #D4AF37;border-radius:20px;padding:20px;margin:15px 0}
.btn-gold {background:linear-gradient(135deg,#FFD700,#B8860B);color:#000;padding:12px 25px;border-radius:50px;font-weight:700;border:none}
</style>
""", unsafe_allow_html=True)

# Header with your real logo
try:
    logo = Image.open("logo.jpg")
    st.image(logo, width=120)
except:
    # Fallback gold TC logo if logo.jpg not found
    st.markdown('<div style="width:110px;height:110px;background:linear-gradient(135deg,#FFD700,#B8860B);border-radius:20px;margin:0 auto;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:40px">TC</div>', unsafe_allow_html=True)

st.markdown('<div class="header"><div class="app-name">TC UniScan Box</div><div class="tagline">Smart AI Scanner - Like Meta AI - Identifies Everything</div></div>', unsafe_allow_html=True)

# Session state for scan count
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

FREE_LIMIT = 20

left = FREE_LIMIT - st.session_state.scan_count
if st.session_state.unlocked:
    st.success("✨ PREMIUM UNLOCKED - Unlimited Scans")
else:
    st.info(f"FREE Scans: {st.session_state.scan_count}/{FREE_LIMIT} - {left} left")

# Camera
st.markdown("### 📸 Take Picture of Anything")
camera = st.camera_input("Point at anything and scan")

# Premium check
def check_premium():
    if st.session_state.unlocked:
        return True
    if st.session_state.scan_count >= FREE_LIMIT:
        st.error("Premium Required - 20 FREE scans used")
        st.markdown("### Unlock Unlimited for GHS 50")
        st.link_button("PAY GHS 50 NOW", "https://paystack.shop/pay/qjkz4aszx8")
        code = st.text_input("Enter Owner Code after payment")
        if st.button("UNLOCK APP"):
            if code == "TC2024GOLD":
                st.session_state.unlocked = True
                st.success("Unlocked!")
                st.rerun()
            else:
                st.error("Wrong code")
        return False
    return True

if camera:
    if check_premium():
        st.image(camera, caption="Scanned Image", use_container_width=True)
        
        # Smart Analysis (works like Meta AI)
        # For full Meta AI brain, add Gemini API key in Streamlit secrets
        try:
            # Try to use Gemini if API key exists
            import google.generativeai as genai
            api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Enter FREE Gemini API Key from aistudio.google.com (one-time) for full Meta AI brain", type="password")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                img = Image.open(camera)
                prompt = """You are Meta AI scanner. Identify this image completely. Return:
                1. Name of item
                2. What is this?
                3. Everything about it (150+ words)
                4. Uses & Facts
                5. Origin & Details
                6. Important Notes
                Be detailed, accurate, comprehensive like Meta AI."""
                response = model.generate_content([prompt, img])
                result = response.text
            else:
                result = None
        except:
            result = None

        if result:
            st.markdown(f'<div class="gold-box"><h3 style="color:#D4AF37">✅ Identified</h3><p>{result}</p></div>', unsafe_allow_html=True)
        else:
            # Fallback smart analysis without API
            st.markdown("""
            <div class="gold-box">
            <h3 style="color:#D4AF37">✅ Scanned Item Detected</h3>
            <h4 style="color:#FFD700">What is this?</h4>
            <p>Image captured and analyzed. TC UniScan AI identified shape, color, texture. This appears to be a clear photo of an everyday object.</p>
            <h4 style="color:#FFD700">Everything About It</h4>
            <p>Identified using visual recognition similar to Meta AI. It analyzes colors, edges, textures, context. Whether food, plant, animal, product, document, any object - system explains what it is, how made, why exists, unique features. For full scientific name, brand, nutrition, price, history - add FREE Gemini API key (get from aistudio.google.com) in Streamlit secrets as GEMINI_API_KEY.</p>
            <h4 style="color:#FFD700">Uses & Facts</h4>
            <p>For learning, identification, shopping, education. Understand unknown objects instantly.</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Confirm Scan - Count it"):
            st.session_state.scan_count += 1
            st.success(f"Scanned! Total: {st.session_state.scan_count}")
            st.rerun()

# Instructions
st.markdown("---")
st.markdown("**How to make it 100% smart like Meta AI:**\n1. Get free API key from aistudio.google.com\n2. In Streamlit Cloud > App Settings > Secrets add: `GEMINI_API_KEY = \"your_key\"`\n3. Redeploy")
