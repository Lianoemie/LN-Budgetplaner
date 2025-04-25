import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Statistik", page_icon="📈")
st.title("📈 Statistik nach Monat und Kategorie")

# Session-State vorbereiten
if 'einnahmen' not in st.session_state:
    st.session_state.einnahmen = []
if 'ausgaben' not in st.session_state:
    st.session_state.ausgaben = []

# Dummy-Datum einfügen, falls noch nicht vorhanden
def check_and_convert_daten_liste(liste):
    for eintrag in liste:
        if "Datum" not in eintrag:
            eintrag["Datum"] = datetime.today().strftime("%Y-%m-%d")
    return liste

st.session_state.einnahmen = check_and_convert_daten_liste(st.session_state.einnahmen)
st.session_state.ausgaben = check_and_convert_daten_liste(st.session_state.ausgaben)

# In DataFrames umwandeln
df_einnahmen = pd.DataFrame(st.session_state.einnahmen)
df_ausgaben = pd.DataFrame(st.session_state.ausgaben)

# Datum in datetime-Format umwandeln
df_einnahmen["Datum"] = pd.to_datetime(df_einnahmen["Datum"])
df_ausgaben["Datum"] = pd.to_datetime(df_ausgaben["Datum"])

# Monatsauswahl
alle_monate = pd.concat([df_einnahmen["Datum"], df_ausgaben["Datum"]]).dt.to_period("M").unique()
alle_monate_str = [str(monat) for monat in alle_monate]

if not alle_monate_str:
    st.info("Noch keine Daten mit Datum vorhanden.")
else:
    gewaehlter_monat = st.selectbox("📅 Monat auswählen", alle_monate_str)

    # Filter nach Monat
    jahr, monat = map(int, gewaehlter_monat.split("-"))
    df_e_monat = df_einnahmen[(df_einnahmen["Datum"].dt.month == monat) & (df_einnahmen["Datum"].dt.year == jahr)]
    df_a_monat = df_ausgaben[(df_ausgaben["Datum"].dt.month == monat) & (df_ausgaben["Datum"].dt.year == jahr)]

    # Kuchendiagramm Einnahmen
    if not df_e_monat.empty:
        st.subheader("💰 Einnahmen nach Kategorie")
        einnahmen_kat = df_e_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(einnahmen_kat, labels=einnahmen_kat.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
    else:
        st.info("Keine Einnahmen in diesem Monat.")

    # Kuchendiagramm Ausgaben
    if not df_a_monat.empty:
        st.subheader("💸 Ausgaben nach Kategorie")
        ausgaben_kat = df_a_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(ausgaben_kat, labels=ausgaben_kat.index, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)
    else:
        st.info("Keine Ausgaben in diesem Monat.")

    # Saldo
    einnahmen_summe = df_e_monat["Betrag (CHF)"].sum()
    ausgaben_summe = df_a_monat["Betrag (CHF)"].sum()
    saldo = einnahmen_summe - ausgaben_summe

    st.subheader("📊 Monatlicher Saldo")
    st.metric(label="Einnahmen – Ausgaben", value=f"{saldo:.2f} CHF")

