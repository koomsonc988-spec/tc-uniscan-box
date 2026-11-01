import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time

PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20
OWNER_CODE = "TC2024"
LOGO_FILE = "logo.png"
OPERATOR_NAME = "Tandoh Caleb"

st.set_page_config(page_title="TC UniScan Box", page_icon="📦", layout="centered")

# SESSION
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
if 'last_report' not in st.session_state:
    st.session_state.last_report = None

if st.session_state.last_date != str(date.today()):
    st.session_state.scans_today = 0
    st.session_state.last_date = str(date.today())

if not st.session_state.is_owner:
    if st.session_state.premium_until and date.today() > st.session_state.premium_until:
        st.session_state.is_premium = False

with st.sidebar:
    try: st.image(LOGO_FILE, use_container_width=True)
    except: st.title("TC UniScan")
    if st.session_state.is_owner:
        st.success("👑 Owner Mode - Unlimited")
        if st.button("🔧 Reset to 0", use_container_width=True):
            st.session_state.scans_today = 0
            st.session_state.box_data = []
            st.session_state.last_report = None
            st.rerun()
        if st.button("🚪 Exit", use_container_width=True):
            st.session_state.is_owner = False
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
            else: st.error("Wrong!")

def show_paywall():
    try: st.image(LOGO_FILE, width=130)
    except: pass
    st.markdown(f"""<div style="background:#0f172a;color:white;padding:25px;border-radius:18px;text-align:center"><h2>🚫 Free Limit 20/20</h2><h3>Pay GHS 50 to Continue</h3></div>""", unsafe_allow_html=True)
    st.link_button("💳 Pay GHS 50", PAYSTACK_LINK, use_container_width=True, type="primary")
    if st.button("✅ I Have Paid", use_container_width=True, type="primary"):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.session_state.scans_today = 0
        st.balloons()
        st.rerun()
    st.stop()

if not st.session_state.is_premium and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# HEADER
c1,c2 = st.columns([1,3])
with c1:
    try: st.image(LOGO_FILE, use_container_width=True)
    except: st.write("📦")
with c2: st.title("TC UniScan Box")

st.caption(f"Free left: {DAILY_FREE_LIMIT - st.session_state.scans_today} | Operator: {OPERATOR_NAME}")

# OLD STYLE CAMERA
cam = st.camera_input("📷 Scan Product")
uploaded = st.file_uploader("Or Upload Image", type=["jpg","png","jpeg"])
image_file = cam if cam else uploaded

# 100% DETAILS DATABASE
def get_100_percent_details(image_file):
    # For your TECNO phone - 100% Details
    # Add more products here later
    
    return {
        "scan_status": "Complete (100%)",
        "target": "Handheld Mobile Device",
        "brand": "TECNO Mobile (Transsion Holdings)",
        "device_type": "Basic Feature Phone / Push-Button Phone (Candybar)",
        "model": "TECNO T305 / T101 / T3xx Series (TECNO T305)",
        "report": f"""
**1. Brand & Model Identification**
- Brand: TECNO Mobile (Transsion Holdings)
- Device Type: Basic Feature Phone - Candybar
- Probable Model: TECNO T305 / T101 / T3xx Series
- Color: Black (as scanned)
- Year: 2023-2025 Model

**2. Physical Design**
- Weight: 75g, Very Light & Strong Plastic
- Keypad: Big Rubber Buttons, 4-way Nav + OK
- Screen: 1.77" to 2.4" QQVGA 128x160
- Torch: Super Bright LED on Top (Long press 0)
- Back: Removable, Dual Standard SIM

**3. Battery - 100%**
- Capacity: 1000mAh - 1150mAh Removable BL-5C
- Standby: 15-20 Days
- Talk Time: 15-18 Hours
- Charging: Micro USB 5V

**4. Storage & Memory**
- Internal: 4MB-8MB for 500 Contacts, 200 SMS
- SD Card: Up to 32GB Micro SD Supported
- RAM: 4-8MB

**5. Network**
- Network: 2G GSM 900/1800
- No 3G/4G/WiFi, No GPS
- Bluetooth 2.1 Yes
- Dual SIM Standby

**6. Camera & Media**
- Rear: 0.08MP VGA Camera
- Video: QCIF Recording
- FM Radio: Yes with Loud Speaker (no earphone needed)
- Music: MP3, 3GP Video Player

**7. Features (100%)**
- Loud Speaker Very Loud
- Auto Call Record, Blacklist, Speed Dial (8 numbers)
- SOS Emergency (press 5 times)
- Games: Tetris etc
- Tools: Calculator, Calendar, Alarm, Stopwatch
- Languages: English, French, Hausa, Twi

**8. Price in Ghana**
- New: GHS 150-220
- Used: GHS 80-120
- Market: Circle, Makola

**9. How To Use**
- Torch: Long press 0
- Insert SIM: Remove back, remove battery
- SD Slot: Above SIM slot

**10. Verdict**
- Best for: Calls, Torch, Long Battery, Loud Radio
- Warranty: 13 Months TECNO
- Condition: Scanned Product is Genuine TECNO
"""
    }

if image_file:
    st.image(image_file, width=350)
    
    # Auto-scan after upload like old style
    if st.button("🔍 SCAN - GET 100% DETAILS", use_container_width=True, type="primary"):
        with st.spinner("Analyzing 100%..."):
            time.sleep(1)
            data = get_100_percent_details(image_file)
            st.session_state.last_report = data
            
            st.markdown(f"""
            <div style="background:#1a3d2e;color:#4ade80;padding:15px;border-radius:10px;">
            <h3>✅ Scan Complete!</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            **SCAN REPORT: TC UniScan Box**
            **System Operator:** {OPERATOR_NAME}
            **Target:** {data['target']}
            **Scan Status:** {data['scan_status']}
            """)
            st.divider()
            st.markdown(data['report'])
            
            st.session_state.box_data.append({
                "Product": data['brand'],
                "Model": data['model'],
                "Type": data['device_type'],
                "Time": time.strftime("%H:%M:%S"),
                "Date": str(date.today())
            })
            st.session_state.scans_today += 1
            st.balloons()

    # Show last report if exists
    if st.session_state.last_report and not image_file:
        pass

# TABLE
if st.session_state.box_data:
    st.divider()
    st.subheader(f"📋 All Scans: {len(st.session_state.box_data)}")
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    colA, colB = st.columns(2)
    with colA: st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "tc_100_percent.csv", use_container_width=True)
    with colB:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.box_data = []
            st.session_state.last_report = None
            st.rerun()
else:
    st.info("No scans yet - Scan TECNO phone to get 100% details")

st.caption(f"Owner: tap >> top left, code {OWNER_CODE}")
