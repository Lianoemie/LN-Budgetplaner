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
# Session-State initialisieren
# -----------------------------
if 'monatliches_budget' not in st.session_state:
    st.session_state.monatliches_budget = 0.0

# -----------------------------
# Feste Monatsauswahl (ab Jan 2025)
# -----------------------------
st.subheader("📅 Monat auswählen")

von_jahr = 2025
bis_jahr = 2026
alle_monate = [f"{jahr}-{monat:02d}" for jahr in range(von_jahr, bis_jahr + 1) for monat in range(1, 13)]
standard_monat = "2025-01"

gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))
jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
monat_ende = datetime(jahr, monat, calendar.monthrange(jahr, monat)[1])

# -----------------------------
# Monatliches Budget eingeben
# -----------------------------
st.subheader("💶 Monatliches Budget")

data = st.session_state.get('data_df', pd.DataFrame())
budget_df = data[(data['typ'] == 'budget') & (data['monat'] == gewaehlter_monat)]

aktuelles_budget = float(budget_df['budget'].iloc[0]) if not budget_df.empty else 0.0
st.session_state.monatliches_budget = aktuelles_budget

st.session_state.monatliches_budget = st.number_input(
    "Budget für den Monat (CHF)",
    min_value=0.0,
    value=st.session_state.monatliches_budget,
    step=50.0,
    format="%.2f"
)

if st.button("💾 Budget speichern"):
    neues_budget = {
        "typ": "budget",
        "monat": gewaehlter_monat,
        "budget": st.session_state.monatliches_budget,
        "timestamp": str(ch_now())
    }
    st.session_state.data_df = data[~((data['typ'] == 'budget') & (data['monat'] == gewaehlter_monat))]
    DataManager().append_record('data_df', neues_budget)
    st.success("Budget gespeichert!")
    st.rerun()


# -----------------------------
# Fixkosten filtern
# -----------------------------
if 'typ' in data.columns:
    fixkosten_df = data[data['typ'] == 'fixkosten'].copy()
else:
    fixkosten_df = pd.DataFrame()

if not fixkosten_df.empty:
    fixkosten_df["timestamp"] = pd.to_datetime(fixkosten_df["timestamp"])
    fixkosten_df["stoppdatum"] = pd.to_datetime(fixkosten_df["stoppdatum"], errors='coerce')

    aktiv_fixkosten = fixkosten_df[
        (fixkosten_df["timestamp"] <= monat_ende) &
        (fixkosten_df["stoppdatum"].isna() | (fixkosten_df["stoppdatum"] >= monat_start))
    ]
    gesamt_fixkosten = aktiv_fixkosten["betrag"].sum()
else:
    gesamt_fixkosten = 0.0

st.metric("📋 Fixkosten im gewählten Monat", f"{gesamt_fixkosten:.2f} CHF")

# -----------------------------
# Einnahmen & Ausgaben filtern
# -----------------------------
def berechne_summe(df, typ):
    if 'typ' not in df.columns:
        return 0.0
    df_filtered = df[df['typ'] == typ].copy()
    if df_filtered.empty:
        return 0.0
    df_filtered["timestamp"] = pd.to_datetime(df_filtered["timestamp"])
    return df_filtered[
        (df_filtered["timestamp"] >= monat_start) &
        (df_filtered["timestamp"] <= monat_ende)
    ]["betrag"].sum()

gesamt_einnahmen = berechne_summe(data, 'einnahme')
gesamt_ausgaben = berechne_summe(data, 'ausgabe')

col1, col2 = st.columns(2)
with col1:
    st.metric("📈 Gesamteinnahmen", f"{gesamt_einnahmen:.2f} CHF")
with col2:
    st.metric("📉 Gesamtausgaben", f"{gesamt_ausgaben:.2f} CHF")

# -----------------------------
# Navigation (Buttons)
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Einmalige Ausgabe"):
        st.switch_page("6_Ausgaben_hinzufügen")

with col2:
    if st.button("📈 Statistik"):
        st.switch_page("7_Statistik")

if st.button("💡 Spartipps"):
    st.switch_page("8_Spartipps")

if st.button("👤 Mein Profil"):
    st.switch_page("9_Mein_Profil.")
