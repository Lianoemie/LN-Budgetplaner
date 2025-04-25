import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sparziele", page_icon="🎯")

# -------------------------------
# Session-State initialisieren
# -------------------------------
if 'sparziele' not in st.session_state:
    st.session_state.sparziele = []

# 🛡️ Sicherheits-Check für alte Einträge
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
        st.rerun()

# -----------------------------
# Übersicht Sparziele
# -----------------------------
if st.session_state.sparziele:
    st.subheader("📋 Übersicht deiner Sparziele")

    def motivation(fortschritt):
        if fortschritt == 1:
            return "🎉 Glückwunsch, du hast dein Sparziel erreicht!"
        elif fortschritt >= 0.75:
            return "🚀 Fast geschafft – das Ziel ist zum Greifen nah!"
        elif fortschritt >= 0.5:
            return "💪 Mehr als die Hälfte ist geschafft – stark!"
        elif fortschritt >= 0.25:
            return "🧱 Du hast schon ein gutes Stück geschafft!"
        else:
            return "✨ Jeder Franken zählt – bleib dran!"

    for index, ziel in enumerate(st.session_state.sparziele):
        st.markdown(f"### 🎯 {ziel['Name']}")
        zielbetrag = ziel["Zielbetrag (CHF)"]
        aktuell = ziel["Bisher gespart (CHF)"]
        rest = max(zielbetrag - aktuell, 0)
        fortschritt = min(aktuell / zielbetrag, 1.0)

        st.text(f"Gespart: {aktuell:.2f} CHF von {zielbetrag:.2f} CHF")
        st.progress(fortschritt)
        st.markdown(f"**💸 Noch fehlend:** {rest:.2f} CHF")
        st.markdown(f"{motivation(fortschritt)}")

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
                    st.rerun()

        # Liste der Einzahlungen mit Lösch-Buttons
        if ziel["Einzahlungen"]:
            st.markdown(f"**📜 Bisherige Einzahlungen für {ziel['Name']}:**")
            for einzahl_index, einzahlung in enumerate(ziel["Einzahlungen"]):
                cols = st.columns([3, 2, 1])
                cols[0].markdown(f"- {einzahlung['Datum']}")
                cols[1].markdown(f"{einzahlung['Betrag (CHF)']:.2f} CHF")
                if cols[2].button("🗑️", key=f"delete_einzahlung_{index}_{einzahl_index}"):
                    ziel["Bisher gespart (CHF)"] -= einzahlung["Betrag (CHF)"]
                    ziel["Einzahlungen"].pop(einzahl_index)
                    st.success("Einzahlung gelöscht.")
                    st.rerun()

        # Button zum Sparziel löschen
        if st.button(f"❌ Sparziel '{ziel['Name']}' löschen", key=f"delete_sparziel_{index}"):
            st.session_state.sparziele.pop(index)
            st.success(f"Sparziel '{ziel['Name']}' wurde gelöscht.")
            st.rerun()

        st.divider()

else:
    st.info("Noch keine Sparziele vorhanden. Lege eines an!")
