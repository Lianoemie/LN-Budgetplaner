import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ausgaben hinzufügen", page_icon="💸")

# Session-State initialisieren
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("💸 Ausgaben hinzufügen")

with st.form("ausgabe_formular"):
    st.subheader("Neue Ausgabe erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_ausgaben)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_ausgabe = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung,
            "Datum": str(datum)
        }
        st.session_state.ausgaben.append(neue_ausgabe)
        st.success("Ausgabe hinzugefügt!")

if st.session_state.ausgaben:
    df = pd.DataFrame(st.session_state.ausgaben)
    st.subheader("📋 Übersicht deiner Ausgaben")
    st.dataframe(df, use_container_width=True)
    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")
else:
    st.info("Noch keine Ausgaben eingetragen.")
