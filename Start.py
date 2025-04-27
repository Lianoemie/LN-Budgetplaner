import streamlit as st
import pandas as pd

from utils.data_manager import DataManager

# Initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Studibudget")

# Load the data from persistent storage into session state
data_manager.load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value=pd.DataFrame(), 
    parse_dates=['timestamp']
)

# --- Welcome Page ---
st.title('Studibudget 📅')

st.markdown("""
# Willkommen bei **Studibudget** 🎉

Schön, dass du hier bist! Diese App hilft dir dabei, deine **Einnahmen** und **Ausgaben** einfach und strukturiert zu verwalten.

---
""")

st.info("""
**Hinweis:** Studibudget unterstützt dich beim Finanzmanagement – ersetzt jedoch **keine professionelle Finanzberatung**.
Für eine umfassende Beurteilung deiner finanziellen Situation wende dich bitte an eine Fachperson.
""")

st.markdown("""
## 📖 Über Studibudget
Diese Anwendung wurde von **Selina Rüdisüli**, **Elena Stevanovic** und **Lia Müller**
im Rahmen des Moduls **"BMLD Informatik 2"** an der **ZHAW** entwickelt.

Viel Spaß beim Planen und Verwalten deiner Finanzen!
""")
