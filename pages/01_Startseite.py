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
initial_df = pd.DataFrame(columns=["timestamp", "typ", "monat", "budget", "betrag", "beschreibung", "stoppdatum"])

DataManager().load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=initial_df,
    parse_dates=['timestamp', 'stoppdatum']
)

st.title("🏠 Startseite – Studibudget")

# -----------------------------
# Dynamisch aktuellen Monat vorauswählen
# -----------------------------
st.subheader("📅 Monat auswählen")

von_jahr = 2025
bis_jahr = 2026
alle_monate = [f"{jahr}-{monat:02d}" for jahr in range(von_jahr, bis_jahr + 1) for monat in range(1, 13)]
standard_monat = datetime.now().strftime("%Y-%m")

gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))
jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
monat_ende = datetime(jahr, monat, calendar.monthrange(jahr, monat)[1])

# -----------------------------
# Datengrundlage
# -----------------------------
data = st.session_state.get('data_df', initial_df)

# -----------------------------
# Fixkosten berechnen
# -----------------------------
if 'typ' in data.columns:
    fixkosten_df = data[data['typ'] == 'fixkosten'].copy()
else:
    fixkosten_df = pd.DataFrame()

if not fixkosten_df.empty:
    fixkosten_df["timestamp"] = pd.to_datetime(fixkosten_df["timestamp"], errors='coerce')
    fixkosten_df["stoppdatum"] = pd.to_datetime(fixkosten_df.get("stoppdatum"), errors='coerce')

    invalid_timestamps = fixkosten_df[fixkosten_df["timestamp"].isna()]
    if not invalid_timestamps.empty:
        st.warning("⚠️ Ungültige Zeitstempel in den Fixkosten gefunden (werden ignoriert):")
        st.write(invalid_timestamps)

    fixkosten_df = fixkosten_df[fixkosten_df["timestamp"].notna()]
    aktiv_fixkosten = fixkosten_df[
        (fixkosten_df["timestamp"] <= monat_ende) &
        (fixkosten_df["stoppdatum"].isna() | (fixkosten_df["stoppdatum"] >= monat_start))
    ]
    gesamt_fixkosten = aktiv_fixkosten["betrag"].sum()
else:
    gesamt_fixkosten = 0.0

# -----------------------------
# Einnahmen & Ausgaben berechnen
# -----------------------------
def berechne_summe(df, typ):
    if 'typ' not in df.columns or 'timestamp' not in df.columns or 'betrag' not in df.columns:
        return 0.0
    df_filtered = df[df['typ'] == typ].copy()
    df_filtered["timestamp"] = pd.to_datetime(df_filtered["timestamp"], errors='coerce')
    df_filtered = df_filtered[df_filtered["timestamp"].notna()]
    return df_filtered[
        (df_filtered["timestamp"] >= monat_start) &
        (df_filtered["timestamp"] <= monat_ende)
    ]["betrag"].sum()

gesamt_einnahmen = berechne_summe(data, 'einnahme')
gesamt_ausgaben = berechne_summe(data, 'ausgabe')
verfuegbar = gesamt_einnahmen - gesamt_fixkosten - gesamt_ausgaben

# -----------------------------
# Dynamisches Sparziel (%)
# -----------------------------
st.subheader("💶 Monatliches Budget & Sparen")

sparquote = st.slider("Wie viel % möchtest du sparen?", min_value=0, max_value=100, value=10, step=5)
sparbetrag = max(0.0, verfuegbar * (sparquote / 100))
budget_verfuegbar = max(0.0, verfuegbar - sparbetrag)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📈 Gesamteinnahmen", f"{gesamt_einnahmen:.2f} CHF")

with col2:
    st.metric("📉 Gesamtausgaben", f"{gesamt_ausgaben:.2f} CHF")

with col3:
    st.metric("📋 Fixkosten", f"{gesamt_fixkosten:.2f} CHF")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("💰 Total noch verfügbar", f"{verfuegbar:.2f} CHF")

with col5:
    st.metric("💡 Diesen Betrag spare ich", f"{sparbetrag:.2f} CHF")

with col6:
    st.metric("🛒 Dein Budget für diesen Monat", f"{budget_verfuegbar:.2f} CHF")

# -----------------------------
# Navigation (Buttons)
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Einmalige Ausgabe"):
        st.switch_page("pages/06_Ausgaben hinzufügen.py")

with col2:
    if st.button("📈 Statistik"):
        st.switch_page("pages/07_Statistik.py")

if st.button("💡 Spartipps"):
    st.switch_page("pages/08_Spartipps.py")

if st.button("👤 Mein Profil"):
    st.switch_page("pages/09_Mein Profil.py")
