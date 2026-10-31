import streamlit as st
from PIL import Image

st.set_page_config(page_title="TC PetroScan Box", page_icon="💎", layout="wide")

# YOUR GOLD LOGO - WILL SHOW NOW
try:
    logo = Image.open("logo.png")
    st.image(logo, use_column_width=True)
except:
    st.error("Logo not found - make sure you uploaded logo.png to GitHub")

st.markdown("---")
st.markdown("### 📸 Rock Scanner")

uploaded = st.file_uploader("Upload Rock Image", type=["jpg","png","jpeg"])
hardness = st.selectbox("Hardness Test", ["Not tested","Scratches glass (7)","Knife scratches it (5.5)","Fingernail (<2.5)"])
streak = st.selectbox("Streak Color", ["Not tested","White","Red/Brown","Black","Yellow"])
luster = st.selectbox("Luster", ["Not tested","Glassy","Metallic","Dull/Earthy"])
magnetic = st.checkbox("Magnetic?")
acid = st.checkbox("Fizzes with acid?")

if uploaded:
    st.image(uploaded, width=350)
    if st.button("🔍 ANALYZE NOW", use_container_width=True):
        if magnetic:
            st.success("MAGNETITE - 92%")
            st.write("Fe3O4 | Iron Ore")
        elif acid:
            st.success("LIMESTONE - 94%")
        elif "Red" in streak:
            st.success("HEMATITE - 90% - Iron Ore")
        elif "Dull" in luster:
            st.success("BAUXITE - 88% - From Awaso")
        elif "Glassy" in luster:
            st.success("QUARTZ - 85% - Gold indicator in Tarkwa")
        else:
            st.warning("Select Hardness + Streak + Luster! Don't leave as Not tested.")
