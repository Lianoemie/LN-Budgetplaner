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
if not data.empty:
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

# Einnahmen
einnahmen_df = data[data["typ"] == "einnahme"] if not data.empty else pd.DataFrame()
einnahmen_monat = einnahmen_df[
    (einnahmen_df["timestamp"] >= monat_start) & (einnahmen_df["timestamp"] <= monat_ende)
] if not einnahmen_df.empty else pd.DataFrame()
gesamt_einnahmen = einnahmen_monat["betrag"].sum() if "betrag" in einnahmen_monat.columns else 0.0

# Ausgaben
ausgaben_df = data[data["typ"] == "ausgabe"] if not data.empty else pd.DataFrame()
ausgaben_monat = ausgaben_df[
    (ausgaben_df["timestamp"] >= monat_start) & (ausgaben_df["timestamp"] <= monat_ende)
] if not ausgaben_df.empty else pd.DataFrame()
gesamt_ausgaben = ausgaben_monat["betrag"].sum() if "betrag" in ausgaben_monat.columns else 0.0

# Fixkosten
fixkosten_df = data[data["typ"] == "fixkosten"].copy() if not data.empty else pd.DataFrame()
if not fixkosten_df.empty:
    fixkosten_df["datum"] = pd.to_datetime(fixkosten_df["timestamp"], errors="coerce")
    fixkosten_df["stoppdatum"] = pd.to_datetime(fixkosten_df.get("stoppdatum"), errors="coerce")
    fixkosten_monat = fixkosten_df[
        (fixkosten_df["datum"] <= monat_ende) &
        ((fixkosten_df["stoppdatum"].isna()) | (fixkosten_df["stoppdatum"] >= monat_start))
    ]
    gesamt_fixkosten = fixkosten_monat["betrag"].sum() if "betrag" in fixkosten_monat.columns else 0.0
else:
    gesamt_fixkosten = 0.0

# -----------------------------
# Monatliches Budget
# -----------------------------
st.subheader("💶 Monatliches Budget")
budgets = data[data["typ"] == "budget"] if not data.empty else pd.DataFrame()
aktuelles_budget_row = budgets[budgets["monat"] == gewaehlter_monat] if not budgets.empty else pd.DataFrame()
vorgabe = aktuelles_budget_row["budget"].iloc[0] if not aktuelles_budget_row.empty else 0.0
neues_budget = st.number_input("Budget für den Monat (CHF)", min_value=0.0, value=vorgabe, step=50.0, format="%.2f")

if st.button("💾 Budget speichern"):
    neues_record = {
        "typ": "budget",
        "monat": gewaehlter_monat,
        "budget": neues_budget,
        "timestamp": str(datetime.today().date())
    }
    st.session_state.data_df = st.session_state.data_df[
        ~((st.session_state.data_df["typ"] == "budget") & (st.session_state.data_df["monat"] == gewaehlter_monat))
    ]
    DataManager().append_record("data_df", neues_record)
    st.success("Budget gespeichert.")
    st.rerun()

# -----------------------------
# Finanzübersicht
# -----------------------------
aktueller_stand = neues_budget + gesamt_einnahmen - gesamt_fixkosten - gesamt_ausgaben
st.subheader(f"📊 Finanzübersicht für {gewaehlter_monat}")
st.metric("💰 Verfügbar", f"{aktueller_stand:.2f} CHF")
st.caption(f"(Fixkosten in Höhe von {gesamt_fixkosten:.2f} CHF berücksichtigt)")

# -----------------------------
# Hilfsfunktion für sichere Tabellenanzeige
# -----------------------------
def sichere_tabelle(df, title):
    st.subheader(title)
    if not df.empty:
        required_columns = ["kategorie", "betrag", "beschreibung", "timestamp"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = ""
        df = df.rename(columns={
            "kategorie": "Kategorie",
            "betrag": "Betrag",
            "beschreibung": "Beschreibung",
            "timestamp": "Datum"
        })
        df["Beschreibung"] = df["Beschreibung"].fillna("-")
        df["Betrag"] = pd.to_numeric(df["Betrag"], errors="coerce").fillna(0.0).round(2)
        df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce").dt.date.fillna("-")
        df = df.sort_values("Datum", ascending=False).tail(5).iloc[::-1]
        df.index = range(1, len(df) + 1)
        st.table(df[["Kategorie", "Betrag", "Beschreibung", "Datum"]])
    else:
        st.info("Keine Daten in diesem Monat.")

# -----------------------------
# Letzte Ausgaben und Einnahmen anzeigen
# -----------------------------
sichere_tabelle(ausgaben_monat, "🧾 Übersicht letzte Ausgaben")
sichere_tabelle(einnahmen_monat, "💵 Übersicht letzte Einnahmen")

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
