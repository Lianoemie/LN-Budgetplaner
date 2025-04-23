import streamlit as st
import pandas as pd

# Initialisierung der Session State (wenn nötig)
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []

st.title("💰 Budgetplaner")

# Eingabeformular für neue Ausgaben
with st.form("ausgabe_formular"):
    kategorie = st.selectbox("Kategorie", ["Lebensmittel", "Miete", "Freizeit", "Transport", "Sonstiges"])
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    abgesendet = st.form_submit_button("Hinzufügen")

    if abgesendet and betrag > 0:
        neue_ausgabe = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung
        }
        st.session_state.ausgaben.append(neue_ausgabe)
        st.success("Ausgabe hinzugefügt!")

# Anzeige der bisherigen Ausgaben
if st.session_state.ausgaben:
    df = pd.DataFrame(st.session_state.ausgaben)
    st.subheader("📋 Deine Ausgaben")
    st.dataframe(df, use_container_width=True)

    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")
