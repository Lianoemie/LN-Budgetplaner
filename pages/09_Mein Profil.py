import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
import json
import os
from utils.style import set_background #Hintergrundfarbe
set_background()


# ====== Login ======
LoginManager().go_to_login('Start.py')

import streamlit as st
import pandas as pd

# Session State Initialisierung
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'vorname' not in st.session_state:
    st.session_state.vorname = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'data_df' not in st.session_state:
    st.session_state.data_df = pd.DataFrame()
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = []
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = []

st.title("📘 StudiBudget")
st.header("🧑‍💼 Mein Profil")

st.subheader("👤 Persönliche Informationen")


# Anzeige
st.write(f"**Name:** {st.session_state.vorname} {st.session_state.name}")
st.write(f"**E-Mail:** {st.session_state.email}")

# Bearbeitung
with st.expander("📋 Profil bearbeiten"):
    st.session_state.name = st.text_input("Name", value=st.session_state.name)
    st.session_state.email = st.text_input("E-Mail", value=st.session_state.email)


# ----------------------------------------
# Fixkosten Übersicht
# ----------------------------------------
st.subheader("🏠 Fixkosten")
fixkosten_df = st.session_state.data_df
fixkosten_df = fixkosten_df[fixkosten_df["typ"] == "fixkosten"]

if not fixkosten_df.empty:
    for _, row in fixkosten_df.iterrows():
        st.write(f"- {row['kategorie']}: {row['betrag']:.2f} CHF ({row['wiederholung']})")
else:
    st.info("Noch keine Fixkosten eingetragen.")

if st.button("Fixkosten bearbeiten ✏️"):
    st.switch_page("pages/03_Fixkosten.py")

st.divider()

# ----------------------------------------
# Kategorien Übersicht
# ----------------------------------------
st.subheader("📂 Kategorien")

st.write("**Einnahmen-Kategorien:**")
if st.session_state.kategorien_einnahmen:
    st.write(", ".join(st.session_state.kategorien_einnahmen))
else:
    st.info("Noch keine Einnahmen-Kategorien.")

st.write("**Ausgaben-Kategorien:**")
if st.session_state.kategorien_ausgaben:
    st.write(", ".join(st.session_state.kategorien_ausgaben))
else:
    st.info("Noch keine Ausgaben-Kategorien.")

if st.button("Kategorien bearbeiten ✏️"):
    st.switch_page("pages/02_Kategorien.py")

st.divider()

# ----------------------------------------
# Sparziele Übersicht
# ----------------------------------------
st.subheader("💰 Sparziele")
sparziele_df = st.session_state.data_df
sparziele_df = sparziele_df[sparziele_df["typ"] == "sparziel"]

if not sparziele_df.empty:
    einzahlungen_df = st.session_state.data_df
    einzahlungen_df = einzahlungen_df[einzahlungen_df["typ"] == "einzahlung"].copy()

    for _, row in sparziele_df.iterrows():
        zielname = row["name"]
        zielbetrag = row["zielbetrag"]
        startbetrag = row.get("bisher_gespart", 0.0)

        einzahlungen_summe = einzahlungen_df[einzahlungen_df["zielname"] == zielname]["betrag"].sum()
        gesamt_gespart = startbetrag + einzahlungen_summe

        st.write(f"- {zielname}: Ziel {zielbetrag:.2f} CHF, Gespart: {gesamt_gespart:.2f} CHF, Ziel-Datum: {row['zieldatum']}")
        if gesamt_gespart >= zielbetrag:
            st.success(f"🎉 Ziel erreicht: {zielname}!")
        else:
            st.warning(f"🚧 Ziel noch nicht erreicht: {zielname}." )
else:
    st.info("Noch keine Sparziele vorhanden.")

if st.button("Sparziele bearbeiten ✏️"):
    st.switch_page("pages/04_Sparziele.py")

