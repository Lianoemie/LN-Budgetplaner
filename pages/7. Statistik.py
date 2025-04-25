import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Statistiken", page_icon="📊")

st.title("📊 Statistiken")

# ----------------------------------------
# Sicherstellen, dass Einnahmen und Ausgaben existieren
# ----------------------------------------
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []

# ----------------------------------------
# Daten vorbereiten
# ----------------------------------------
df_einnahmen = pd.DataFrame(st.session_state.einnahmen)
df_ausgaben = pd.DataFrame(st.session_state.ausgaben)

# Datum in datetime-Format umwandeln
if not df_einnahmen.empty:
    df_einnahmen['Datum'] = pd.to_datetime(df_einnahmen['Datum'])
if not df_ausgaben.empty:
    df_ausgaben['Datum'] = pd.to_datetime(df_ausgaben['Datum'])

# Alle vorhandenen Monate herausfiltern (für Dropdown)
alle_monate = pd.concat([df_einnahmen['Datum'], df_ausgaben['Datum']]).dropna()
alle_monate = alle_monate.dt.to_period('M').sort_values().unique()

# Aktuellen Monat ermitteln
aktueller_monat = datetime.now().strftime('%Y-%m')

# Auswahlbox für Monat
ausgewaehlter_monat = st.selectbox(
    "Monat auswählen",
    options=[str(monat) for monat in alle_monate],
    index=[str(monat) for monat in alle_monate].index(aktueller_monat) if aktueller_monat in [str(monat) for monat in alle_monate] else 0
)

# ----------------------------------------
# Daten für den ausgewählten Monat filtern
# ----------------------------------------
monat_start = pd.to_datetime(ausgewaehlter_monat + "-01")
monat_ende = (monat_start + pd.offsets.MonthEnd(1))

df_einnahmen_monat = df_einnahmen[(df_einnahmen['Datum'] >= monat_start) & (df_einnahmen['Datum'] <= monat_ende)]
df_ausgaben_monat = df_ausgaben[(df_ausgaben['Datum'] >= monat_start) & (df_ausgaben['Datum'] <= monat_ende)]

# ----------------------------------------
# Kuchendiagramm erstellen
# ----------------------------------------

st.subheader(f"Übersicht für {ausgewaehlter_monat}")

# Einnahmen-Daten für Kuchendiagramm
einnahmen_summen = df_einnahmen_monat.groupby('Kategorie')['Betrag (CHF)'].sum().reset_index()
einnahmen_summen['Typ'] = 'Einnahmen'

# Ausgaben-Daten für Kuchendiagramm
ausgaben_summen = df_ausgaben_monat.groupby('Kategorie')['Betrag (CHF)'].sum().reset_index()
ausgaben_summen['Typ'] = 'Ausgaben'

# Einnahmen und Ausgaben zusammenfügen
gesamt_summen = pd.concat([einnahmen_summen, ausgaben_summen])

if not gesamt_summen.empty:
    fig = px.pie(
        gesamt_summen,
        values='Betrag (CHF)',
        names='Kategorie',
        color='Typ',  # Einnahmen und Ausgaben bekommen verschiedene Farben
        hole=0.4,
        title="Verteilung Einnahmen und Ausgaben",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Keine Einnahmen oder Ausgaben für diesen Monat vorhanden.")

# ----------------------------------------
# Detailansicht Einnahmen
# ----------------------------------------
st.subheader("📥 Detailansicht Einnahmen")

if not df_einnahmen_monat.empty:
    st.dataframe(df_einnahmen_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']], use_container_width=True)
    st.metric("💵 Gesamteinnahmen", f"{df_einnahmen_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Einnahmen für diesen Monat.")

# ----------------------------------------
# Detailansicht Ausgaben
# ----------------------------------------
st.subheader("📤 Detailansicht Ausgaben")

if not df_ausgaben_monat.empty:
    st.dataframe(df_ausgaben_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']], use_container_width=True)
    st.metric("💸 Gesamtausgaben", f"{df_ausgaben_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Ausgaben für diesen Monat.")
