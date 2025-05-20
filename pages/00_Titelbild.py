import streamlit as st
from PIL import Image

# Seite konfigurieren (muss ganz oben stehen)
st.set_page_config(page_title="Titelseite", page_icon="🎓")

# Optionaler rosa Hintergrund
from utils.style import set_background
set_background()

# Titelbild anzeigen
image = Image.open("Fotos/Titelbild.png")  # Pfad anpassen falls nötig
st.image(image, use_column_width=True)

# Optional: etwas Abstand oder Begrüßung
st.markdown("<br><br>", unsafe_allow_html=True)
