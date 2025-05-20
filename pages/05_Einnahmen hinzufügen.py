from utils.style import set_background #Hintergrundfarbe
set_background()
import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="Einnahmen hinzufügen", page_icon="💰")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py') 

# ====== App-Daten laden ======
DataManager().load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value=pd.DataFrame(), 
    parse_dates=['timestamp']
)

if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]

st.title("💰 Einnahmen hinzufügen")

# ----------------------------------------
# 📅 Monat auswählen
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

alle_monate = data[data["typ"] == "einnahme"]["timestamp"].dropna().dt.to_period("M").sort_values().unique()
alle_monate_str = [str(monat) for monat in alle_monate]

aktueller_monat = datetime.now().strftime("%Y-%m")
ausgewaehlter_monat = st.selectbox(
    "Monat auswählen",
    options=alle_monate_str if alle_monate_str else [aktueller_monat],
    index=alle_monate_str.index(aktueller_monat) if aktueller_monat in alle_monate_str else 0
)

# ----------------------------------------
# Neue Einnahme direkt speichern
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
            "typ": "einnahme",
            "kategorie": kategorie,
            "betrag": betrag,
            "beschreibung": beschreibung,
            "timestamp": str(datum)
        }
        DataManager().append_record(
            session_state_key='data_df',
            record_dict=neue_einnahme
        )
        st.success("Einnahme gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der gefilterten Einnahmen
# ----------------------------------------
einnahmen_df = data[
    (data['typ'] == 'einnahme') & 
    (data['timestamp'].dt.to_period("M") == ausgewaehlter_monat)
].copy()

einnahmen_df = einnahmen_df.sort_values(by="timestamp", ascending=False)

if not einnahmen_df.empty:
    st.subheader(f"📋 Einnahmen im Monat {ausgewaehlter_monat}")

    # Originalindex speichern für Löschung
    einnahmen_df["original_index"] = einnahmen_df.index
    einnahmen_df.index = range(1, len(einnahmen_df) + 1)

    # Gesamtsumme anzeigen
    gesamt = einnahmen_df["betrag"].sum()
    st.metric("💵 Gesamteinnahmen", f"{gesamt:.2f} CHF")

    # Tabellenkopf
    header = st.columns([2, 2, 2, 3, 1])
    header[0].markdown("**Datum**")
    header[1].markdown("**Kategorie**")
    header[2].markdown("**Betrag**")
    header[3].markdown("**Beschreibung**")
    header[4].markdown("")

    # Tabellenzeilen mit 🗑️
    for idx, row in einnahmen_df.iterrows():
        cols = st.columns([2, 2, 2, 3, 1])
        cols[0].write(row["timestamp"].date())
        cols[1].write(row["kategorie"])
        cols[2].write(f"{row['betrag']:.2f} CHF")
        cols[3].write(row["beschreibung"] if row["beschreibung"] else "-")
        if cols[4].button("🗑️", key=f"delete_einnahme_{idx}"):
            st.session_state.data_df.drop(index=row["original_index"], inplace=True)
            DataManager().save_data("data_df")
            st.success("Einnahme gelöscht.")
            st.rerun()

    st.divider()

    # Alle Einnahmen löschen (für gewählten Monat)
    if st.button("❌ Alle Einnahmen für diesen Monat löschen"):
        indices_loeschen = einnahmen_df["original_index"].tolist()
        st.session_state.data_df.drop(index=indices_loeschen, inplace=True)
        DataManager().save_data("data_df")
        st.success("Alle Einnahmen für diesen Monat wurden gelöscht.")
        st.rerun()
else:
    st.info(f"Keine Einnahmen im Monat {ausgewaehlter_monat}.")
