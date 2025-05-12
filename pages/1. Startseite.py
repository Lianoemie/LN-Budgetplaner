import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Startseite", page_icon="🏠")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 

# ====== App-Daten laden ======
DataManager().load_app_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

st.title("🏠 Startseite – Studibudget")

# -----------------------------
# Monat auswählen
# -----------------------------
st.subheader("📅 Monat auswählen")

von_jahr = 2025
bis_jahr = 2026
alle_monate = [f"{jahr}-{monat:02d}" for jahr in range(von_jahr, bis_jahr + 1) for monat in range(1, 13)]

standard_monat = f"{datetime.today().year}-{datetime.today().month:02d}"
alle_monate = sorted(set(alle_monate + [standard_monat]))
gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))

jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
letzter_tag = calendar.monthrange(jahr, monat)[1]
monat_ende = datetime(jahr, monat, letzter_tag)

# -----------------------------
# Daten vorbereiten
# -----------------------------
data = st.session_state.get("data_df", pd.DataFrame())
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Einnahmen
einnahmen_df = data[data["typ"] == "einnahme"]
einnahmen_monat = einnahmen_df[
    (einnahmen_df["timestamp"] >= monat_start) & (einnahmen_df["timestamp"] <= monat_ende)
]
gesamt_einnahmen = einnahmen_monat["betrag"].sum()

# Ausgaben
ausgaben_df = data[data["typ"] == "ausgabe"]
ausgaben_monat = ausgaben_df[
    (ausgaben_df["timestamp"] >= monat_start) & (ausgaben_df["timestamp"] <= monat_ende)
]
gesamt_ausgaben = ausgaben_monat["betrag"].sum()

# Fixkosten
fixkosten_df = data[data["typ"] == "fixkosten"].copy()
fixkosten_df["datum"] = pd.to_datetime(fixkosten_df["timestamp"])
fixkosten_df["stoppdatum"] = pd.to_datetime(fixkosten_df["stoppdatum"], errors="coerce")

fixkosten_monat = fixkosten_df[
    (fixkosten_df["datum"] <= monat_ende) &
    ((fixkosten_df["stoppdatum"].isna()) | (fixkosten_df["stoppdatum"] >= monat_start))
]
gesamt_fixkosten = fixkosten_monat["betrag"].sum()

# -----------------------------
# Monatliches Budget (speicherbar)
# -----------------------------
st.subheader("💶 Monatliches Budget")
budgets = data[data["typ"] == "budget"]
aktuelles_budget_row = budgets[budgets["monat"] == gewaehlter_monat]

vorgabe = aktuelles_budget_row["budget"].iloc[0] if not aktuelles_budget_row.empty else 0.0
neues_budget = st.number_input("Budget für den Monat (CHF)", min_value=0.0, value=vorgabe, step=50.0, format="%.2f")

if st.button("💾 Budget speichern"):
    # Budget als separaten typ speichern
    neues_record = {
        "typ": "budget",
        "monat": gewaehlter_monat,
        "budget": neues_budget,
        "timestamp": str(datetime.today().date())
    }
    # Alte Zeile ggf. entfernen
    st.session_state.data_df = st.session_state.data_df[
        ~((st.session_state.data_df["typ"] == "budget") & (st.session_state.data_df["monat"] == gewaehlter_monat))
    ]
    DataManager().append_record("data_df", neues_record)
    st.success("Budget gespeichert.")
    st.rerun()

# -----------------------------
# Übersicht
# -----------------------------
aktueller_stand = neues_budget + gesamt_einnahmen - gesamt_fixkosten - gesamt_ausgaben

st.subheader(f"📊 Finanzübersicht für {gewaehlter_monat}")
st.metric("💰 Verfügbar", f"{aktueller_stand:.2f} CHF")
st.caption(f"(Fixkosten in Höhe von {gesamt_fixkosten:.2f} CHF berücksichtigt)")

# -----------------------------
# Letzte Ausgaben anzeigen
# -----------------------------
st.subheader("🧾 Übersicht letzte Ausgaben")
if not ausgaben_monat.empty:
    df = ausgaben_monat.sort_values("timestamp", ascending=False).tail(5).iloc[::-1]
    df.index = range(1, len(df) + 1)
    df = df.rename(columns={"kategorie": "Kategorie", "betrag": "Betrag", "beschreibung": "Beschreibung", "timestamp": "Datum"})
    st.table(df[["Kategorie", "Betrag", "Beschreibung", "Datum"]])
else:
    st.info("Keine Ausgaben in diesem Monat.")

# -----------------------------
# Letzte Einnahmen anzeigen
# -----------------------------
st.subheader("💵 Übersicht letzte Einnahmen")
if not einnahmen_monat.empty:
    df = einnahmen_monat.sort_values("timestamp", ascending=False).tail(5).iloc[::-1]
    df.index = range(1, len(df) + 1)
    df = df.rename(columns={"kategorie": "Kategorie", "betrag": "Betrag", "beschreibung": "Beschreibung", "timestamp": "Datum"})
    st.table(df[["Kategorie", "Betrag", "Beschreibung", "Datum"]])
else:
    st.info("Keine Einnahmen in diesem Monat.")

# -----------------------------
# Navigation
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Einmalige Ausgabe"):
        st.switch_page("6. Ausgaben hinzufügen")

with col2:
    if st.button("📈 Statistik"):
        st.switch_page("7. Statistik")

if st.button("💡 Spartipps"):
    st.switch_page("8. Spartipps")

if st.button("👤 Mein Profil"):
    st.switch_page("9. Mein Profil")
