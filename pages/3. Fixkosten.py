import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fixkosten", page_icon="📆")

st.title("📆 Fixkosten verwalten")

# Session-State initialisieren
if 'fixkosten' not in st.session_state:
    st.session_state.fixkosten = []

# Neue Fixkosten erfassen
with st.form("fixkosten_formular"):
    st.subheader("➕ Neue Fixkosten hinzufügen")
    kategorie = st.text_input("Kategorie (z. B. Miete, Versicherung)")
    betrag = st.number_input("Monatlicher Betrag (CHF)", min_value=0.0, format="%.2f")
    speichern = st.form_submit_button("Hinzufügen")

    if speichern and kategorie and betrag > 0:
        neue_fixkosten = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag
        }
        st.session_state.fixkosten.append(neue_fixkosten)
        st.success(f"Fixkosten '{kategorie}' gespeichert.")

# Anzeige der Fixkosten
if st.session_state.fixkosten:
    st.subheader("📋 Deine aktuellen Fixkosten")
    df = pd.DataFrame(st.session_state.fixkosten)
    st.table(df)

    gesamt_fixkosten = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamte Fixkosten pro Monat", f"{gesamt_fixkosten:.2f} CHF")
else:
    st.info("Noch keine Fixkosten eingetragen.")
