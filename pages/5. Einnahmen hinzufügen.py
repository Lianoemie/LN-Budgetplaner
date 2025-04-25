import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Einnahmen hinzufügen", page_icon="💰")

# Session-State initialisieren
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]

st.title("💰 Einnahmen hinzufügen")

with st.form("einnahmen_formular"):
    st.subheader("Neue Einnahme erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_einnahmen)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_einnahme = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung,
            "Datum": str(datum)
        }
        st.session_state.einnahmen.append(neue_einnahme)
        st.success("Einnahme hinzugefügt!")

if st.session_state.einnahmen:
    df = pd.DataFrame(st.session_state.einnahmen)
    df.index = range(1, len(df) + 1)  # <-- Index beginnt jetzt bei 1
    st.subheader("📋 Übersicht deiner Einnahmen")
    st.dataframe(df, use_container_width=True)
    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💵 Gesamteinnahmen", f"{gesamt:.2f} CHF")
else:
    st.info("Noch keine Einnahmen eingetragen.")
