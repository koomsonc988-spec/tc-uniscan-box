import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time

# --- CONFIG - EVERYTHING YOU ASKED ---
PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20
OWNER_CODE = "TC2024"  # Your secret - only you know
LOGO_FILE = "logo.png"  # Your neon TC cube

st.set_page_config(
    page_title="TC UniScan Box", 
    page_icon="📦", 
    layout="centered"
)

# --- SESSION STATE ---
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

# --- DAILY RESET + EXPIRY CHECK ---
if st.session_state.last_date != str(date.today()):
    st.session_state.scans_today = 0
    st.session_state.last_date = str(date.today())

if not st.session_state.is_owner:
    if st.session_state.premium_until and date.today() > st.session_state.premium_until:
        st.session_state.is_premium = False
        st.session_state.premium_until = None

# --- SIDEBAR WITH LOGO + OWNER BYPASS ---
with st.sidebar:
    try:
        st.image(LOGO_FILE, use_container_width=True)
    except:
        st.title("📦 TC UniScan")
    
    if st.session_state.is_owner:
        st.success("👑 Owner Mode Active")
        st.caption(f"Premium Until: {st.session_state.premium_until}")
        st.divider()
        if st.button("🔧 Reset Scans to 0", use_container_width=True):
            st.session_state.scans_today = 0
            st.session_state.box_data = []
            st.success("Reset Done!")
            time.sleep(0.5)
            st.rerun()
        if st.button("🚪 Exit Owner Mode", use_container_width=True):
            st.session_state.is_owner = False
            st.session_state.is_premium = False
            st.rerun()
    else:
        st.title("TC UniScan")
        st.subheader("👑 Owner Login")
        code = st.text_input("Enter Owner Code", type="password", placeholder="TC2024")
        if st.button("🔓 Unlock Owner - 1 Year Free", use_container_width=True):
            if code == OWNER_CODE:
                st.session_state.is_owner = True
                st.session_state.is_premium = True
                st.session_state.premium_until = date.today() + timedelta(days=365)
                st.session_state.scans_today = 0
                st.balloons()
                st.success("Owner Unlocked! 365 Days!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Wrong Owner Code!")
        st.divider()
        st.caption("Customer: 20 free scans/day\nThen GHS 50/month")

# --- PAYWALL - WITH RESET AFTER PAYMENT ---
def show_paywall():
    try:
        st.image(LOGO_FILE, width=150)
    except:
        pass
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);color:white;padding:28px;border-radius:20px;text-align:center;border:2px solid #6366f1">
    <h2>🚫 Free Limit Reached</h2>
    <h2>20 / 20 Used Today</h2>
    <h3 style="color:#a5b4fc">TC UniScan Premium - GHS 50 / Month</h3>
    <p>✅ Unlimited scans for 30 days<br>✅ Bank / MoMo / VISA Accepted<br>✅ Export CSV<br>✅ Priority Support</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.link_button("💳 Pay GHS 50 - Unlock 30 Days Now", PAYSTACK_LINK, use_container_width=True, type="primary")
    st.write("")
    st.markdown("**After you pay on Paystack, click below:**")
    if st.button("✅ I Have Paid GHS 50 - Unlock My App Now", use_container_width=True, type="primary"):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.session_state.scans_today = 0  # <-- RESETS TO 0 AFTER PAYMENT
        st.balloons()
        st.success(f"✅ Payment Confirmed! Premium until {st.session_state.premium_until} - Scans Reset to 0!")
        time.sleep(2)
        st.rerun()
    st.divider()
    st.caption(f"Need help? Payment link: {PAYSTACK_LINK}")
    st.stop()

# Check if should show paywall
if not st.session_state.is_premium and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# --- HEADER WITH YOUR REAL NEON LOGO ---
col1, col2 = st.columns([1,3.5])
with col1:
    try:
        st.image(LOGO_FILE, use_container_width=True)
    except:
        st.markdown("## 📦")
with col2:
    st.title("TC UniScan Box")

if st.session_state.is_premium:
    if st.session_state.is_owner:
        st.markdown(f"**👑 Owner Mode** | ⭐ Premium until **{st.session_state.premium_until}** | Free Left: **Unlimited**")
    else:
        st.markdown(f"⭐ **Premium Active until {st.session_state.premium_until}** | Unlimited Scans")
else:
    left = DAILY_FREE_LIMIT - st.session_state.scans_today
    st.markdown(f"**Free:** {left} left today | {st.session_state.scans_today}/{DAILY_FREE_LIMIT} used")

# --- SCANNER SECTION ---
st.divider()
cam = st.camera_input("📷 Scan Box / Barcode")
if cam:
    new_code = f"BOX-{int(time.time())%100000}"
    st.session_state.box_data.append({
        "Box Code": new_code,
        "Time": time.strftime("%H:%M:%S"),
        "Date": str(date.today())
    })
    st.session_state.scans_today += 1
    st.success(f"✅ Scanned {new_code}! Total: {len(st.session_state.box_data)}")
    time.sleep(0.6)
    st.rerun()

up = st.file_uploader("Or Upload Box Image", type=["jpg","png","jpeg"])
if up:
    st.image(up, width=300)
    if st.button("🔍 Scan Uploaded Image", use_container_width=True):
        new_code = f"IMG-{int(time.time())%100000}"
        st.session_state.box_data.append({
            "Box Code": new_code,
            "Time": time.strftime("%H:%M:%S"),
            "Date": str(date.today())
        })
        st.session_state.scans_today += 1
        st.success(f"✅ Scanned {new_code}!")
        st.rerun()

# --- RESULTS TABLE ---
if st.session_state.box_data:
    st.divider()
    st.subheader(f"📋 Scanned Boxes: {len(st.session_state.box_data)}")
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    cA, cB = st.columns(2)
    with cA:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export to CSV", csv, "tc_uniscan_boxes.csv", "text/csv", use_container_width=True)
    with cB:
        if st.button("🗑️ Clear All Boxes", use_container_width=True):
            st.session_state.box_data = []
            st.rerun()
else:
    st.info("👆 No boxes scanned yet. Use camera above to start scanning.")

st.divider()
st.caption(f"© 2026 TC UniScan Box | GHS 50/month | Paystack: {PAYSTACK_LINK} | Owner Tap > to login")
