import streamlit as st
import pandas as pd

# Initialisierung der Session State (wenn nötig)
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []

st.title("Einnahme hinzufügen")

# Eingabeformular für neue Ausgaben
with st.form("ausgabe_formular"):
    kategorie = st.selectbox(
    "Kategorie",
    st.session_state.get('kategorien_einnahmen', ["Lohn", "Stipendium"])
)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    abgesendet = st.form_submit_button("Hinzufügen")

    if abgesendet and betrag > 0:
        neue_Einnahme = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung
        }
        st.session_state.Einnahme.append(neue_Einnahme)
        st.success("Einnahme hinzugefügt!")

# Anzeige der bisherigen Einnahmen
if st.session_state.Einnahme:
    df = pd.DataFrame(st.session_state.Einnahme)
    st.subheader("📋 Deine Einnahmen")
    st.dataframe(df, use_container_width=True)

    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamteinnahmen", f"{gesamt:.2f} CHF")
else:
    st.info("Noch keine Einnahmen eingetragen.")