# ======================================
# 📦 Imports & Konfiguration
# ======================================
import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Startseite", page_icon="🏠")

from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py')

# ======================================
# 📂 Daten laden & vorbereiten
# ======================================
initial_df = pd.DataFrame(columns=["timestamp", "typ", "monat", "budget", "betrag", "beschreibung", "stoppdatum"])
dm = DataManager()
dm.load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=initial_df,
    parse_dates=['timestamp', 'stoppdatum']
)
data = st.session_state.get('data_df', initial_df)

# ======================================
# 🧠 Hilfsfunktionen
# ======================================
def berechne_summe(df: pd.DataFrame, typ: str, start: datetime, ende: datetime) -> float:
    if 'typ' not in df.columns or 'timestamp' not in df.columns or 'betrag' not in df.columns:
        return 0.0
    df_filtered = df[(df['typ'] == typ)].copy()
    df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'], errors='coerce')
    df_filtered = df_filtered[df_filtered['timestamp'].notna()]
    return df_filtered[(df_filtered['timestamp'] >= start) & (df_filtered['timestamp'] <= ende)]["betrag"].sum()

def hole_budget(df: pd.DataFrame, monat: str) -> float:
    if all(col in df.columns for col in ["typ", "monat", "budget"]):
        budget_df = df[(df["typ"] == "budget") & (df["monat"] == monat)]
        if not budget_df.empty:
            return float(budget_df["budget"].iloc[0])
    return 0.0

def zeige_fixkosten(df: pd.DataFrame, start: datetime, ende: datetime) -> float:
    if "typ" not in df.columns or "timestamp" not in df.columns:
        return 0.0
    df = df[df["typ"] == "fixkosten"].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df["stoppdatum"] = pd.to_datetime(df.get("stoppdatum"), errors='coerce')

    df = df[df["timestamp"].notna()]
    aktiv = df[(df["timestamp"] <= ende) & (df["stoppdatum"].isna() | (df["stoppdatum"] >= start))]
    return aktiv["betrag"].sum()

# ======================================
# 📅 Monatsauswahl
# ======================================
st.title("🏠 Startseite – Studibudget")
st.subheader("📅 Monat auswählen")

alle_monate = [f"{jahr}-{monat:02d}" for jahr in range(2025, 2027) for monat in range(1, 13)]
standard_monat = "2025-01"
gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))
jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
monat_ende = datetime(jahr, monat, calendar.monthrange(jahr, monat)[1])

# ======================================
# 💶 Budget bearbeiten
# ======================================
st.subheader("💶 Monatliches Budget")
aktuelles_budget = hole_budget(data, gewaehlter_monat)
st.session_state.monatliches_budget = st.number_input(
    "Budget für den Monat (CHF)", min_value=0.0, value=aktuelles_budget, step=50.0, format="%.2f"
)

if st.button("💾 Budget speichern"):
    neues_budget = {
        "typ": "budget",
        "monat": gewaehlter_monat,
        "budget": st.session_state.monatliches_budget,
        "timestamp": str(ch_now())
    }
    # Alte Einträge entfernen
    st.session_state.data_df = data[~((data['typ'] == 'budget') & (data['monat'] == gewaehlter_monat))]
    dm.append_record('data_df', neues_budget)
    st.success("Budget gespeichert!")
    st.rerun()

# ======================================
# 📋 Fixkosten berechnen
# ======================================
fixkosten = zeige_fixkosten(data, monat_start, monat_ende)
st.metric("📋 Fixkosten im gewählten Monat", f"{fixkosten:.2f} CHF")

# ======================================
# 📈 Einnahmen & Ausgaben
# ======================================
einnahmen = berechne_summe(data, 'einnahme', monat_start, monat_ende)
ausgaben = berechne_summe(data, 'ausgabe', monat_start, monat_ende)

col1, col2 = st.columns(2)
with col1:
    st.metric("📈 Gesamteinnahmen", f"{einnahmen:.2f} CHF")
with col2:
    st.metric("📉 Gesamtausgaben", f"{ausgaben:.2f} CHF")

# ======================================
# 🚀 Navigation
# ======================================
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Einmalige Ausgabe"):
        st.switch_page("06_Ausgaben_hinzufügen")
with col2:
    if st.button("📈 Statistik"):
        st.switch_page("07_Statistik")

if st.button("💡 Spartipps"):
    st.switch_page("08_Spartipps")

if st.button("👤 Mein Profil"):
    st.switch_page("09_Mein_Profil")
