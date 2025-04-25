import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sparziele", page_icon="🎯")

# Session-State initialisieren
if 'sparziele' not in st.session_state:
    st.session_state.sparziele = []

st.title("🎯 Sparziele verwalten")

# -----------------------------
# Neues Sparziel erfassen
# -----------------------------
with st.form("sparziel_formular"):
    st.subheader("Neues Sparziel erstellen")
    name = st.text_input("Name des Sparziels")
    zielbetrag = st.number_input("Zielbetrag (CHF)", min_value=1.0, step=10.0, format="%.2f")
    aktueller_betrag = st.number_input("Bisher gespart (CHF)", min_value=0.0, step=10.0, format="%.2f")
    ziel_datum = st.date_input("Gewünschtes Ziel-Datum", value=datetime.today())
    sparziel_erstellen = st.form_submit_button("Sparziel hinzufügen")

    if sparziel_erstellen and name and zielbetrag > 0:
        neues_sparziel = {
            "Name": name,
            "Zielbetrag (CHF)": zielbetrag,
            "Bisher gespart (CHF)": aktueller_betrag,
            "Ziel-Datum": str(ziel_datum)
        }
        st.session_state.sparziele.append(neues_sparziel)
        st.success(f"Sparziel '{name}' wurde hinzugefügt!")

# -----------------------------
# Übersicht Sparziele
# -----------------------------
if st.session_state.sparziele:
    df_sparziele = pd.DataFrame(st.session_state.sparziele)
    df_sparziele.index = range(1, len(df_sparziele) + 1)  # Index beginnt bei 1

    st.subheader("📋 Übersicht deiner Sparziele")
    st.dataframe(df_sparziele, use_container_width=True)

    # Fortschritt anzeigen
    st.subheader("📈 Fortschritt deiner Sparziele")
    for ziel in st.session_state.sparziele:
        name = ziel["Name"]
        zielbetrag = ziel["Zielbetrag (CHF)"]
        aktuell = ziel["Bisher gespart (CHF)"]
        fortschritt = min(aktuell / zielbetrag, 1.0)  # maximal 100%

        st.text(f"{name}: {aktuell:.2f} CHF von {zielbetrag:.2f} CHF")
        st.progress(fortschritt)
else:
    st.info("Noch keine Sparziele vorhanden. Lege eines an!")
