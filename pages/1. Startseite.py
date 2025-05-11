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

# ====== End Login Block ======

st.title("🏠 Startseite – Studibudget")

# -----------------------------
# Session-State initialisieren
# -----------------------------
if 'monatliches_budget' not in st.session_state:
    st.session_state.monatliches_budget = 0.0
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'fixkosten' not in st.session_state:
    st.session_state.fixkosten = []

# -----------------------------
# Feste Monatsauswahl (ab Jan 2025)
# -----------------------------
st.subheader("📅 Monat auswählen")

von_jahr = 2025
bis_jahr = 2026
alle_monate = [f"{jahr}-{monat:02d}" for jahr in range(von_jahr, bis_jahr + 1) for monat in range(1, 13)]

standard_monat = "2025-01"
if standard_monat not in alle_monate:
    alle_monate.append(standard_monat)
alle_monate = sorted(alle_monate)

gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(standard_monat))
jahr, monat = map(int, gewaehlter_monat.split("-"))
monat_start = datetime(jahr, monat, 1)
letzter_tag = calendar.monthrange(jahr, monat)[1]
monat_ende = datetime(jahr, monat, letzter_tag)

# -----------------------------
# Monatliches Budget eingeben
# -----------------------------
st.subheader("💶 Monatliches Budget")
st.session_state.monatliches_budget = st.number_input(
    "Budget für den Monat (CHF)",
    min_value=0.0,
    value=st.session_state.monatliches_budget,
    step=50.0,
    format="%.2f"
)

# -----------------------------
# Fixkosten filtern (Start- und Enddatum prüfen)
# -----------------------------
fixkosten_monat = []
for eintrag in st.session_state.fixkosten:
    try:
        startdatum = datetime.strptime(eintrag["Datum"], "%Y-%m-%d")
        stoppdatum = datetime.strptime(eintrag["Stoppdatum"], "%Y-%m-%d") if eintrag["Stoppdatum"] else None

        if startdatum <= monat_ende and (stoppdatum is None or monat_start <= stoppdatum):
            fixkosten_monat.append(eintrag)
    except:
        continue
gesamt_fixkosten = sum([f["Betrag (CHF)"] for f in fixkosten_monat])

# -----------------------------
# Einnahmen & Ausgaben filtern
# -----------------------------
gesamt_einnahmen = 0
gesamt_ausgaben = 0

df_e = pd.DataFrame(st.session_state.einnahmen)
if not df_e.empty:
    df_e["Datum"] = pd.to_datetime(df_e["Datum"])
    df_e_monat = df_e[(df_e["Datum"].dt.month == monat) & (df_e["Datum"].dt.year == jahr)]
    gesamt_einnahmen = df_e_monat["Betrag (CHF)"].sum()
else:
    df_e_monat = pd.DataFrame()

df_a = pd.DataFrame(st.session_state.ausgaben)
if not df_a.empty:
    df_a["Datum"] = pd.to_datetime(df_a["Datum"])
    df_a_monat = df_a[(df_a["Datum"].dt.month == monat) & (df_a["Datum"].dt.year == jahr)]
    gesamt_ausgaben = df_a_monat["Betrag (CHF)"].sum()
else:
    df_a_monat = pd.DataFrame()

# -----------------------------
# Aktueller Stand berechnen
# -----------------------------
aktueller_stand = (
    st.session_state.monatliches_budget
    + gesamt_einnahmen
    - gesamt_fixkosten
    - gesamt_ausgaben
)

st.subheader(f"📊 Finanzübersicht für {gewaehlter_monat}")
st.metric("💰 Verfügbar", f"{aktueller_stand:.2f} CHF")
st.caption(f"(Fixkosten in Höhe von {gesamt_fixkosten:.2f} CHF für {gewaehlter_monat} berücksichtigt)")

# -----------------------------
# Letzte Ausgaben anzeigen
# -----------------------------
st.subheader("🧾 Übersicht letzte Ausgaben")

if not df_a_monat.empty:
    letzte_ausgaben = df_a_monat.sort_values("Datum", ascending=False).tail(5).iloc[::-1]
    letzte_ausgaben.index = range(1, len(letzte_ausgaben) + 1)
    st.table(letzte_ausgaben[["Kategorie", "Betrag (CHF)", "Beschreibung", "Datum"]])
else:
    st.info("Keine Ausgaben in diesem Monat.")

# -----------------------------
# Letzte Einnahmen anzeigen
# -----------------------------
st.subheader("💵 Übersicht letzte Einnahmen")

if not df_e_monat.empty:
    letzte_einnahmen = df_e_monat.sort_values("Datum", ascending=False).tail(5).iloc[::-1]
    letzte_einnahmen.index = range(1, len(letzte_einnahmen) + 1)
    st.table(letzte_einnahmen[["Kategorie", "Betrag (CHF)", "Beschreibung", "Datum"]])
else:
    st.info("Keine Einnahmen in diesem Monat.")

    # -----------------------------
    # Seitenwechsel-Logik
    # -----------------------------
    if "page" not in st.session_state:
        st.session_state.page = "1. Startseite"

    if st.session_state.page == "6. Ausgaben hinzufügen":
        st.experimental_set_query_params(page="6. Ausgaben hinzufügen")
        st.experimental_rerun()

    if st.session_state.page == "7. Statistik":
        st.experimental_set_query_params(page="7. Statistik")
        st.experimental_rerun()

    if st.session_state.page == "8. Spartipps":
        st.experimental_set_query_params(page="8. Spartipps")
        st.experimental_rerun()

    if st.session_state.page == "9. Mein Profil":
        st.experimental_set_query_params(page="9. Mein Profil")
        st.experimental_rerun()