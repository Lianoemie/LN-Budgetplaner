import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ausgaben hinzufügen", page_icon="💸")

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

if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("💸 Ausgaben hinzufügen")

# ----------------------------------------
# 📅 Monat auswählen
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

alle_monate = data[data["typ"] == "ausgabe"]["timestamp"].dropna().dt.to_period("M").sort_values().unique()
alle_monate_str = [str(monat) for monat in alle_monate]

aktueller_monat = datetime.now().strftime("%Y-%m")
ausgewaehlter_monat = st.selectbox(
    "Monat auswählen",
    options=alle_monate_str if alle_monate_str else [aktueller_monat],
    index=alle_monate_str.index(aktueller_monat) if aktueller_monat in alle_monate_str else 0
)

# ----------------------------------------
# Neue Ausgabe direkt speichern
# ----------------------------------------
with st.form("ausgaben_formular"):
    st.subheader("Neue Ausgabe erfassen")
    kategorie = st.selectbox("Kategorie", st.session_state.kategorien_ausgaben)
    betrag = st.number_input("Betrag (CHF)", min_value=0.0, step=1.0, format="%.2f")
    beschreibung = st.text_input("Beschreibung (optional)")
    datum = st.date_input("Datum", value=datetime.today())
    abschicken = st.form_submit_button("Hinzufügen")

    if abschicken and betrag > 0:
        neue_ausgabe = {
            "typ": "ausgabe",
            "kategorie": kategorie,
            "betrag": betrag,
            "beschreibung": beschreibung,
            "timestamp": str(datum)
        }
        DataManager().append_record(
            session_state_key='data_df',
            record_dict=neue_ausgabe
        )
        st.success("Ausgabe gespeichert!")
        st.rerun()

# ----------------------------------------
# Übersicht der Ausgaben im gewählten Monat
# ----------------------------------------
ausgaben_df = data[
    (data['typ'] == 'ausgabe') & 
    (data['timestamp'].dt.to_period("M") == ausgewaehlter_monat)
].copy()

if not ausgaben_df.empty:
    st.subheader(f"📋 Ausgaben im Monat {ausgewaehlter_monat}")

    # Nach Datum sortieren (neueste zuerst)
    ausgaben_df = ausgaben_df.sort_values(by="timestamp", ascending=False)

    # Leere Beschreibungen durch Punkt ersetzen
    ausgaben_df["beschreibung"] = ausgaben_df["beschreibung"].fillna("-")

    # Originalindex merken für Löschen
    ausgaben_df["original_index"] = ausgaben_df.index
    ausgaben_df.index = range(1, len(ausgaben_df) + 1)

    # Gesamtsumme anzeigen
    gesamt = ausgaben_df["betrag"].sum()
    st.metric("💸 Gesamtausgaben", f"{gesamt:.2f} CHF")

    # Tabellenkopf
    header = st.columns([2, 2, 2, 3, 1])
    header[0].markdown("**Datum**")
    header[1].markdown("**Kategorie**")
    header[2].markdown("**Betrag**")
    header[3].markdown("**Beschreibung**")
    header[4].markdown("")

    # Zeilen mit 🗑️
    for idx, row in ausgaben_df.iterrows():
        cols = st.columns([2, 2, 2, 3, 1])
        cols[0].write(row["timestamp"].date())
        cols[1].write(row["kategorie"])
        cols[2].write(f"{row['betrag']:.2f} CHF")
        cols[3].write(row["beschreibung"] if row["beschreibung"] else "-")
        if cols[4].button("🗑️", key=f"delete_ausgabe_{idx}"):
            st.session_state.data_df.drop(index=row["original_index"], inplace=True)
            DataManager().save_data("data_df")
            st.success("Ausgabe gelöscht.")
            st.rerun()

    st.divider()

    # Alle Ausgaben des Monats löschen
    if st.button("❌ Alle Ausgaben für diesen Monat löschen"):
        indices_loeschen = ausgaben_df["original_index"].tolist()
        st.session_state.data_df.drop(index=indices_loeschen, inplace=True)
        DataManager().save_data("data_df")
        st.success("Alle Ausgaben für diesen Monat wurden gelöscht.")
        st.rerun()
else:
    st.info(f"Keine Ausgaben im Monat {ausgewaehlter_monat}.")
