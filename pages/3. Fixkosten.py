import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Fixkosten", page_icon="📆")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py')

# ====== App-Daten laden ======
DataManager().load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

if 'kategorien_fixkosten' not in st.session_state:
    st.session_state.kategorien_fixkosten = ["Miete", "Versicherung", "ÖV", "Streaming"]

st.title("📆 Fixkosten verwalten")

# ----------------------------------------
# Neue Fixkosten direkt speichern
# ----------------------------------------
with st.form("fixkosten_formular"):
    st.subheader("➕ Neue Fixkosten hinzufügen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_fixkosten)
    betrag = st.number_input("Monatlicher Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    wiederholung = st.radio(
        "Wiederholung auswählen",
        options=[
            "Keine Wiederholung",
            "Wöchentlich",
            "Zweiwöchentlich",
            "Monatlich",
            "Halbjährlich",
            "Jährlich"
        ],
        index=3
    )
    datum = st.date_input("Startdatum der Fixkosten", value=datetime.today())

    stopp_aktiv = st.checkbox("Stoppdatum setzen?")
    stoppdatum = None
    if stopp_aktiv:
        stoppdatum = st.date_input("Stoppdatum auswählen")

    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_fixkosten = {
            "typ": "fixkosten",
            "kategorie": kategorie,
            "betrag": betrag,
            "wiederholung": wiederholung,
            "beschreibung": "",
            "timestamp": str(datum),
            "stoppdatum": str(stoppdatum) if stoppdatum else None
        }
        DataManager().append_record(
            session_state_key='data_df',
            record_dict=neue_fixkosten
        )
        st.success("Fixkosten gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der gespeicherten Fixkosten
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
fixkosten_df = data[data['typ'] == 'fixkosten']

if not fixkosten_df.empty:
    st.subheader("📋 Deine aktuellen Fixkosten")

    fixkosten_df_display = fixkosten_df[["timestamp", "kategorie", "betrag", "wiederholung", "stoppdatum"]].copy()
    fixkosten_df_display.columns = ["Startdatum", "Kategorie", "Betrag", "Wiederholung", "Stoppdatum"]
    fixkosten_df_display.index = range(1, len(fixkosten_df_display) + 1)

    gesamt = fixkosten_df_display["Betrag"].sum()
    st.metric("💸 Gesamte Fixkosten (alle)", f"{gesamt:.2f} CHF")

    st.dataframe(fixkosten_df_display, use_container_width=True)

    if st.button("❌ Alle Fixkosten löschen"):
        st.session_state.data_df = data[data['typ'] != 'fixkosten']
        DataManager().save_app_data('data_df', 'data.csv')
        st.success("Alle Fixkosten wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Fixkosten eingetragen.")
