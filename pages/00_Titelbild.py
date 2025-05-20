import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import time

from utils.style import set_background # Hintergrundfarbe
set_background() # Hintergrundfarbe anzeigen

# Titelbild anzeigen
bild = Image.open("docs/Fotos/Titelbild.png")
st.image(bild, use_container_width=True)

# Lottie-Animation laden
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Beispiel: Finanz-Animation
lottie_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json")

st_lottie(lottie_animation, speed=1, reverse=False, loop=True, quality="low", height=300)


# Schriftzug mit Typewriter-Effekt
def typewriter(text, delay=0.1):
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"<h1 style='text-align:center;'>{output}</h1>", unsafe_allow_html=True)
        time.sleep(delay)

typewriter("Try it out! 🚀", delay=0.15)

