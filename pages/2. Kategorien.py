import streamlit as st
import pandas as pd

from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

# Seiteneinstellungen
st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# Login
LoginManager().go_to_login('Start.py')

# DataManager initialisieren
dm = DataManager()

# Initialisierung der Session-State-Variablen
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium", "Schenkungen"]
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Miete", "Freizeit", "Transport", "Geschenke", "Sonstiges"]
if 'kategorien_df' not in st.session_state:
    st.session_state.kategorien_df = pd.DataFrame(columns=["kategorie", "typ", "aktion", "zeitpunkt"])

# Titel
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
            liste = st.session_state.kategorien_einnahmen if kategorie_typ == "Einnahme" else st.session_state.kategorien_ausgaben
            if kategorie in liste:
                st.warning("Diese Kategorie existiert bereits.")
            else:
                liste.append(kategorie)
                result = {
                    "kategorie": kategorie,
                    "typ": kategorie_typ,
                    "aktion": "hinzugefügt",
                    "zeitpunkt": ch_now()
                }
                dm.append_record(session_state_key='kategorien_df', record_dict=result)
                st.success(f"Kategorie '{kategorie}' als {kategorie_typ} hinzugefügt.")

# -----------------------------
# Kategorie löschen
# -----------------------------
st.markdown("---")
st.subheader("🗑️ Kategorie löschen")

loesch_typ = st.radio("Art der Kategorie", ["Einnahme", "Ausgabe"])

if loesch_typ == "Einnahme":
    kategorien_liste = st.session_state.kategorien_einnahmen
else:
    kategorien_liste = st.session_state.kategorien_ausgaben

if kategorien_liste:
    auswahl = st.selectbox("Kategorie wählen", kategorien_liste)
    if st.button("Kategorie löschen"):
        if loesch_typ == "Einnahme":
            st.session_state.kategorien_einnahmen.remove(auswahl)
        else:
            st.session_state.kategorien_ausgaben.remove(auswahl)

        result = {
            "kategorie": auswahl,
            "typ": loesch_typ,
            "aktion": "gelöscht",
            "zeitpunkt": ch_now()
        }
        dm.append_record(session_state_key='kategorien_df', record_dict=result)
        st.success(f"Kategorie '{auswahl}' wurde gelöscht.")
        st.rerun()
else:
    st.info(f"Keine {loesch_typ}-Kategorien vorhanden.")

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
