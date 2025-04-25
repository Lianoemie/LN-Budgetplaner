import streamlit as st
import pandas as pd

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
# Berechnungen: aktueller Stand
# -----------------------------
gesamt_einnahmen = sum([e["Betrag (CHF)"] for e in st.session_state.einnahmen])
gesamt_ausgaben = sum([a["Betrag (CHF)"] for a in st.session_state.ausgaben])
gesamt_fixkosten = sum([f["Betrag (CHF)"] for f in st.session_state.fixkosten])

aktueller_stand = (
    st.session_state.monatliches_budget
    + gesamt_einnahmen
    - gesamt_fixkosten
    - gesamt_ausgaben
)

st.subheader("📊 Aktueller Stand")
st.metric("💰 Verfügbar", f"{aktueller_stand:.2f} CHF")
st.caption(f"(Fixkosten in Höhe von {gesamt_fixkosten:.2f} CHF wurden bereits berücksichtigt)")

# -----------------------------
# Letzte Ausgaben anzeigen
# -----------------------------
st.subheader("🧾 Übersicht letzte Ausgaben")

if st.session_state.ausgaben:
    df = pd.DataFrame(st.session_state.ausgaben)
    letzte = df.tail(5).iloc[::-1]  # letzte 5, neueste zuerst
    st.table(letzte[["Kategorie", "Betrag (CHF)", "Beschreibung"]])
else:
    st.info("Noch keine Ausgaben eingetragen.")

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

