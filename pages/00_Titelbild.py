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

# ➕ HTML-zentrierter Button mit Streamlit-Callback
st.markdown("""
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 3em;
    }
    .center-button button {
        background-color: #ffccd5;
        color: black;
        font-size: 20px;
        padding: 0.8em 2.5em;
        border-radius: 12px;
        border: none;
        cursor: pointer;
    }
    </style>
    <div class="center-button">
        <form action="" method="post">
            <button name="start" type="submit">👉 Beginne hier</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Interaktion abfangen
if "start" in st.session_state or st.experimental_get_query_params().get("start"):
    st.switch_page("pages/1_Kategorie.py")