import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ausgaben hinzufügen", page_icon="💸")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py') 

# ====== App-Daten laden ======
DataManager().load_app_data(
    session_state_key='ausgaben_df', 
    file_name='ausgaben.csv', 
    initial_value=pd.DataFrame(), 
    parse_dates=['timestamp']
)

# ====== Kategorien initialisieren ======
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("💸 Ausgaben hinzufügen")

# ----------------------------------------
# Neue Ausgabe direkt speichern
# ----------------------------------------
with st.form("ausgabe_formular"):
    st.subheader("Neue Ausgabe erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_ausgaben)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_ausgabe = {
            "typ": "ausgabe",
            "kategorie": kategorie,
            "betrag": betrag,
            "beschreibung": beschreibung,
            "timestamp": str(datum)
        }
        DataManager().append_record(
            session_state_key='ausgaben_df',
            record_dict=neue_ausgabe
        )
        st.success("Ausgabe gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der gespeicherten Ausgaben
# ----------------------------------------
data = st.session_state.get('ausgaben_df', pd.DataFrame())
ausgaben_df = data[data['typ'] == 'ausgabe']

if not ausgaben_df.empty:
    st.subheader("📋 Übersicht deiner Ausgaben")
    ausgaben_df_display = ausgaben_df.copy()
    ausgaben_df_display.index = range(1, len(ausgaben_df_display) + 1)
    gesamt = ausgaben_df_display["betrag"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")
    st.dataframe(ausgaben_df_display, use_container_width=True)

    # Alle Ausgaben löschen
    if st.button("❌ Alle Ausgaben löschen"):
        st.session_state.ausgaben_df = data[data['typ'] != 'ausgabe']
        DataManager().save_app_data('ausgaben_df', 'ausgaben.csv')
        st.success("Alle Ausgaben wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Ausgaben eingetragen.")
