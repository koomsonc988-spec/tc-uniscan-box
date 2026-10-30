import streamlit as st
import os
from PIL import Image
from rock_classifier import classify

st.set_page_config(page_title="TC PETROSCAN BOX", page_icon="💎", layout="centered")

# LOGO ON TOP - CENTER
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", use_container_width=True)
else:
    st.markdown("<h1 style='text-align:center'>💎</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;color:#FFD700;'>TC PETROSCAN BOX</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Geologist AI Brain | Phone Camera Mode</p>", unsafe_allow_html=True)

st.info("📱 This camera works ONLY on your phone browser!")

# PHONE CAMERA ONLY - no upload
camera_photo = st.camera_input("📷 Point at rock and TAKE PHOTO")

if camera_photo:
    st.image(camera_photo, caption="Your Rock", use_column_width=True)
    temp = "temp.jpg"
    with open(temp, "wb") as f:
        f.write(camera_photo.getbuffer())
    with st.spinner("🔬 TC Geologist AI analyzing crystals, layers, quartz..."):
        result = classify(temp)
    st.success(result)
    if "GOLD" in result:
        st.balloons()
    os.remove(temp)
