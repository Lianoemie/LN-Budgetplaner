import streamlit as st
from PIL import Image

# Optionaler rosa Hintergrund
from utils.style import set_background
set_background()

# Titelbild anzeigen
image = Image.open("docs/Fotos/Titelbild.png")  # Pfad anpassen falls nötig
st.image(image, use_column_width=True)

# Optional: etwas Abstand oder Begrüßung
st.markdown("<br><br>", unsafe_allow_html=True)
