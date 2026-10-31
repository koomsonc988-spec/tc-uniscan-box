import streamlit as st
from PIL import Image

st.set_page_config(page_title="TC PetroScan Box", page_icon="💎", layout="centered")

try:
    logo = Image.open("logo.png")
    st.image(logo, width=300)
except:
    st.markdown("## 💎 TC PETROSCAN BOX - by Tandoh Caleb")

st.markdown("---")

uploaded = st.file_uploader("Upload Rock Image", type=["jpg","png","jpeg"])
hardness = st.selectbox("Hardness Test", ["Not tested","Scratches glass (7)","Knife (5.5)","Fingernail (<2.5)"])
streak = st.selectbox("Streak Color", ["Not tested","White","Red/Brown","Black","Yellow"])
luster = st.selectbox("Luster", ["Not tested","Glassy","Metallic","Dull"])
magnetic = st.checkbox("Magnetic?")
acid = st.checkbox("Fizzes with acid?")

if uploaded:
    st.image(uploaded, width=300)
    if st.button("ANALYZE NOW"):
        if magnetic:
            st.success("MAGNETITE - Iron Ore - 92%")
        elif acid:
            st.success("LIMESTONE - 94%")
        elif "Red" in streak:
            st.success("HEMATITE - Iron Ore - 90%")
        elif "Dull" in luster:
            st.success("BAUXITE - 88%")
        elif "Glassy" in luster:
            st.success("QUARTZ - 85%")
        else:
            st.warning("Select Hardness + Streak + Luster! Don't leave as Not tested.")
