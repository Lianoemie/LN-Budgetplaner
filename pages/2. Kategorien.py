import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 

# ====== End Login Block ======

dm = DataManager()

if 'kategorien_df' not in st.session_state:
    file = 'kategorien.csv'
    if os.path.exists(file):
        st.session_state['kategorien_df'] = pd.read_csv(file)
    else:
        st.session_state['kategorien_df'] = pd.DataFrame(columns=["kategorie", "typ", "zeitpunkt"])
        st.session_state['kategorien_df'].to_csv(file, index=False)

# Session-State initialisieren
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("🗂️ Kategorien verwalten")

# -----------------------------
# Neue Kategorie hinzufügen
# -----------------------------
with st.form("neue_kategorie"):
    st.subheader("➕ Neue Kategorie erfassen")
    kategorie = st.text_input("Name der neuen Kategorie")
    kategorie_typ = st.selectbox("Für was ist die Kategorie gedacht?", ["Einnahme", "Ausgabe"])
    hinzufügen = st.form_submit_button("Hinzufügen")

if hinzufügen:
    if not kategorie:
        st.error("Bitte gib einen Namen ein.")
    else:
        liste = (
            st.session_state.kategorien_einnahmen 
            if kategorie_typ == "Einnahme" 
            else st.session_state.kategorien_ausgaben
        )

        if kategorie in liste:
            st.warning("Diese Kategorie existiert bereits.")
        else:
            liste.append(kategorie)
            
            # Sicherstellen, dass 'kategorien_df' im Session State existiert
            if "kategorien_df" not in st.session_state:
                st.session_state["kategorien_df"] = pd.DataFrame(columns=["kategorie", "typ", "zeitpunkt"])

            result = {
                "kategorie": kategorie,
                "typ": kategorie_typ,
                "zeitpunkt": ch_now()  # Gibt aktuellen Timestamp als String zurück
            }

            dm.append_record(session_state_key='kategorien_df', record_dict=result)
            st.success(f"Kategorie '{kategorie}' als {kategorie_typ} hinzugefügt.")

# -----------------------------
# Kategorie löschen
# -----------------------------
st.markdown("---")
st.subheader("🗑️ Kategorie löschen")

with st.form("kategorie_loeschen"):
    # DIREKT den Wert aus der Selectbox nutzen!
    loesch_typ = st.selectbox("Art der Kategorie", ["Einnahme", "Ausgabe"])

    # Richtige Kategorien abhängig von der Auswahl
    if loesch_typ == "Einnahme":
        kategorien = st.session_state.kategorien_einnahmen
    else:
        kategorien = st.session_state.kategorien_ausgaben

    if kategorien:
        auswahl = st.selectbox("Kategorie wählen", kategorien)
    else:
        auswahl = None
        st.info(f"Keine {loesch_typ}-Kategorien vorhanden.")

    loeschen = st.form_submit_button("Löschen")

    if loeschen and auswahl:
        kategorien.remove(auswahl)
        # ✅ Optional: Auch die Löschung im gespeicherten DataFrame vermerken
        result = {
            "kategorie": auswahl,
            "typ": loesch_typ,
            "aktion": "gelöscht",
            "zeitpunkt": ch_now()
        }
        dm.append_record(session_state_key='kategorien_df', record_dict=result)
        st.success(f"Kategorie '{auswahl}' wurde gelöscht.")

# -----------------------------
# Kategorien anzeigen (Badges)
# -----------------------------
st.markdown("---")

def zeige_kategorien(titel, kategorien, farbe):
    st.markdown(f"### {titel}")
    if kategorien:
        badges = " ".join([
            f"<span style='background-color:{farbe}; padding:4px 12px; border-radius:20px; color:white; font-size:14px; margin-right:6px'>{k}</span>"
            for k in kategorien
        ])
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.write("Noch keine Kategorien vorhanden.")

zeige_kategorien("📥 Einnahmen-Kategorien", st.session_state.kategorien_einnahmen, farbe="#4CAF50")
zeige_kategorien("📤 Ausgaben-Kategorien", st.session_state.kategorien_ausgaben, farbe="#F44336")
