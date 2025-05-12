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
standard_monat = "2025-01"

gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))
jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
monat_ende = datetime(jahr, monat, calendar.monthrange(jahr, monat)[1])

# -----------------------------
# Budget setzen
# -----------------------------
st.subheader("💶 Monatliches Budget")

data = st.session_state.get('data_df', pd.DataFrame())
budget_df = data[(data['typ'] == 'budget') & (data['monat'] == gewaehlter_monat)]

aktuelles_budget = float(budget_df['budget'].iloc[0]) if not budget_df.empty else 0.0

with st.form("budget_formular"):
    budget = st.number_input(
        "Budget für den Monat (CHF)", 
        min_value=0.0, 
        value=aktuelles_budget, 
        step=50.0, 
        format="%.2f"
    )
    speichern = st.form_submit_button("💾 Budget speichern")
    if speichern:
        neues_budget = {
            "typ": "budget",
            "monat": gewaehlter_monat,
            "budget": budget,
            "timestamp": str(ch_now())
        }
        # Entferne bestehendes Budget für den Monat, bevor ein neues hinzugefügt wird
        st.session_state.data_df = data[data[['typ', 'monat']].ne(['budget', gewaehlter_monat]).any(1)]
        DataManager().append_record('data_df', neues_budget)
        st.success("Budget gespeichert!")
        st.rerun()

# -----------------------------
# Fixkosten für den Monat berechnen
# -----------------------------
fixkosten_df = data[data['typ'] == 'fixkosten'].copy()

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
# Einnahmen & Ausgaben im Monat berechnen
# -----------------------------
einnahmen_df = data[data['typ'] == 'einnahme'].copy()
ausgaben_df = data[data['typ'] == 'ausgabe'].copy()

def filter_monat(df):
    if df.empty:
        return 0.0
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df[(df["timestamp"] >= monat_start) & (df["timestamp"] <= monat_ende)]["betrag"].sum()

gesamt_einnahmen = filter_monat(einnahmen_df)
gesamt_ausgaben = filter_monat(ausgaben_df)

col1, col2 = st.columns(2)
with col1:
    st.metric("📈 Gesamteinnahmen", f"{gesamt_einnahmen:.2f} CHF")
with col2:
    st.metric("📉 Gesamtausgaben", f"{gesamt_ausgaben:.2f} CHF")

# -----------------------------
# Budget-Übersicht
# -----------------------------
verfügbares_budget = budget - gesamt_fixkosten - gesamt_ausgaben + gesamt_einnahmen
st.subheader("📊 Budgetübersicht")
st.metric("💰 Verfügbares Budget", f"{verfügbares_budget:.2f} CHF")
