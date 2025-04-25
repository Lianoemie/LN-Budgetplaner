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

st.session_state.einnahmen = check_and_convert_daten_liste(st.session_state.einnahmen)
st.session_state.ausgaben = check_and_convert_daten_liste(st.session_state.ausgaben)

# In DataFrames umwandeln
df_einnahmen = pd.DataFrame(st.session_state.einnahmen)
df_ausgaben = pd.DataFrame(st.session_state.ausgaben)

# Datum umwandeln
df_einnahmen["Datum"] = pd.to_datetime(df_einnahmen["Datum"])
df_ausgaben["Datum"] = pd.to_datetime(df_ausgaben["Datum"])

# -----------------------------
# Monatsauswahl
# -----------------------------
alle_monate = pd.concat([df_einnahmen["Datum"], df_ausgaben["Datum"]]).dt.to_period("M").unique()
alle_monate_str = [str(monat) for monat in alle_monate]

if not alle_monate_str:
    st.info("Noch keine Daten mit Datum vorhanden.")
else:
    gewaehlter_monat = st.selectbox("📅 Monat auswählen", alle_monate_str)

    jahr, monat = map(int, gewaehlter_monat.split("-"))
    df_e_monat = df_einnahmen[(df_einnahmen["Datum"].dt.month == monat) & (df_einnahmen["Datum"].dt.year == jahr)]
    df_a_monat = df_ausgaben[(df_ausgaben["Datum"].dt.month == monat) & (df_ausgaben["Datum"].dt.year == jahr)]

    # -----------------------------
    # Einnahmen Kuchendiagramm mit farbigen Labels
    # -----------------------------
    if not df_e_monat.empty:
        st.subheader("💰 Einnahmen nach Kategorie")
        einnahmen_kat = df_e_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
        total_einnahmen = einnahmen_kat.sum()
        colors = plt.get_cmap("tab20").colors[:len(einnahmen_kat)]

        fig1, ax1 = plt.subplots()
        wedges, _, _ = ax1.pie(
            einnahmen_kat,
            colors=colors,
            startangle=90,
            radius=1,
            wedgeprops={'edgecolor': 'white'}
        )
        ax1.axis('equal')

        for i, w in enumerate(wedges):
            kategorie = einnahmen_kat.index[i]
            betrag = einnahmen_kat.values[i]
            prozent = betrag / total_einnahmen * 100
            label = f"{kategorie}\n{betrag:.2f} CHF ({prozent:.1f}%)"

            angle = (w.theta2 + w.theta1) / 2
            x = np.cos(np.deg2rad(angle))
            y = np.sin(np.deg2rad(angle))
            ha = 'left' if x >= 0 else 'right'
            ax1.annotate(
                label,
                xy=(x, y),
                xytext=(1.4 * x, 1.4 * y),
                ha=ha,
                va='center',
                fontsize=10,
                color=colors[i],
                arrowprops=dict(arrowstyle='-', color=colors[i])
            )

        st.pyplot(fig1)

        st.markdown("**💵 Einnahmen – Detailübersicht:**")
        df_e_detail = pd.DataFrame({
            "Kategorie": einnahmen_kat.index,
            "Betrag (CHF)": [f"{v:,.2f}".replace(",", "'") for v in einnahmen_kat.values],
            "Anteil (%)": [f"{(v / total_einnahmen * 100):.1f}%" for v in einnahmen_kat.values]
        })
        st.table(df_e_detail)
    else:
        st.info("Keine Einnahmen in diesem Monat.")

    # -----------------------------
    # Ausgaben Kuchendiagramm mit farbigen Labels
    # -----------------------------
    if not df_a_monat.empty:
        st.subheader("💸 Ausgaben nach Kategorie")
        ausgaben_kat = df_a_monat.groupby("Kategorie")["Betrag (CHF)"].sum()
        total_ausgaben = ausgaben_kat.sum()
        colors = plt.get_cmap("tab20b").colors[:len(ausgaben_kat)]

        fig2, ax2 = plt.subplots()
        wedges, _, _ = ax2.pie(
            ausgaben_kat,
            colors=colors,
            startangle=90,
            radius=1,
            wedgeprops={'edgecolor': 'white'}
        )
        ax2.axis('equal')

        for i, w in enumerate(wedges):
            kategorie = ausgaben_kat.index[i]
            betrag = ausgaben_kat.values[i]
            prozent = betrag / total_ausgaben * 100
            label = f"{kategorie}\n{betrag:.2f} CHF ({prozent:.1f}%)"

            angle = (w.theta2 + w.theta1) / 2
            x = np.cos(np.deg2rad(angle))
            y = np.sin(np.deg2rad(angle))
            ha = 'left' if x >= 0 else 'right'
            ax2.annotate(
                label,
                xy=(x, y),
                xytext=(1.4 * x, 1.4 * y),
                ha=ha,
                va='center',
                fontsize=10,
                color=colors[i],
                arrowprops=dict(arrowstyle='-', color=colors[i])
            )

        st.pyplot(fig2)

        st.markdown("**💸 Ausgaben – Detailübersicht:**")
        df_a_detail = pd.DataFrame({
            "Kategorie": ausgaben_kat.index,
            "Betrag (CHF)": [f"{v:,.2f}".replace(",", "'") for v in ausgaben_kat.values],
            "Anteil (%)": [f"{(v / total_ausgaben * 100):.1f}%" for v in ausgaben_kat.values]
        })
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





