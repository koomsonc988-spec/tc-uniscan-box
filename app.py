import streamlit as st
from PIL import Image
import os
from rock_classifier import classify

st.set_page_config(page_title="TC PETROSCAN BOX", page_icon="💎", layout="centered")

st.markdown("<h1 style='text-align:center;color:gold;'>💎 TC PETROSCAN BOX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>📱 Phone Camera Mode | Geologist AI Brain</p>", unsafe_allow_html=True)

st.info("👉 This camera works ONLY on your phone browser!")

# PHONE CAMERA ONLY - no upload
camera_photo = st.camera_input("📷 Point at rock and TAKE PHOTO")

if camera_photo:
    st.image(camera_photo, caption="Your Rock", use_column_width=True)
    
    # Save temp
    temp = "temp_phone.jpg"
    with open(temp, "wb") as f:
        f.write(camera_photo.getbuffer())
    
    with st.spinner("🔬 Geologist Brain Analyzing crystals, layers..."):
        result = classify(temp)
    
    st.success(result)
    
    # Gold celebration
    if "GOLD" in result:
        st.balloons()
        st.warning("💰 GOLD DETECTED!")
    
    os.remove(temp)

st.markdown("---")
st.caption("Tip: Take close-up photo in daylight for best accuracy")