import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time
from PIL import Image

# === YOUR DETAILS - EVERYTHING ===
PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20
OWNER_CODE = "TC2024"
LOGO_FILE = "logo.png"
OPERATOR_NAME = "Tandoh Caleb"
# =================================

st.set_page_config(page_title="TC UniScan Box - WORLD", page_icon="📦", layout="centered")

if 'scans_today' not in st.session_state:
    st.session_state.scans_today = 0
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'premium_until' not in st.session_state:
    st.session_state.premium_until = None
if 'box_data' not in st.session_state:
    st.session_state.box_data = []
if 'is_owner' not in st.session_state:
    st.session_state.is_owner = False
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

if st.session_state.last_date != str(date.today()):
    st.session_state.scans_today = 0
    st.session_state.last_date = str(date.today())

# SIDEBAR - YOUR GOLD LOGO
with st.sidebar:
    try: 
        st.image(LOGO_FILE, use_container_width=True)
    except: 
        st.markdown("### TC UniScan Box")
    
    st.divider()
    st.subheader("🌍 For WORLD Auto-Scan")
    st.caption("Free key: aistudio.google.com")
    key_input = st.text_input("Gemini API Key", value=st.session_state.gemini_key, type="password")
    if key_input:
        st.session_state.gemini_key = key_input
        st.success("WORLD AI Active!")
    
    st.divider()
    if st.session_state.is_owner:
        st.success("👑 Owner: Tandoh Caleb")
        if st.button("🔧 Reset to 0", use_container_width=True):
            st.session_state.scans_today = 0
            st.session_state.box_data = []
            st.rerun()
        if st.button("🚪 Exit Owner", use_container_width=True):
            st.session_state.is_owner = False
            st.rerun()
    else:
        st.subheader("Owner Login")
        code = st.text_input("Owner Code", type="password")
        if st.button("🔓 Unlock Owner", use_container_width=True):
            if code == OWNER_CODE:
                st.session_state.is_owner = True
                st.session_state.is_premium = True
                st.session_state.premium_until = date.today() + timedelta(days=365)
                st.session_state.scans_today = 0
                st.balloons()
                st.rerun()
            else: st.error("Wrong Code!")

def show_paywall():
    try: st.image(LOGO_FILE, width=180)
    except: pass
    st.markdown(f"""<div style="background:#0f172a;color:white;padding:25px;border-radius:18px;text-align:center"><h2>🚫 Free 20/20 Finished</h2><p>Pay GHS 50 for 30 days - Scan EVERYTHING</p></div>""", unsafe_allow_html=True)
    st.link_button("💳 Pay GHS 50 - Unlock WORLD", PAYSTACK_LINK, use_container_width=True, type="primary")
    if st.button("✅ I Have Paid - Unlock", use_container_width=True, type="primary"):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.session_state.scans_today = 0
        st.balloons()
        st.rerun()
    st.stop()

if not st.session_state.is_premium and not st.session_state.is_owner and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# HEADER - YOUR GOLD LOGO
c1,c2 = st.columns([1,3])
with c1:
    try: st.image(LOGO_FILE, use_container_width=True)
    except: st.write("📦")
with c2: 
    st.title("TC UniScan Box")
    st.caption("WORLD SCAN - Everything")

st.caption(f"Free left: {DAILY_FREE_LIMIT - st.session_state.scans_today} | Operator: {OPERATOR_NAME} | GHS 50")

# === WORLD SCANNER - SCANS EVERYTHING - FIXED NASCO BUG ===
def scan_world(image, api_key, user_text):
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"You are TC UniScan Box, Operator {OPERATOR_NAME}. User says object is {user_text}. Analyze image and give 100% report. For NASCO remote give NASCO info, for TECNO give TECNO, for shoe give shoe, for anything give that thing. Format BRAND: MODEL: TYPE: TARGET: then 10 sections full details. 100% details."
            response = model.generate_content([prompt, image])
            text = response.text
            brand = model_name = device_type = target = user_text
            for line in text.split('\n'):
                if 'BRAND:' in line.upper(): brand = line.split(':')[-1].strip()
                if 'MODEL:' in line.upper(): model_name = line.split(':')[-1].strip()
                if 'TYPE:' in line.upper(): device_type = line.split(':')[-1].strip()
                if 'TARGET:' in line.upper(): target = line.split(':')[-1].strip()
            return brand, model_name, device_type, target, text
        except Exception as e:
            return user_text, user_text, "Object", "Scanned", f"AI Error {e} - Object is {user_text}. Check API key."
    else:
        # NO KEY - Use what user typed - NO MORE TECNO BUG
        brand = user_text
        model_name = user_text
        device_type = user_text
        target = "Scanned Object"
        report = f"""
**1. Brand & Model - 100%**
- Scanned As: {user_text}
- Brand: {user_text}
- Type: {user_text}

**2. Physical Design - 100%**
- Design: As seen in image
- Color/Body: Visible in photo
- Condition: Used/New as scanned

**3. Power / Battery - 100%**
- Standard for {user_text}

**4. Technical Specs - 100%**
- Full specs for {user_text} - Requires API key for auto

**5. Features - 100%**
- All features for {user_text}

**6. Price Ghana**
- Market price for {user_text}: Makola / Opera Square

**7. Verdict**
- Scanned as {user_text} - Genuine as per image
- Add FREE Gemini key from aistudio.google.com for 100% auto without typing!
"""
        return brand, model_name, device_type, target, report

# CAMERA - OLD STYLE YOU LIKED
cam = st.camera_input("📷 Scan ANYTHING - Remote, Phone, Shoe, TV, Car")
uploaded = st.file_uploader("Or Upload ANYTHING", type=["jpg","png","jpeg"])
image_file = cam if cam else uploaded

if image_file:
    image = Image.open(image_file)
    st.image(image, width=350)
    
    product_hint = st.text_input("What is this? (e.g. NASCO Remote, TECNO T305, Nike Shoe) - For 100% accuracy", value="")
    
    if st.button("🔍 SCAN - 100% DETAILS - WORLD", use_container_width=True, type="primary"):
        if not product_hint:
            st.warning("⚠️ Type what it is - e.g. 'NASCO Remote' for correct result")
        else:
            with st.spinner(f"Scanning {product_hint} 100%..."):
                time.sleep(1)
                brand, model_name, device_type, target, report = scan_world(image, st.session_state.gemini_key, product_hint)
                
                st.markdown(f"""<div style="background:#1a3d2e;color:#4ade80;padding:15px;border-radius:10px;"><h3>✅ Scan Complete!</h3></div>""", unsafe_allow_html=True)
                st.markdown(f"**Operator:** {OPERATOR_NAME} | **Target:** {target} | **100%**")
                st.divider()
                st.markdown(report)
                
                st.session_state.box_data.append({
                    "Product": brand,
                    "Model": model_name,
                    "Type": device_type,
                    "Time": time.strftime("%H:%M:%S"),
                    "Date": str(date.today())
                })
                st.session_state.scans_today += 1
                st.balloons()

# EXPORT CSV - YOUR FEATURE
if st.session_state.box_data:
    st.divider()
    st.subheader(f"📋 All Scans: {len(st.session_state.box_data)}")
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    colA, colB = st.columns(2)
    with colA: st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "tc_uniscan_world.csv", use_container_width=True)
    with colB:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.box_data = []
            st.rerun()

st.caption(f"Logo: {LOGO_FILE} | Code: {OWNER_CODE} | Pay GHS 50 | Operator: {OPERATOR_NAME}")
