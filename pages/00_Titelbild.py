import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image

from utils.style import set_background
set_background()

# Titelbild anzeigen
bild = Image.open("docs/Fotos/Titelbild.png")
st.image(bild, use_container_width=True)

# Lottie-Animation laden
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# Animation anzeigen
st_lottie(lottie_animation, speed=1, reverse=False, loop=True, quality="low", height=300)


