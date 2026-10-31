import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="TC Universe Scan - Identify ANYTHING", page_icon="🌍")

st.title("🌍 TC-Universe-Scan-Box")
st.caption("Take a picture of ANYTHING and it will tell you what it is - Like you wanted!")

API_KEY = st.text_input("Paste FREE Gemini API Key", type="password", help="Get free at aistudio.google.com/app/apikey")
uploaded = st.file_uploader("📸 Take/Upload picture of ANYTHING - Rock, Animal, Plant, Food, Car, Anything!", type=["jpg","png","jpeg"])

if uploaded and API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    img = Image.open(uploaded)
    st.image(img, width=500)

    UNIVERSAL_PROMPT = """
    You are the WORLD'S MOST VIGILANT AI - Expert in EVERYTHING. You can identify ANYTHING in the world from a single photo.

    TASK: Identify what is in this image. Be smart, accurate, vigilant.

    VIGILANT CHECKS:
    1. If blurry/dark/too far: Say "Photo not clear, take closer in daylight"
    2. If multiple things: Identify main subject first, then list others
    3. Never guess. If unsure, say confidence level.

    IF IT IS A ROCK: Give rock name, type, composition, Ghana location, use (as before)
    IF IT IS AN ANIMAL: Give species, breed, age estimate, characteristics, care
    IF IT IS A PLANT: Give common name, scientific name, family, uses, where it grows in Ghana/world
    IF IT IS FOOD: Give dish name, ingredients, origin, nutrition
    IF IT IS A CAR/PHONE/OBJECT: Give brand, model, year, specs, price range in Ghana Cedis
    IF IT IS A PERSON'S SKIN/DISEASE (be careful): Say "See doctor, this looks like... but need medical check"
    IF IT IS ANYTHING ELSE: Identify it fully.

    FORMAT ALWAYS:
    ✅ **WHAT IT IS:** (One line clear name)
    🔍 **DETAILS:** Full description - what you see, color, size, features
    🌍 **ORIGIN / WHERE FOUND:** Where in world/Ghana
    💡 **INTERESTING FACTS / USE:** 3 useful facts
    💰 **VALUE / IMPORTANCE:** Economic value, use, importance
    ⚠️ **VIGILANT NOTE:** How sure you are (90%, 95%) and what to check to confirm

    Be like a genius professor who knows everything. Give ONE best answer, not 3 guesses. Talk simple, friendly, like Meta AI.
    """

    with st.spinner("🧠 TC-Universe AI is scanning... Identifying ANYTHING like you asked!"):
        response = model.generate_content([UNIVERSAL_PROMPT, img])
        st.success("✅ IDENTIFIED!")
        st.markdown(response.text)

        st.divider()
        st.info("💡 Tip: For best accuracy, take photo in daylight, close-up, no shadow.")

elif uploaded and not API_KEY:
    st.error("Paste your free Gemini API Key to activate - Get it in 10 seconds at aistudio.google.com/app/apikey")
else:
    st.info("🌍 This NEW version identifies ANYTHING: Rock? It says rock name. Plant? It says plant name. Food? Car? Dog? Anything!")
