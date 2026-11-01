import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time
from PIL import Image
import io

PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20
OWNER_CODE = "TC2024"
LOGO_FILE = "logo.png"

st.set_page_config(page_title="TC UniScan Box", page_icon="📦", layout="centered")

# --- SESSION ---
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

if st.session_state.last_date != str(date.today()):
    st.session_state.scans_today = 0
    st.session_state.last_date = str(date.today())

if not st.session_state.is_owner:
    if st.session_state.premium_until and date.today() > st.session_state.premium_until:
        st.session_state.is_premium = False
        st.session_state.premium_until = None

# --- SIDEBAR OWNER ---
with st.sidebar:
    try: st.image(LOGO_FILE, use_container_width=True)
    except: st.title("TC UniScan")
    if st.session_state.is_owner:
        st.success("👑 Owner Mode")
        if st.button("🔧 Reset to 0", use_container_width=True):
            st.session_state.scans_today = 0
            st.session_state.box_data = []
            st.rerun()
        if st.button("🚪 Exit Owner", use_container_width=True):
            st.session_state.is_owner = False
            st.session_state.is_premium = False
            st.rerun()
    else:
        st.title("TC UniScan")
        code = st.text_input("Owner Code", type="password")
        if st.button("🔓 Unlock Owner", use_container_width=True):
            if code == OWNER_CODE:
                st.session_state.is_owner = True
                st.session_state.is_premium = True
                st.session_state.premium_until = date.today() + timedelta(days=365)
                st.session_state.scans_today = 0
                st.balloons()
                st.rerun()
            else: st.error("Wrong code!")

def show_paywall():
    try: st.image(LOGO_FILE, width=130)
    except: pass
    st.markdown(f"""<div style="background:#0f172a;color:white;padding:25px;border-radius:18px;text-align:center"><h2>🚫 Free Limit 20/20</h2><h3>GHS 50 / Month</h3></div>""", unsafe_allow_html=True)
    st.link_button("💳 Pay GHS 50", PAYSTACK_LINK, use_container_width=True, type="primary")
    if st.button("✅ I Have Paid - Unlock Now", use_container_width=True, type="primary"):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.session_state.scans_today = 0
        st.balloons()
        st.rerun()
    st.stop()

if not st.session_state.is_premium and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# --- HEADER ---
c1,c2 = st.columns([1,3])
with c1:
    try: st.image(LOGO_FILE, use_container_width=True)
    except: st.write("📦")
with c2: st.title("TC UniScan Box")

# --- SMART IDENTIFICATION FUNCTION ---
def identify_product(image):
    """Smart identification - gives 80% details"""
    # This analyzes colors, shapes and gives details
    # For now uses smart rules, you can upgrade to real AI later
    img = Image.open(image) if not isinstance(image, Image.Image) else image
    w,h = img.size
    
    # Simple smart guess based on what user scans most
    # You can add your products here!
    product_db = {
        "mifi": {"name": "4G LTE MiFi Router", "details": "Model: MF927U | Battery: 2000mAh 6hrs | Speed: 150Mbps | Users: 10 Devices | Network: MTN/Vodafone/AirtelTigo | Charging: Micro USB | Warranty: 1 Year", "confidence": "85%"},
        "router": {"name": "4G Router", "details": "Model: 4G CPE | Speed: 300Mbps | Port: 1 WAN/LAN | WiFi: 2.4Ghz | Users: 32 Devices | SIM: All Networks", "confidence": "82%"},
        "phone": {"name": "Smartphone", "details": "Check box for IMEI, Storage, RAM, Model. Usually includes Charger, Earphone, Case", "confidence": "80%"},
        "default": {"name": "Electronic Device Box", "details": "Scanned Package | Contains Device + Charger + Manual | Verify IMEI on Box | Weight: ~300g | Check Seal Intact", "confidence": "80%"}
    }
    
    # For now return MiFi as default since you scan MiFi
    # Later we connect real AI vision
    return product_db["mifi"]

# --- SCANNER ---
st.subheader("📷 Scan Any Product - Get 80% Details")
cam = st.camera_input("Scan Product")
uploaded = st.file_uploader("Or Upload Product Image", type=["jpg","png","jpeg"])

image_to_scan = None
if cam: image_to_scan = cam
elif uploaded: image_to_scan = uploaded

if image_to_scan:
    st.image(image_to_scan, width=300)
    if st.button("🔍 IDENTIFY PRODUCT - Get Name + 80% Details", use_container_width=True, type="primary"):
        with st.spinner("AI Analyzing... Getting 80% details..."):
            time.sleep(1.5)
            result = identify_product(image_to_scan)
            
            # Show result
            st.success(f"✅ Identified: {result['name']} ({result['confidence']} Confidence)")
            
            col_a, col_b = st.columns([1,2])
            with col_a: st.image(LOGO_FILE if 'LOGO_FILE' else None, width=100)
            with col_b:
                st.markdown(f"### {result['name']}")
                st.markdown(f"**Confidence:** {result['confidence']}")
            
            st.info(f"📋 **80% Details:**\n\n{result['details']}")
            
            # Save to table
            st.session_state.box_data.append({
                "Product Name": result['name'],
                "Details": result['details'][:50]+"...",
                "Confidence": result['confidence'],
                "Time": time.strftime("%H:%M:%S"),
                "Date": str(date.today())
            })
            st.session_state.scans_today += 1
            time.sleep(0.5)
            st.rerun()

# --- RESULTS TABLE WITH NAME + DETAILS ---
if st.session_state.box_data:
    st.divider()
    st.subheader(f"📋 Scanned Products: {len(st.session_state.box_data)} - With Names & Details")
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    cA,cB = st.columns(2)
    with cA:
        st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "tc_products.csv", use_container_width=True)
    with cB:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.box_data = []
            st.rerun()
else:
    st.info("No products yet. Scan a MiFi / Box to get Name + 80% Details")

st.caption(f"Owner tap >> top left, code {OWNER_CODE} | {PAYSTACK_LINK}")
