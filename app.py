import streamlit as st
from datetime import date, timedelta
import pandas as pd
import time

PAYSTACK_LINK = "https://paystack.shop/pay/qjkz4aszx8"
DAILY_FREE_LIMIT = 20

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
if 'box_data' not in st.session_state:  # FIXED - was 'items'
    st.session_state.box_data = []

# Daily reset
if st.session_state.last_date != str(date.today()):
    st.session_state.scans_today = 0
    st.session_state.last_date = str(date.today())
if st.session_state.premium_until and date.today() > st.session_state.premium_until:
    st.session_state.is_premium = False

def show_paywall():
    st.markdown(f"""
    <div style="background:#0f172a;color:white;padding:25px;border-radius:18px;text-align:center">
    <h2>🚫 Free Limit Reached (20/20)</h2>
    <h3>📦 TC UniScan Premium - GHS 50 / Month</h3>
    <p>Unlimited scans for 30 days<br>Bank / MoMo / VISA Accepted</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.link_button("💳 Pay GHS 50 - Unlock 30 Days", PAYSTACK_LINK, use_container_width=True, type="primary")
    if st.button("✅ I Have Paid GHS 50 - Unlock Now", use_container_width=True):
        st.session_state.is_premium = True
        st.session_state.premium_until = date.today() + timedelta(days=30)
        st.balloons()
        st.rerun()
    st.stop()

if not st.session_state.is_premium and st.session_state.scans_today >= DAILY_FREE_LIMIT:
    show_paywall()

# --- APP ---
c1, c2 = st.columns([3,1])
with c1:
    st.title("📦 TC UniScan Box")
with c2:
    if st.session_state.is_premium:
        st.success(f"Premium until {st.session_state.premium_until}")
    else:
        st.metric("Free left", f"{DAILY_FREE_LIMIT - st.session_state.scans_today}")

cam = st.camera_input("📷 Scan Box")
if cam:
    # FIXED LINE
    st.session_state.box_data.append({"code": f"BOX-{int(time.time())%100000}", "time": time.strftime("%H:%M")})
    st.session_state.scans_today += 1
    st.success("Scanned!")
    st.rerun()

if st.session_state.box_data:
    df = pd.DataFrame(st.session_state.box_data)
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "tc_uniscan.csv", use_container_width=True)
    if st.button("🗑️ Clear All"):
        st.session_state.box_data = []
        st.rerun()
