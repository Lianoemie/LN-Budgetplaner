import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Fixkosten", page_icon="📆")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 

# ====== End Login Block ======

st.title("📆 Fixkosten verwalten")

# -------------------------------------
# DataManager Initialisierung
# -------------------------------------
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_DB")

# -------------------------------------
# Fixkosten aus persistentem Speicher laden
# -------------------------------------
if 'fixkosten' not in st.session_state:
    data_manager.load_app_data(
        session_state_key='fixkosten',
        file_name='fixkosten.csv',
        initial_value=[],
    )

# 🔐 Sicherheits-Update für ältere Einträge
for eintrag in st.session_state.fixkosten:
    if "Wiederholung" not in eintrag:
        eintrag["Wiederholung"] = "Monatlich"
    if "Datum" not in eintrag:
        eintrag["Datum"] = datetime.today().strftime("%Y-%m-%d")
    if "Stoppdatum" not in eintrag:
        eintrag["Stoppdatum"] = None

# -------------------------------------
# Formular-Elemente (außerhalb des st.form)
# -------------------------------------
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
    index=3
)

datum = st.date_input("Startdatum der Fixkosten", value=datetime.today())

stopp_aktiv = st.checkbox("Stoppdatum setzen?")
stoppdatum = None
if stopp_aktiv:
    stoppdatum = st.date_input("Stoppdatum auswählen")

# -------------------------------------
# Speichern (innerhalb form)
# -------------------------------------
if st.button("Hinzufügen"):
    if kategorie and betrag > 0:
        neue_fixkosten = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Wiederholung": wiederholung,
            "Datum": str(datum),
            "Stoppdatum": str(stoppdatum) if stoppdatum else None
        }
        st.session_state.fixkosten.append(neue_fixkosten)
        st.success(f"Fixkosten '{kategorie}' gespeichert.")
        st.rerun()
    else:
        st.warning("Bitte Kategorie und Betrag korrekt ausfüllen.")

# -------------------------------------
# Anzeige der Fixkosten + Löschoption
# -------------------------------------
if st.session_state.fixkosten:
    st.subheader("📋 Deine aktuellen Fixkosten")

    for i, eintrag in enumerate(st.session_state.fixkosten):
        cols = st.columns([3, 2, 2, 2, 2, 1])
        cols[0].markdown(f"**{eintrag['Kategorie']}**")
        cols[1].markdown(f"{eintrag['Betrag (CHF)']:.2f} CHF")
        cols[2].markdown(eintrag["Wiederholung"])
        cols[3].markdown(f"📅 Start: {eintrag['Datum']}")
        cols[4].markdown(f"📅 Stopp: {eintrag['Stoppdatum'] if eintrag['Stoppdatum'] else '❌'}")
        if cols[5].button("🗑️", key=f"loeschen_{i}"):
            st.session_state.fixkosten.pop(i)
            st.success("Fixkosten gelöscht.")
            st.rerun()

    st.markdown("---")

    df = pd.DataFrame(st.session_state.fixkosten)
    gesamt_fixkosten = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamte Fixkosten (alle)", f"{gesamt_fixkosten:.2f} CHF")

    if st.button("❌ Alle Fixkosten löschen"):
        st.session_state.fixkosten.clear()
        st.success("Alle Fixkosten wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Fixkosten eingetragen.")
