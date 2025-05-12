import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Einnahmen hinzufügen", page_icon="💰")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py') 

# ====== App-Daten laden ======
DataManager().load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value=pd.DataFrame(), 
    parse_dates=['timestamp']
)

if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]

st.title("💰 Einnahmen hinzufügen")

# ----------------------------------------
# Neue Einnahme direkt speichern
# ----------------------------------------
with st.form("einnahmen_formular"):
    st.subheader("Neue Einnahme erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_einnahmen)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_einnahme = {
            "typ": "einnahme",
            "kategorie": kategorie,
            "betrag": betrag,
            "beschreibung": beschreibung,
            "timestamp": str(datum)
        }
        DataManager().append_record(
            session_state_key='data_df',
            record_dict=neue_einnahme
        )
        st.success("Einnahme gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der gespeicherten Einnahmen
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
einnahmen_df = data[data['typ'] == 'einnahme']

if not einnahmen_df.empty:
    st.subheader("📋 Übersicht deiner Einnahmen")

    # Nur relevante Spalten und schöne Beschriftung
    einnahmen_df_display = einnahmen_df[["timestamp", "kategorie", "betrag", "beschreibung"]].copy()
    einnahmen_df_display.columns = ["Datum", "Kategorie", "Betrag", "Beschreibung"]
    einnahmen_df_display.index = range(1, len(einnahmen_df_display) + 1)

    # Gesamtsumme anzeigen
    gesamt = einnahmen_df_display["Betrag"].sum()
    st.metric("💵 Gesamteinnahmen", f"{gesamt:.2f} CHF")

    # Tabelle anzeigen
    st.dataframe(einnahmen_df_display, use_container_width=True)

    # Alle Einnahmen löschen
    if st.button("❌ Alle Einnahmen löschen"):
        st.session_state.data_df = data[data['typ'] != 'einnahme']
        DataManager().save_app_data('data_df', 'data.csv')
        st.success("Alle Einnahmen wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Einnahmen eingetragen.")