import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Startseite", page_icon="🏠")

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
# Monat & Jahr-Auswahl
# -----------------------------
st.subheader("📅 Monat auswählen")

# Sammle alle relevanten Daten (aus Fixkosten, Einnahmen, Ausgaben)
alle_daten = []
for quelle in [st.session_state.fixkosten, st.session_state.einnahmen, st.session_state.ausgaben]:
    for eintrag in quelle:
        try:
            datum = datetime.strptime(eintrag["Datum"], "%Y-%m-%d")
            alle_daten.append(datum)
        except:
            continue

# Fallback: Heute anzeigen, falls keine Daten vorhanden
if not alle_daten:
    alle_daten = [datetime.today()]

# Monate extrahieren
alle_monate = sorted(list(set([d.strftime("%Y-%m") for d in alle_daten])))

# Aktueller Monat vorauswählen
heute = datetime.today().strftime("%Y-%m")
if heute not in alle_monate:
    alle_monate.append(heute)
alle_monate = sorted(alle_monate)

gewaehlter_monat = st.selectbox("Wähle einen Monat", alle_monate, index=alle_monate.index(heute))
jahr, monat = map(int, gewaehlter_monat.split("-"))

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
# Fixkosten filtern nach gewähltem Monat
# -----------------------------
fixkosten_monat = []

for eintrag in st.session_state.fixkosten:
    try:
        datum = datetime.strptime(eintrag["Datum"], "%Y-%m-%d")
        if datum.month == monat and datum.year == jahr:
            fixkosten_monat.append(eintrag)
    except:
        continue

# -----------------------------
# Berechnungen: aktueller Stand
# -----------------------------
gesamt_einnahmen = sum([e["Betrag (CHF)"] for e in st.session_state.einnahmen])
gesamt_ausgaben = sum([a["Betrag (CHF)"] for a in st.session_state.ausgaben])
gesamt_fixkosten = sum([f["Betrag (CHF)"] for f in fixkosten_monat])

aktueller_stand = (
    st.session_state.monatliches_budget
    + gesamt_einnahmen
    - gesamt_fixkosten
    - gesamt_ausgaben
)

st.subheader("📊 Finanzübersicht für", anchor=False)
st.metric("💰 Verfügbar", f"{aktueller_stand:.2f} CHF")
st.caption(f"(Fixkosten in Höhe von {gesamt_fixkosten:.2f} CHF für {gewaehlter_monat} berücksichtigt)")

# -----------------------------
# Letzte Ausgaben anzeigen
# -----------------------------
st.subheader("🧾 Übersicht letzte Ausgaben")

df_a = pd.DataFrame(st.session_state.ausgaben)
if not df_a.empty:
    df_a["Datum"] = pd.to_datetime(df_a["Datum"])
    df_a_monat = df_a[(df_a["Datum"].dt.month == monat) & (df_a["Datum"].dt.year == jahr)]
    if not df_a_monat.empty:
        df_a_monat = df_a_monat.sort_values("Datum", ascending=False).tail(5).iloc[::-1]
        df_a_monat.index = range(1, len(df_a_monat) + 1)
        st.table(df_a_monat[["Kategorie", "Betrag (CHF)", "Beschreibung", "Datum"]])
    else:
        st.info("Keine Ausgaben in diesem Monat.")
else:
    st.info("Noch keine Ausgaben eingetragen.")

# -----------------------------
# Letzte Einnahmen anzeigen
# -----------------------------
st.subheader("💵 Übersicht letzte Einnahmen")

df_e = pd.DataFrame(st.session_state.einnahmen)
if not df_e.empty:
    df_e["Datum"] = pd.to_datetime(df_e["Datum"])
    df_e_monat = df_e[(df_e["Datum"].dt.month == monat) & (df_e["Datum"].dt.year == jahr)]
    if not df_e_monat.empty:
        df_e_monat = df_e_monat.sort_values("Datum", ascending=False).tail(5).iloc[::-1]
        df_e_monat.index = range(1, len(df_e_monat) + 1)
        st.table(df_e_monat[["Kategorie", "Betrag (CHF)", "Beschreibung", "Datum"]])
    else:
        st.info("Keine Einnahmen in diesem Monat.")
else:
    st.info("Noch keine Einnahmen eingetragen.")

# -----------------------------
# Navigation (Buttons)
# -----------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Einmalige Ausgabe"):
        st.switch_page("pages/ausgaben.py")

with col2:
    if st.button("📈 Statistik"):
        st.switch_page("pages/statistik.py")

if st.button("💡 Spartipps"):
    st.switch_page("pages/spartipps.py")

if st.button("👤 Mein Profil"):
    st.switch_page("pages/profil.py")
