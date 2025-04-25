import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sparziele", page_icon="🎯")

# ----------------------------------------
# Session-State initialisieren + absichern
# ----------------------------------------
if 'sparziele' not in st.session_state:
    st.session_state.sparziele = []

# 🛡️ Sicherheits-Check für alte Sparziele ohne 'Einzahlungen'
for ziel in st.session_state.sparziele:
    if "Einzahlungen" not in ziel:
        ziel["Einzahlungen"] = []

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
            "Ziel-Datum": str(ziel_datum),
            "Einzahlungen": []
        }
        st.session_state.sparziele.append(neues_sparziel)
        st.success(f"Sparziel '{name}' wurde hinzugefügt!")
        st.experimental_rerun()

# -----------------------------
# Übersicht Sparziele
# -----------------------------
if st.session_state.sparziele:
    st.subheader("📋 Übersicht deiner Sparziele")

    for index, ziel in enumerate(st.session_state.sparziele):
        st.markdown(f"### 🎯 {ziel['Name']}")
        zielbetrag = ziel["Zielbetrag (CHF)"]
        aktuell = ziel["Bisher gespart (CHF)"]
        fortschritt = min(aktuell / zielbetrag, 1.0)

        st.text(f"Gespart: {aktuell:.2f} CHF von {zielbetrag:.2f} CHF")
        st.progress(fortschritt)

        # Einzahlung hinzufügen
        with st.expander(f"➕ Einzahlung hinzufügen für {ziel['Name']}"):
            betrag = st.number_input(
                f"Betrag einzahlen für '{ziel['Name']}'",
                min_value=0.0,
                step=10.0,
                format="%.2f",
                key=f"einzahlen_{index}"
            )
            if st.button(f"Einzahlen auf '{ziel['Name']}'", key=f"button_{index}"):
                if betrag > 0:
                    ziel["Bisher gespart (CHF)"] += betrag
                    ziel["Einzahlungen"].append({
                        "Betrag (CHF)": betrag,
                        "Datum": datetime.today().strftime("%Y-%m-%d")
                    })
                    st.success(f"{betrag:.2f} CHF erfolgreich auf '{ziel['Name']}' eingezahlt!")
                    st.experimental_rerun()

        # Liste der Einzahlungen
        if ziel["Einzahlungen"]:
            st.markdown(f"**📜 Bisherige Einzahlungen für {ziel['Name']}:**")
            einzahlungen_df = pd.DataFrame(ziel["Einzahlungen"])
            einzahlungen_df["Betrag (CHF)"] = einzahlungen_df["Betrag (CHF)"].map(lambda x: f"{x:.2f}")
            einzahlungen_df.index = range(1, len(einzahlungen_df) + 1)
            st.table(einzahlungen_df)

        st.divider()

else:
    st.info("Noch keine Sparziele vorhanden. Lege eines an!")
