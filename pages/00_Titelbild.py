import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image

from utils.style import set_background
set_background()

# Titelbild anzeigen
bild = Image.open("images/titelseite.png")
st.image(bild, use_column_width=True)

# Lottie-Animation laden
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Beispiel: Finanz-Animation
lottie_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json")

st_lottie(lottie_animation, speed=1, reverse=False, loop=True, quality="low", height=300)

