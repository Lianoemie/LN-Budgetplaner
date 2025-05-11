import streamlit as st
import pandas as pd
from datetime import datetime

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 

# ====== End Login Block ======


st.set_page_config(page_title="Ausgaben hinzufügen", page_icon="💸")

# ----------------------------------------
# Session-State initialisieren
# ----------------------------------------
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("💸 Ausgaben hinzufügen")

# ----------------------------------------
# Neue Ausgabe erfassen
# ----------------------------------------
with st.form("ausgabe_formular"):
    st.subheader("Neue Ausgabe erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_ausgaben)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_ausgabe = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Beschreibung": beschreibung,
            "Datum": str(datum)
        }
        st.session_state.ausgaben.append(neue_ausgabe)
        st.success("Ausgabe hinzugefügt!")
        st.rerun()

# ----------------------------------------
# Übersicht und Löschfunktionen
# ----------------------------------------
if st.session_state.ausgaben:
    st.subheader("📋 Übersicht deiner Ausgaben")

    for i, eintrag in enumerate(st.session_state.ausgaben):
        cols = st.columns([3, 2, 3, 1])
        cols[0].markdown(f"**{eintrag['Kategorie']}**")
        cols[1].markdown(f"{eintrag['Betrag (CHF)']:.2f} CHF")
        cols[2].markdown(eintrag.get("Beschreibung", "") + f" – {eintrag['Datum']}")
        if cols[3].button("🗑️", key=f"loeschen_{i}"):
            st.session_state.ausgaben.pop(i)
            st.success("Ausgabe gelöscht.")
            st.rerun()

    st.markdown("---")

    # Gesamtsumme & DataFrame-Tabelle (optional)
    df = pd.DataFrame(st.session_state.ausgaben)
    df.index = range(1, len(df) + 1)
    gesamt = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")

    # Tabelle anzeigen
    st.dataframe(df, use_container_width=True)

    # Button: Alle löschen
    if st.button("❌ Alle Ausgaben löschen"):
        st.session_state.ausgaben.clear()
        st.success("Alle Ausgaben wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Ausgaben eingetragen.")
