import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Statistiken", page_icon="📊")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 

# ====== End Login Block ======

st.title("📊 Statistiken")

# ----------------------------------------
# Sicherstellen, dass Daten vorhanden sind
# ----------------------------------------
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []
if 'fixkosten' not in st.session_state:
    st.session_state.fixkosten = []

# ----------------------------------------
# Daten vorbereiten
# ----------------------------------------
df_einnahmen = pd.DataFrame(st.session_state.einnahmen)
df_ausgaben = pd.DataFrame(st.session_state.ausgaben)
df_fixkosten = pd.DataFrame(st.session_state.fixkosten)

# Datum in datetime-Format umwandeln (nur wenn Spalte vorhanden)
for df in [df_einnahmen, df_ausgaben, df_fixkosten]:
    if 'Datum' in df.columns:
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')

# ----------------------------------------
# Monat-Auswahl vorbereiten
# ----------------------------------------
daten_quellen = []
for df in [df_einnahmen, df_ausgaben, df_fixkosten]:
    if 'Datum' in df.columns:
        daten_quellen.append(df['Datum'])

if daten_quellen:
    alle_monate = pd.concat(daten_quellen).dropna()
    alle_monate = alle_monate.dt.to_period('M').sort_values().unique()
    alle_monate_str = [str(monat) for monat in alle_monate]
else:
    st.warning("Noch keine Einnahmen oder Ausgaben/Fixkosten vorhanden.")
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

df_einnahmen_monat = df_einnahmen[(df_einnahmen['Datum'] >= monat_start) & (df_einnahmen['Datum'] <= monat_ende)] if 'Datum' in df_einnahmen.columns else pd.DataFrame()
df_ausgaben_monat = df_ausgaben[(df_ausgaben['Datum'] >= monat_start) & (df_ausgaben['Datum'] <= monat_ende)] if 'Datum' in df_ausgaben.columns else pd.DataFrame()
df_fixkosten_monat = df_fixkosten[(df_fixkosten['Datum'] >= monat_start) & (df_fixkosten['Datum'] <= monat_ende)] if 'Datum' in df_fixkosten.columns else pd.DataFrame()

# ----------------------------------------
# Kuchendiagramm: Einnahmen
# ----------------------------------------
st.subheader(f"📥 Einnahmen im {ausgewaehlter_monat}")
if not df_einnahmen_monat.empty:
    gruppiert_einnahmen = df_einnahmen_monat.groupby("Kategorie")["Betrag (CHF)"].sum().reset_index()
    
    fig_e = go.Figure(
        data=[go.Pie(
            labels=gruppiert_einnahmen["Kategorie"],
            values=gruppiert_einnahmen["Betrag (CHF)"],
            hole=0.4,
            textinfo="value+percent",
            insidetextorientation='radial'
        )]
    )
    fig_e.update_layout(title="Einnahmen nach Kategorie")
    st.plotly_chart(fig_e, use_container_width=True)

    st.dataframe(
        df_einnahmen_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']],
        use_container_width=True
    )
    st.metric("💵 Gesamteinnahmen", f"{df_einnahmen_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Einnahmen für diesen Monat.")

# ----------------------------------------
# Kuchendiagramm: Ausgaben (inkl. Fixkosten)
# ----------------------------------------
st.subheader(f"📤 Ausgaben (inkl. Fixkosten) im {ausgewaehlter_monat}")

# Fixkosten als "Fixkosten" markieren, falls keine Kategorie vorhanden
if not df_fixkosten_monat.empty:
    df_fixkosten_monat = df_fixkosten_monat.copy()
    df_fixkosten_monat['Kategorie'] = df_fixkosten_monat['Kategorie'].fillna('Fixkosten')

# Gesamtausgaben zusammenfassen
df_gesamtausgaben_monat = pd.concat([df_ausgaben_monat, df_fixkosten_monat], ignore_index=True)

if not df_gesamtausgaben_monat.empty:
    gruppiert_ausgaben = df_gesamtausgaben_monat.groupby("Kategorie")["Betrag (CHF)"].sum().reset_index()
    
    fig_a = go.Figure(
        data=[go.Pie(
            labels=gruppiert_ausgaben["Kategorie"],
            values=gruppiert_ausgaben["Betrag (CHF)"],
            hole=0.4,
            textinfo="value+percent",
            insidetextorientation='radial'
        )]
    )
    fig_a.update_layout(title="Ausgaben nach Kategorie (inkl. Fixkosten)")
    st.plotly_chart(fig_a, use_container_width=True)

    st.dataframe(
        df_gesamtausgaben_monat[['Datum', 'Kategorie', 'Betrag (CHF)', 'Beschreibung']],
        use_container_width=True
    )
    st.metric("💸 Gesamtausgaben (inkl. Fixkosten)", f"{df_gesamtausgaben_monat['Betrag (CHF)'].sum():.2f} CHF")
else:
    st.info("Keine Ausgaben/Fixkosten für diesen Monat.")
