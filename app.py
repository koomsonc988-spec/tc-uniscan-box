import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="TC UniScan Box", page_icon="🚀")
st.title("🚀 TC UniScan Box - AI Universe Scanner")
st.caption("By Tandoh Caleb - TC AI Ghana | Built for UMaT")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Add GOOGLE_API_KEY in Secrets")
    st.stop()

uploaded = st.file_uploader("📦 Upload ANYTHING", type=["jpg","png","jpeg"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, use_container_width=True)
    prompt = "You are TC UniScan Box by Tandoh Caleb. Scan this image deeply, explain brand, model, all parts, functions, how to use it."
    with st.spinner("Scanning..."):
        try:
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[prompt, img]
            )
            st.success("✅ Scan Complete!")
            st.markdown(response.text)
        except Exception as e:
            except Exception as e:
    if "503" in str(e):
        st.warning("🚀 Universe is busy! So many TC users scanning! Wait 15 seconds and tap Scan again - it works on 2nd try!")
    else:
        st.error(f"Error: {e}")
