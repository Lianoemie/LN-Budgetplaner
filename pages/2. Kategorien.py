import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
from utils.helpers import ch_now

st.set_page_config(page_title="Fixkosten", page_icon="📆")

# ====== Start Login Block ======
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

st.title("📆 Fixkosten verwalten")

# DataManager Instanz (SwitchDrive via WebDAV)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Studibudget")

# Session-State initialisieren und Daten laden
if 'fixkosten_df' not in st.session_state:
    data_manager.load_app_data(
        session_state_key='fixkosten_df',
        file_name='fixkosten.csv',
        initial_value=pd.DataFrame(columns=["Kategorie", "Betrag (CHF)", "Wiederholung", "Datum", "Stoppdatum"])
    )

# Formular zur Eingabe neuer Fixkosten
with st.form("fixkosten_formular"):
    st.subheader("➕ Neue Fixkosten hinzufügen")
    kategorie = st.text_input("Kategorie (z. B. Miete, Versicherung)")
    betrag = st.number_input("Monatlicher Betrag (CHF)", min_value=0.0, format="%.2f")
    wiederholung = st.radio(
        "Wiederholung auswählen",
        options=[
            "Keine Wiederholung", "Wöchentlich", "Zweiwöchentlich",
            "Monatlich", "Halbjährlich", "Jährlich"
        ],
        index=3
    )
    datum = st.date_input("Startdatum der Fixkosten", value=datetime.today())
    stopp_aktiv = st.checkbox("Stoppdatum setzen?")
    stoppdatum = st.date_input("Stoppdatum auswählen") if stopp_aktiv else None

    hinzugefügt = st.form_submit_button("Hinzufügen")

if hinzugefügt:
    if kategorie and betrag > 0:
        neuer_eintrag = {
            "Kategorie": kategorie,
            "Betrag (CHF)": betrag,
            "Wiederholung": wiederholung,
            "Datum": str(datum),
            "Stoppdatum": str(stoppdatum) if stoppdatum else None
        }
        # Direkt speichern über DataManager
        data_manager.append_record(session_state_key='fixkosten_df', record_dict=neuer_eintrag)
        st.success(f"Fixkosten '{kategorie}' gespeichert.")
        st.rerun()
    else:
        st.warning("Bitte Kategorie und Betrag korrekt ausfüllen.")

# Anzeige der gespeicherten Fixkosten
df = st.session_state.fixkosten_df

if not df.empty:
    st.subheader("📋 Deine aktuellen Fixkosten")
    for i, row in df.iterrows():
        cols = st.columns([3, 2, 2, 2, 2, 1])
        cols[0].markdown(f"**{row['Kategorie']}**")
        cols[1].markdown(f"{row['Betrag (CHF)']:.2f} CHF")
        cols[2].markdown(row["Wiederholung"])
        cols[3].markdown(f"📅 Start: {row['Datum']}")
        stopp = row["Stoppdatum"] if pd.notna(row["Stoppdatum"]) else '❌'
        cols[4].markdown(f"📅 Stopp: {stopp}")

        if cols[5].button("🗑️", key=f"loeschen_{i}"):
            df.drop(index=i, inplace=True)
            df.reset_index(drop=True, inplace=True)
            data_manager.save_app_data(
                session_state_key='fixkosten_df',
                file_name='fixkosten.csv',
                dataframe=df
            )
            st.success("Fixkosten gelöscht.")
            st.rerun()

    st.markdown("---")
    gesamt_fixkosten = df["Betrag (CHF)"].sum()
    st.metric("💸 Gesamte Fixkosten (alle)", f"{gesamt_fixkosten:.2f} CHF")

    if st.button("❌ Alle Fixkosten löschen"):
        st.session_state.fixkosten_df = pd.DataFrame(columns=df.columns)
        data_manager.save_app_data(
            session_state_key='fixkosten_df',
            file_name='fixkosten.csv',
            dataframe=st.session_state.fixkosten_df
        )
        st.success("Alle Fixkosten wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Fixkosten eingetragen.")
