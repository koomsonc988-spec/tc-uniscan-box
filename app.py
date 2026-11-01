import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time

# --- YOUR PAYSTACK LINK - GHS 50 ---
PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20
OWNER_CODE = "TC2024"

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

# --- SIDEBAR - OWNER ---
with st.sidebar:
    st.title("📦 TC UniScan")
    if st.session_state.is_owner:
        st.success("👑 Owner Mode Active")
        st.caption(f"Until {st.session_state.premium_until}")
        if st.button("🔧 Reset Scans", use_container_width=True):
            st.session_state.scans_today = 0
            st.session_state.box_data = []
            st.rerun()
        if st.button("🚪 Exit Owner", use_container_width=True):
            st.session_state.is_owner = False
            st.session_state.is_premium = False
            st.rerun()
    else:
        st.subheader("👑 Owner Login")
        code = st.text_input("Owner Code", type="password")
        if st.button("🔓 Unlock Owner Mode", use_container_width=True):
            if code == OWNER_CODE:
                st.session_state.is_owner = True
                st.session_state.is_premium = True
                st.session_state.premium_until = date.today() + timedelta(days=365)
                st.session_state.scans_today = 0
                st.balloons()
                st.rerun()
            else:
                st.error("Wrong code!")

# --- PAYWALL WITH RESET ---
def show_paywall():
    st.markdown(f"""
    <div style="background:#0f172a;color:white;padding:25px;border-radius:18px;text-align:center">
    <h2>🚫 Free Limit Reached (20/20)</h2>
    <h3>📦 TC UniScan Premium - GHS 50 / Month</h3>
    <p>Unlimited scans for 30 days<br>Bank / MoMo / VISA</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.link_button("💳 Pay GHS 50 - Unlock 30 Days", PAYSTACK_LINK, use_container_width=True, type="primary")
    st.write("")
    if st.button("✅ I Have Paid GHS 50 - Unlock Now", use_container_width=True, type="primary"):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.session_state.scans_today = 0
        st.balloons()
        st.success(f"Unlocked until {st.session_state.premium_until}")
        time.sleep(1)
        st.rerun()
    st.stop()

if not st.session_state.is_premium and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# --- HEADER - YOUR LOGO HERE ---
# If you have logo.png in repo, uncomment next 3 lines:
# col_logo, col_title = st.columns([1,4])
# with col_logo:
#     st.image("logo.png", width=60)
# with col_title:
#     st.title("TC UniScan Box")

# For now using emoji - change when you upload logo:
st.title("📦 TC UniScan Box")

if st.session_state.is_premium:
    st.caption(f"⭐ Premium until {st.session_state.premium_until}")
else:
    st.caption(f"Free: {DAILY_FREE_LIMIT - st.session_state.scans_today} left today")

# --- SCANNER ---
cam = st.camera_input("📷 Scan Box")
if cam:
    st.session_state.box_data.append({
        "code": f"BOX-{int(time.time())%100000}",
        "time": time.strftime("%H:%M:%S"),
        "date": str(date.today())
    })
    st.session_state.scans_today += 1
    st.success(f"Scanned! {len(st.session_state.box_data)} total")
    st.rerun()

up = st.file_uploader("Or Upload Image", type=["jpg","png","jpeg"])
if up:
    st.image(up, width=250)
    if st.button("🔍 Scan Uploaded"):
        st.session_state.box_data.append({
            "code": f"IMG-{int(time.time())%100000}",
            "time": time.strftime("%H:%M:%S"),
            "date": str(date.today())
        })
        st.session_state.scans_today += 1
        st.rerun()

# --- RESULTS ---
if st.session_state.box_data:
    st.divider()
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "tc_uniscan.csv", use_container_width=True)
    with c2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.box_data = []
            st.rerun()

st.divider()
st.caption("Owner: Tap > and enter TC2024 | Customers: 20 free then GHS 50")
