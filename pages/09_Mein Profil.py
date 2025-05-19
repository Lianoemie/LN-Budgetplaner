import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
import json
import os

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
    st.switch_page("pages/bearbeiten_fixkosten.py")

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
    st.switch_page("pages/bearbeiten_kategorien.py")

st.divider()

# ----------------------------------------
# Sparziele Übersicht
# ----------------------------------------
st.subheader("💰 Sparziele")
sparziele_df = st.session_state.data_df
sparziele_df = sparziele_df[sparziele_df["typ"] == "sparziel"]

if not sparziele_df.empty:
    for _, row in sparziele_df.iterrows():
        st.write(f"- {row['name']}: Ziel {row['zielbetrag']:.2f} CHF, Gespart: {row['bisher_gespart']:.2f} CHF, Ziel-Datum: {row['zieldatum']}")
else:
    st.info("Noch keine Sparziele vorhanden.")

if st.button("Sparziele bearbeiten ✏️"):
    st.switch_page("pages/bearbeiten_sparziele.py")

