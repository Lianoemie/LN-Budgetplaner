import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Einnahmen hinzufügen", page_icon="💰")

# ----------------------------------------
# Session-State initialisieren
# ----------------------------------------
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]

st.title("💰 Einnahmen hinzufügen")

# ----------------------------------------
# Neue Einnahme erfassen
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
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung,
            "Datum": str(datum)
        }
        st.session_state.einnahmen.append(neue_einnahme)
        st.success("Einnahme hinzugefügt!")
        st.rerun()

# ----------------------------------------
# Übersicht und Löschfunktionen
# ----------------------------------------
if st.session_state.einnahmen:
    st.subheader("📋 Übersicht deiner Einnahmen")

    for i, eintrag in enumerate(st.session_state.einnahmen):
        cols = st.columns([3, 2, 3, 1])
        cols[0].markdown(f"**{eintrag['Kategorie']}**")
        cols[1].markdown(f"{eintrag['Betrag (CHF)']:.2f} CHF")
        cols[2].markdown(eintrag.get("Beschreibung", "") + f" – {eintrag['Datum']}")
        if cols[3].button("🗑️", key=f"loeschen_{i}"):
            st.session_state.einnahmen.pop(i)
            st.success("Einnahme gelöscht.")
            st.rerun()

    st.markdown("---")

    # Gesamtsumme & DataFrame-Tabelle
    df = pd.DataFrame(st.session_state.einnahmen)
    df.index = range(1, len(df) + 1)
    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💵 Gesamteinnahmen", f"{gesamt:.2f} CHF")

    st.dataframe(df, use_container_width=True)

    # Button: Alle löschen
    if st.button("❌ Alle Einnahmen löschen"):
        st.session_state.einnahmen.clear()
        st.success("Alle Einnahmen wurden gelöscht.")
        st.rerun()

else:
    st.info("Noch keine Einnahmen eingetragen.")
