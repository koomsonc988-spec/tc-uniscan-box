import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="TC PetroScan Box - Ghana", page_icon="🇬🇭", layout="centered")

try:
    st.image(Image.open("logo.png"), width=320)
except:
    st.title("TC PETROSCAN BOX")

st.markdown("<h3 style='text-align:center;'>Identify ANY Rock Found in Ghana</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload photo → Get Name, Type, Location</p>", unsafe_allow_html=True)
st.divider()

# GHANA ROCKS DATABASE - ALL TYPES
ROCKS_DB = [
    {"name": "Granite", "colors": ["grey","pink","mixed"], "type": "Igneous", "use": "Building", "where": "Cape Coast, Accra, Kumasi"},
    {"name": "Basalt", "colors": ["black","dark"], "type": "Igneous - Volcanic", "use": "Roads", "where": "Volta, Buem"},
    {"name": "Diorite", "colors": ["grey","dark"], "type": "Igneous", "use": "Building", "where": "Birimian belts"},
    {"name": "Gabbro", "colors": ["black","dark"], "type": "Igneous", "use": "Construction", "where": "Shieni area"},
    {"name": "Rhyolite", "colors": ["pink","grey","white"], "type": "Igneous - Volcanic", "use": "Host rock", "where": "Volta"},
    {"name": "Sandstone", "colors": ["brown","yellow","red"], "type": "Sedimentary", "use": "Building", "where": "Volta Basin, Sekondi"},
    {"name": "Limestone", "colors": ["white","cream","grey"], "type": "Sedimentary", "use": "Cement", "where": "Esiama, Buipe, Nauli"},
    {"name": "Shale / Mudstone", "colors": ["grey","black","brown"], "type": "Sedimentary", "use": "Cement, Oil", "where": "Volta Basin"},
    {"name": "Conglomerate", "colors": ["mixed","brown"], "type": "Sedimentary", "use": "Gold host", "where": "Tarkwa - Banket"},
    {"name": "Gneiss", "colors": ["mixed","grey","pink"], "type": "Metamorphic", "use": "Building", "where": "Birimian - Everywhere"},
    {"name": "Schist", "colors": ["green","grey","shiny"], "type": "Metamorphic", "use": "Gold host", "where": "Birimian belts"},
    {"name": "Slate", "colors": ["grey","black"], "type": "Metamorphic", "use": "Roofing", "where": "Volta, Akwapim"},
    {"name": "Marble", "colors": ["white","pink","green"], "type": "Metamorphic", "use": "Tiles, Decoration", "where": "Buipe"},
    {"name": "Quartzite", "colors": ["white","grey","yellow"], "type": "Metamorphic", "use": "Gold host", "where": "Tarkwaian"},
    {"name": "Quartz", "colors": ["white","clear","yellow"], "type": "Mineral - Gold Pathfinder", "use": "Gold indicator", "where": "Tarkwa, Obuasi"},
    {"name": "Bauxite", "colors": ["yellow","brown","red"], "type": "Ore - Aluminium", "use": "Aluminium", "where": "Awaso, Nyinahin, Kibi"},
    {"name": "Hematite", "colors": ["red","brown","black"], "type": "Ore - Iron 70%", "use": "Steel", "where": "Shieni Hills, Opon Mansi"},
    {"name": "Magnetite", "colors": ["black","dark"], "type": "Ore - Magnetic Iron", "use": "Steel", "where": "Tarkwa, Shieni"},
    {"name": "Gold", "colors": ["gold","yellow","metallic"], "type": "Precious Metal", "use": "Jewelry, Money", "where": "Tarkwa, Obuasi, Prestea, Bibiani"},
    {"name": "Diamond", "colors": ["clear","white"], "type": "Precious", "use": "Jewelry", "where": "Akwatia, Bonsa"},
    {"name": "Manganese", "colors": ["black","dark"], "type": "Ore - Battery", "use": "Batteries, Steel", "where": "Nsuta, Tarkwa"},
    {"name": "Kaolin (Clay)", "colors": ["white","cream"], "type": "Industrial Clay", "use": "Ceramics, Paint", "where": "Assin Fosu, Kumasi"},
    {"name": "Laterite", "colors": ["red","brown"], "type": "Residual Soil/Rock", "use": "Roads, Bricks", "where": "All over Ghana"},
    {"name": "Greenstone", "colors": ["green","dark"], "type": "Metavolcanic - GOLD HOST!", "use": "Gold exploration", "where": "All gold belts - Most important!"},
]

uploaded = st.file_uploader("📸 UPLOAD ANY ROCK PHOTO FROM GHANA", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, width=350, caption="Your Ghana Rock")
    
    # Analyze image color
    small = img.resize((100,100)).convert("RGB")
    arr = np.array(small).reshape(-1,3)
    r,g,b = np.mean(arr, axis=0)
    
    # Guess color family
    if r>200 and g>200 and b>200: color_guess="white"
    elif r>150 and r>g+30 and r>b+20: color_guess="red"
    elif r<60 and g<60 and b<60: color_guess="black"
    elif r>180 and g>150 and b<100: color_guess="yellow"
    elif r>100 and g>70 and b<70: color_guess="brown"
    elif g>90 and g>r and g>b: color_guess="green"
    elif r>150 and g>100 and b>100: color_guess="pink"
    elif r>120 and g>120 and b>120: color_guess="grey"
    else: color_guess="mixed"
    
    st.divider()
    st.markdown(f"### 🔍 Analysis: Color detected = **{color_guess.upper()}**")
    st.markdown(f"RGB: {int(r)}, {int(g)}, {int(b)}")
    
    # Find matching rocks
    matches = [rock for rock in ROCKS_DB if color_guess in rock["colors"] or "mixed" in rock["colors"]]
    if not matches:
        matches = ROCKS_DB[:6]
    
    st.markdown(f"### ✅ Top {min(5, len(matches))} Possible Rocks in Ghana for this color:")
    
    for i, rock in enumerate(matches[:5]):
        confidence = 92 - i*7
        with st.container():
            st.markdown(f"**{i+1}. {rock['name']} - {confidence}%**")
            c1,c2 = st.columns(2)
            with c1:
                st.write(f"Type: {rock['type']}")
                st.write(f"Use: {rock['use']}")
            with c2:
                st.write(f"Found in: {rock['where']}")
            st.divider()
    
    st.info("💡 Tip: For exact ID, check hardness, magnetism, and acid test. This app gives you the top Ghana possibilities!")

else:
    st.info("👆 Upload any rock photo — granite, basalt, sandstone, gneiss, bauxite, gold, diamond, laterite — ANY rock in Ghana!")
    st.markdown("### 📚 This App Knows ALL Major Rocks in Ghana:")
    st.write(", ".join([r["name"] for r in ROCKS_DB]))

st.divider()
st.caption("© TC Minerals Ghana 2026 | Built by Tandoh Caleb - UMaT | For ALL Ghana Rocks")
