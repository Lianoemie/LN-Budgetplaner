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
        DataManager().append_record('data_df', neue_fixkosten)
        st.success("Fixkosten gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der gespeicherten Fixkosten
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
fixkosten_df = data[data['typ'] == 'fixkosten'].copy()

if not fixkosten_df.empty:
    st.subheader("📋 Deine aktuellen Fixkosten")

    fixkosten_df.index = range(1, len(fixkosten_df) + 1)

    gesamt = fixkosten_df["betrag"].sum()
    st.metric("💸 Gesamte Fixkosten (alle)", f"{gesamt:.2f} CHF")

    for idx, row in fixkosten_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        col1.write(str(row["timestamp"]))
        col2.write(row["kategorie"])
        col3.write(f"{row['betrag']:.2f} CHF")
        col4.write(row["wiederholung"])
        col5.write(str(row["stoppdatum"]) if row["stoppdatum"] else "None")
        if col6.button("🗑️", key=f"delete_fixkosten_{idx}"):
            st.session_state.data_df.drop(index=row.name, inplace=True)
            DataManager().save_data("data_df")
            st.success(f"Fixkosten-Eintrag '{row['kategorie']}' gelöscht.")
            st.rerun()

    st.divider()

    if st.button("❌ Alle Fixkosten löschen"):
        st.session_state.data_df = data[data['typ'] != 'fixkosten']
        DataManager().save_data("data_df")
        st.success("Alle Fixkosten wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Fixkosten eingetragen.")
