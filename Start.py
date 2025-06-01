
import streamlit as st
import pandas as pd
import os
import requests
import time

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

from utils.style import set_background #Hintergrundfarbe
set_background()

# Initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Studibudget")

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    #parse_dates = ['timestamp']
    )

# --- Welcome Page ---
col1, col2 = st.columns([4, 7])  #Logo neben dem Titel
with col1:
    st.title("Studibudget")
with col2:
    st.image("docs/Fotos/Logo.png", width=80)


st.markdown("""
# Willkommen bei **Studibudget** 🎉

Schön, dass du hier bist!  
**Studibudget** hilft dir dabei, deine **Einnahmen**, **Ausgaben** und **Sparziele** einfach und strukturiert zu verwalten – damit du jederzeit den Überblick über deine Finanzen behältst.
""")

st.markdown("""
### ✨ Mit Studibudget kannst du:

- 💰 **Persönliche Einnahmen und Ausgaben erfassen:**  
  Trage regelmäßige oder einmalige Einnahmen wie Lohn, Stipendien und auch Ausgaben ein und verfolge deine monatlichen Finanzbewegungen übersichtlich.

- 🧾 **Fixkosten verwalten:**  
  Halte deine wiederkehrenden Ausgaben wie Miete, Versicherungen oder Handyabos fest und plane dadurch besser dein monatliches Budget.

- 🎯 **Sparziele setzen:**  
  Lege individuelle Sparziele an, zum Beispiel für Reisen oder ein neues Handy, und verfolge deinen Fortschritt.

- 📊 **Statistiken einsehen:**  
  Analysiere deine Ausgaben- und Einnahmenentwicklung mithilfe von Grafiken und Auswertungen.

- 📂 **Kategorien individuell anpassen:**  
  Erstelle eigene Kategorien, um deine Einnahmen und Ausgaben genau so zu ordnen, wie es für dich am besten passt. Ein paar Beispiele, die du auch wieder löschen kannst, haben wir bereits für dich vorbereitet.

- 📚 **Spartipps entdecken:**  
  Lass dich von unseren Spartipps inspirieren, um deine Ausgaben weiter zu optimieren.

- 👤 **Dein Profil personalisieren:**  
  Verwalte persönliche Informationen oder Eingaben und passe deine App-Einstellungen an.
            
Alle deine Eingaben werden gespeichert und zentrale Werte sind jederzeit auf der **Startseite** einsehbar.
""")

st.info("""
🔔 **Hinweis:**  
**Studibudget** unterstützt dich beim Finanzmanagement – ersetzt jedoch **keine professionelle Finanzberatung**.
Für eine umfassende Beurteilung deiner finanziellen Situation wende dich bitte an eine Fachperson.
""")

st.markdown("""
## 📖 Über Studibudget
Diese Anwendung wurde von **Selina Rüdisüli**, **Elena Stevanovic** und **Lia Müller**
im Rahmen des Moduls **"BMLD Informatik 2"** an der **ZHAW** entwickelt.

Viel Spaß beim Planen und Verwalten deiner Finanzen!
""")

# Schriftzug mit Typewriter-Effekt
def typewriter(text, delay=0.1):
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"<h1 style='text-align:center;'>{output}</h1>", unsafe_allow_html=True)
        time.sleep(delay)

typewriter("Try it out! 🚀", delay=0.15)

if st.button("👉 Beginne hier"):    #Button zur Kategorienpage
    st.switch_page("pages/02_Kategorien.py")