import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Statistik", page_icon="📈")
st.title("📈 Statistik nach Monat und Kategorie")

# -----------------------------
# Session-State vorbereiten
# -----------------------------
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

# Überprüfe, ob 'Datum' Spalte existiert und füge Dummy-Daten hinzu
st.session_state.einnahmen = check_and_convert_daten_liste(st.session_state.einnahmen)
st.session_state.ausgaben = check_and_convert_daten_liste(st.session_state.ausgaben)

# In DataFrames umwandeln
df_einnahmen = pd.DataFrame(st.session_state.einnahmen)
df_ausgaben = pd.DataFrame(st.session_state.ausgaben)

# Überprüfe, ob die 'Datum' Spalte existiert, bevor du sie umwandelst
if "Datum" in df_einnahmen.columns:
    df_einnahmen["Datum"] = pd.to_datetime(df_einnahmen["Datum"])
else:
    st.error("Die 'Datum' Spalte fehlt in den Einnahmen.")
    
if "Datum" in df_ausgaben.columns:
    df_ausgaben["Datum"] = pd.to_datetime(df_ausgaben["Datum"])
else:
    st.error("Die 'Datum' Spalte fehlt in den Ausgaben.")

# -----------------------------
# Monatsauswahl
# -----------------------------
alle_monate = pd.concat([df_einnahmen["Datum"], df_ausgaben["Datum"]]).dt.to_period("M").unique()
alle_monate_str = [str(monat) for monat in alle_monate]

if not alle_monate_str:
    st.info("Noch keine Daten mit Datum vorhanden.")
else:
    gewaehlter_monat = st.selectbox("🗕️ Monat auswählen", alle_monate_str)

    jahr, monat = map(int, gewaehlter_monat.split("-"))
    df_e_monat = df_einnahmen[(df_einnahmen["Datum"].dt.month == monat) & (df_einnahmen["Datum"].dt.year == jahr)]
    df_a_monat = df_ausgaben[(df_ausgaben["Datum"].dt.month == monat) & (df_ausgaben["Datum"].dt.year == jahr)]

# -----------------------------
# Einnahmen Kuchendiagramm
# -----------------------------
if not df_e_monat.empty:
    st.subheader("💰 Einnahmen nach Kategorie")
    einnahmen_kat = df_e_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
    total_einnahmen = einnahmen_kat.sum()

    cmap_einnahmen = plt.cm.get_cmap('tab10', len(einnahmen_kat))
    colors = [cmap_einnahmen(i) for i in range(len(einnahmen_kat))]

    fig1, ax1 = plt.subplots(figsize=(6, 6))
    wedges, texts = ax1.pie(
        einnahmen_kat,
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    ax1.axis('equal')
    ax1.legend(
        wedges,
        [f"{kategorie} – {betrag:,.2f} CHF" for kategorie, betrag in zip(einnahmen_kat.index, einnahmen_kat.values)],
        title="Kategorie",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig1)

    st.markdown("**💵 Einnahmen – Detailübersicht:**")
    df_e_detail = pd.DataFrame({
        "Kategorie": einnahmen_kat.index,
        "Betrag (CHF)": [f"{v:,.2f}".replace(",", "'") for v in einnahmen_kat.values],
        "Anteil (%)": [f"{(v / total_einnahmen * 100):.1f}%" for v in einnahmen_kat.values]
    })
    df_e_detail.index = np.arange(1, len(df_e_detail) + 1)  # Index startet bei 1
    st.table(df_e_detail)
else:
    st.info("Keine Einnahmen in diesem Monat.")

# -----------------------------
# Ausgaben Kuchendiagramm
# -----------------------------
if not df_a_monat.empty:
    st.subheader("💸 Ausgaben nach Kategorie")
    ausgaben_kat = df_a_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
    total_ausgaben = ausgaben_kat.sum()

    cmap_ausgaben = plt.cm.get_cmap('tab20', len(ausgaben_kat))
    colors = [cmap_ausgaben(i) for i in range(len(ausgaben_kat))]

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    wedges, texts = ax2.pie(
        ausgaben_kat,
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    ax2.axis('equal')
    ax2.legend(
        wedges,
        [f"{kategorie} – {betrag:,.2f} CHF" for kategorie, betrag in zip(ausgaben_kat.index, ausgaben_kat.values)],
        title="Kategorie",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig2)

    st.markdown("**💸 Ausgaben – Detailübersicht:**")
    df_a_detail = pd.DataFrame({
        "Kategorie": ausgaben_kat.index,
        "Betrag (CHF)": [f"{v:,.2f}".replace(",", "'") for v in ausgaben_kat.values],
        "Anteil (%)": [f"{(v / total_ausgaben * 100):.1f}%" for v in ausgaben_kat.values]
    })
    df_a_detail.index = np.arange(1, len(df_a_detail) + 1)  # Index startet bei 1
    st.table(df_a_detail)
else:
    st.info("Keine Ausgaben in diesem Monat.")

# -----------------------------
# Monatlicher Saldo
# -----------------------------
einnahmen_summe = df_e_monat["Betrag (CHF)"].sum()
ausgaben_summe = df_a_monat["Betrag (CHF)"].sum()
saldo = einnahmen_summe - ausgaben_summe

st.subheader("📊 Monatlicher Saldo")
st.metric(label="Einnahmen – Ausgaben", value=f"{saldo:,.2f} CHF".replace(",", "'"))
