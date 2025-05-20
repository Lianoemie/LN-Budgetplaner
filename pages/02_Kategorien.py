import streamlit as st
import pandas as pd
from utils.style import set_background
set_background()


st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py')
dm = DataManager()

# ====== App-Daten laden ======
dm.load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

# Session-State initialisieren
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("🗂️ Kategorien verwalten")

# ----------------------------------------
# Neue Kategorie hinzufügen
# ----------------------------------------
with st.form("neue_kategorie"):
    st.subheader("➕ Neue Kategorie erfassen")
    kategorie = st.text_input("Name der neuen Kategorie")
    kategorie_typ = st.selectbox("Für was ist die Kategorie gedacht?", ["Einnahme", "Ausgabe"])
    hinzufügen = st.form_submit_button("Hinzufügen")

if hinzufügen:
    if not kategorie:
        st.error("Bitte gib einen Namen ein.")
    else:
        kategorien_liste = (
            st.session_state.kategorien_einnahmen 
            if kategorie_typ == "Einnahme" 
            else st.session_state.kategorien_ausgaben
        )

        if kategorie in kategorien_liste:
            st.warning("Diese Kategorie existiert bereits.")
        else:
            kategorien_liste.append(kategorie)

            neue_kategorie = {
                "typ": "kategorie",
                "kategorie": kategorie,
                "kategorie_typ": kategorie_typ,
                "timestamp": ch_now()
            }
            dm.append_record(session_state_key='data_df', record_dict=neue_kategorie)
            st.success(f"Kategorie '{kategorie}' als {kategorie_typ} hinzugefügt.")
            st.rerun()

# ----------------------------------------
# Kategorie löschen
# ----------------------------------------
st.markdown("---")
st.subheader("🗑️ Kategorie löschen")

# Zuerst den Typ außerhalb des Formulars auswählen (reaktiv)
loesch_typ = st.selectbox("Art der Kategorie", ["Einnahme", "Ausgabe"])

# Richtige Liste basierend auf dem ausgewählten Typ
kategorien_liste = (
    st.session_state.kategorien_einnahmen 
    if loesch_typ == "Einnahme" 
    else st.session_state.kategorien_ausgaben
)

if kategorien_liste:
    with st.form("kategorie_loeschen"):
        auswahl = st.selectbox("Kategorie wählen", kategorien_liste)
        loeschen = st.form_submit_button("Löschen")

        if loeschen and auswahl:
            kategorien_liste.remove(auswahl)

            geloeschte_kategorie = {
                "typ": "kategorie_geloescht",
                "kategorie": auswahl,
                "kategorie_typ": loesch_typ,
                "timestamp": ch_now()
            }
            dm.append_record(session_state_key='data_df', record_dict=geloeschte_kategorie)
            st.success(f"Kategorie '{auswahl}' wurde gelöscht.")
            st.rerun()
else:
    st.info(f"Keine {loesch_typ}-Kategorien vorhanden.")

# ----------------------------------------
# Kategorien anzeigen (Badges)
# ----------------------------------------
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

