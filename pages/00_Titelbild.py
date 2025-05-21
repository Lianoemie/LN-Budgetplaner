import streamlit as st
import requests
from PIL import Image
import time

from utils.style import set_background # Hintergrundfarbe
set_background() # Hintergrundfarbe anzeigen

# Titelbild anzeigen
bild = Image.open("docs/Fotos/Titelbild.png")
st.image(bild, use_container_width=True)


# Schriftzug mit Typewriter-Effekt
def typewriter(text, delay=0.1):
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"<h1 style='text-align:center;'>{output}</h1>", unsafe_allow_html=True)
        time.sleep(delay)

typewriter("Try it out! 🚀", delay=0.15)

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ffcccc;
        color: black;
        font-size: 18px;
        padding: 0.75em 2em;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)
