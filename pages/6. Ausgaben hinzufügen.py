import streamlit as st
import pandas as pd

st.set_page_config(page_title="Budgetplaner CHF", page_icon="💰")

# Session-State initialisieren
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = [
        {"Kategorie": "Freizeit", "Betrag (CHF)": 50.00, "Beschreibung": "Kino"},
        {"Kategorie": "Miete", "Betrag (CHF)": 1200.00, "Beschreibung": "Wohnung"},
        {"Kategorie": "Lebensmittel", "Betrag (CHF)": 180.00, "Beschreibung": "Wocheneinkauf"},
        {"Kategorie": "Transport", "Betrag (CHF)": 75.00, "Beschreibung": "ÖV-Abo"}
    ]

st.title("Ausgaben hinzufügen")

# Eingabeformular für neue Ausgaben
with st.form("ausgabe_formular"):
    st.subheader("Neue Ausgabe erfassen")
    kategorie = st.selectbox(
    "Kategorie",
    st.session_state.get('kategorien_ausgaben', ["Lebensmittel", "Miete", "Freizeit", "Transport"])
)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_ausgabe = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung
        }
        st.session_state.ausgaben.append(neue_ausgabe)
        st.success("Ausgabe hinzugefügt!")

# Daten als DataFrame anzeigen
if st.session_state.ausgaben:
    df = pd.DataFrame(st.session_state.ausgaben)
    
    st.subheader("📋 Übersicht deiner Ausgaben")
    st.dataframe(df, use_container_width=True)
    
    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")

    # Gruppierte Übersicht
    st.subheader("🔍 Ausgaben nach Kategorie")
    gruppiert = df.groupby("Kategorie")["Betrag (CHF)"].sum()
    st.bar_chart(gruppiert)
else:
    st.info("Noch keine Ausgaben eingetragen.")
