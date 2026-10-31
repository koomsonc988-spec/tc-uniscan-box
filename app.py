import streamlit as st
from PIL import Image

st.set_page_config(page_title="TC PetroScan Box", page_icon="💎")

st.markdown("## 💎 TC PETROSCAN BOX")
st.markdown("by Tandoh Caleb - UMaT")
st.markdown("---")

uploaded = st.file_uploader("Upload Rock Image", type=["jpg","png","jpeg"])
hardness = st.selectbox("Hardness Test", ["Not tested","Scratches glass (7)","Knife scratches it (5.5)","Fingernail (<2.5)"])
streak = st.selectbox("Streak Color", ["Not tested","White","Red/Brown","Black"])
luster = st.selectbox("Luster", ["Not tested","Glassy","Metallic","Dull"])
magnetic = st.checkbox("Magnetic?")
acid = st.checkbox("Fizzes with acid?")

if uploaded:
    st.image(uploaded, width=300)
    if st.button("ANALYZE NOW"):
        if magnetic:
            st.success("Rock: MAGNETITE - Iron Ore - 92%")
        elif acid:
            st.success("Rock: LIMESTONE - 94%")
        elif "Red" in streak:
            st.success("Rock: HEMATITE - Iron Ore - 90%")
        elif "Glassy" in luster and "glass" in hardness:
            st.success("Rock: QUARTZ - 85%")
        else:
            st.warning("Please select Hardness + Streak + Luster to get correct answer. Photo alone is not enough.")
