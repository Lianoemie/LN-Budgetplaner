
import streamlit as st
import pandas as pd

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
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 10px;">Studibudget</h1>
        <img src="docs/Fotos/Logo.png" width="50">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
# Willkommen bei **Studibudget** 🎉


Schön, dass du hier bist!  
**Studibudget** hilft dir dabei, deine **Einnahmen**, **Ausgaben** und **Sparziele** einfach und strukturiert zu verwalten – damit du jederzeit den Überblick über deine Finanzen behältst.
""")

st.markdown("""
### ✨ Mit Studibudget kannst du:

- 💰 **Persönliche Einnahmen erfassen:**  
  Trage regelmäßige oder einmalige Einnahmen wie Lohn, Stipendien oder Geschenke ein und verfolge deine monatlichen Einnahmen übersichtlich.

- 🧾 **Fixkosten verwalten:**  
  Halte deine wiederkehrenden Ausgaben wie Miete, Versicherungen oder Handyabos fest und plane dadurch besser dein monatliches Budget.

- 🎯 **Sparziele setzen:**  
  Lege individuelle Sparziele an, zum Beispiel für Reisen oder ein neues Handy, und verfolge deinen Fortschritt.

- 📊 **Statistiken einsehen:**  
  Analysiere deine Ausgaben- und Einnahmenentwicklung mithilfe von Grafiken und Auswertungen.

- 📂 **Kategorien individuell anpassen:**  
  Erstelle eigene Kategorien, um deine Einnahmen und Ausgaben genau so zu ordnen, wie es für dich am besten passt.

- 📚 **Spartipps entdecken:**  
  Lass dich von unseren Spartipps inspirieren, um deine Ausgaben weiter zu optimieren.

- 👤 **Dein Profil personalisieren:**  
  Verwalte persönliche Informationen und passe deine App-Einstellungen an.
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

