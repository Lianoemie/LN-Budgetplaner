import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fixkosten", page_icon="📆")

st.title("📆 Fixkosten verwalten")

# -------------------------------------
# Session-State initialisieren
# -------------------------------------
if 'fixkosten' not in st.session_state:
    st.session_state.fixkosten = []

# -------------------------------------
# Neue Fixkosten erfassen
# -------------------------------------
with st.form("fixkosten_formular"):
    st.subheader("➕ Neue Fixkosten hinzufügen")
    kategorie = st.text_input("Kategorie (z. B. Miete, Versicherung)")
    betrag = st.number_input("Monatlicher Betrag (CHF)", min_value=0.0, format="%.2f")

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
        index=3  # Standard auf "Monatlich"
    )

    speichern = st.form_submit_button("Hinzufügen")

    if speichern and kategorie and betrag > 0:
        neue_fixkosten = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Wiederholung": wiederholung
        }
        st.session_state.fixkosten.append(neue_fixkosten)
        st.success(f"Fixkosten '{kategorie}' gespeichert.")

# -------------------------------------
# Anzeige der Fixkosten + Löschoption
# -------------------------------------
if st.session_state.fixkosten:
    st.subheader("📋 Deine aktuellen Fixkosten")

    # Einzelne Fixkosten anzeigen mit Löschen-Button
    for i, eintrag in enumerate(st.session_state.fixkosten):
        cols = st.columns([3, 2, 3, 1])
        cols[0].markdown(f"**{eintrag['Kategorie']}**")
        cols[1].markdown(f"{eintrag['Betrag (CHF)']:.2f} CHF")
        cols[2].markdown(eintrag["Wiederholung"])
        if cols[3].button("🗑️", key=f"loeschen_{i}"):
            st.session_state.fixkosten.pop(i)
            st.success("Fixkosten gelöscht.")
            st.rerun()

    st.markdown("---")

    # Gesamtsumme anzeigen
    df = pd.DataFrame(st.session_state.fixkosten)
    gesamt_fixkosten = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamte Fixkosten pro Monat", f"{gesamt_fixkosten:.2f} CHF")

    # Alle löschen Button
    if st.button("❌ Alle Fixkosten löschen"):
        st.session_state.fixkosten.clear()
        st.success("Alle Fixkosten wurden gelöscht.")
        st.rerun()

else:
    st.info("Noch keine Fixkosten eingetragen.")
