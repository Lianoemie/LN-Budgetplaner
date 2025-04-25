import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Statistiken", page_icon="📊")
st.title("📊 Statistiken")

# ----------------------------------------
# Sicherstellen, dass Daten vorhanden sind
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

# Datum in datetime-Format umwandeln (nur wenn Spalte vorhanden)
if 'Datum' in df_einnahmen.columns:
    df_einnahmen['Datum'] = pd.to_datetime(df_einnahmen['Datum'], errors='coerce')
if 'Datum' in df_ausgaben.columns:
    df_ausgaben['Datum'] = pd.to_datetime(df_ausgaben['Datum'], errors='coerce')

# ----------------------------------------
# Monat-Auswahl vorbereiten
# ----------------------------------------
daten_quellen = []
if 'Datum' in df_einnahmen.columns:
    daten_quellen.append(df_einnahmen['Datum'])
if 'Datum' in df_ausgaben.columns:
    daten_quellen.append(df_ausgaben['Datum'])

if daten_quellen:
    alle_monate = pd.concat(daten_quellen).dropna()
    alle_monate = alle_monate.dt.to_period('M').sort_values().unique()
    alle_monate_str = [str(monat) for monat in alle_monate]
else:
    st.warning("Noch keine Einnahmen oder Ausgaben vorhanden.")
    st.stop()

aktueller_monat = datetime.now().strftime('%Y-%m')
ausgewaehlter_monat = st.selectbox(
    "Monat auswählen",
    options=alle_monate_str,
    index=alle_monate_str.index(aktueller_monat) if aktueller_monat in alle_monate_str else 0
)

# ----------------------------------------
# Monatsdaten filtern
# ----------------------------------------
monat_start = pd.to_datetime(ausgewaehlter_monat + "-01")
monat_ende = monat_start + pd.offsets.MonthEnd(0)

if 'Datum' in df_einnahmen.columns:
    df_einnahmen_monat = df_einnahmen[(df_einnahmen['Datum'] >= monat_start) & (df_einnahmen['Datum'] <= monat_ende)]
else:
    df_einnahmen_monat = pd.DataFrame()

if 'Datum' in df_ausgaben.columns:
    df_ausgaben_monat = df_ausgaben[(df_ausgaben['Datum'] >= monat_start) & (df_ausgaben['Datum'] <= monat_ende)]
else:
    df_ausgaben_monat = pd.DataFrame()

# ----------------------------------------
# Kuchendiagramm: Einnahmen
# ----------------------------------------
st.subheader(f"📥 Einnahmen im {ausgewaehlter_monat}")
if not df_einnahmen_monat.empty:
    gruppiert_einnahmen = df_einnahmen_monat.groupby("Kategorie")["Betrag (CHF)"].sum().reset_index()
    fig_e = px.pie(
        gruppiert_einnahmen,
        names="Kategorie",
        values="Betrag (CHF)",
        title="Einnahmen nach Kategorie",
        hole=0.4
    )
    st.plotly_chart(fig_e, use_container_width=True)

    st.dataframe(
        df_einnahmen_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']],
        use_container_width=True
    )
    st.metric("💵 Gesamteinnahmen", f"{df_einnahmen_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Einnahmen für diesen Monat.")

# ----------------------------------------
# Kuchendiagramm: Ausgaben
# ----------------------------------------
st.subheader(f"📤 Ausgaben im {ausgewaehlter_monat}")
if not df_ausgaben_monat.empty:
    gruppiert_ausgaben = df_ausgaben_monat.groupby("Kategorie")["Betrag (CHF)"].sum().reset_index()
    fig_a = px.pie(
        gruppiert_ausgaben,
        names="Kategorie",
        values="Betrag (CHF)",
        title="Ausgaben nach Kategorie",
        hole=0.4
    )
    st.plotly_chart(fig_a, use_container_width=True)

    st.dataframe(
        df_ausgaben_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']],
        use_container_width=True
    )
    st.metric("💸 Gesamtausgaben", f"{df_ausgaben_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Ausgaben für diesen Monat.")
