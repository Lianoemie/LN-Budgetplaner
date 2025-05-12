import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
import json
import os

# ====== Login ======
LoginManager().go_to_login('Start.py')

import streamlit as st

# Initialisierung der Session States
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'vorname' not in st.session_state:
    st.session_state.vorname = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'fixkosten' not in st.session_state:
    st.session_state.fixkosten = ["Miete", "Handyvertrag"]
if 'kategorien' not in st.session_state:
    st.session_state.kategorien = ["Lebensmittel", "Freizeit"]
if 'sparziele' not in st.session_state:
    st.session_state.sparziele = ["Urlaub", "Notgroschen"]

st.title("📘 StudiBudget")
st.header("🧑‍💼 Mein Profil")

# Nutzerdaten anzeigen
st.subheader("Persönliche Informationen")
st.write(f"**Name:** {st.session_state.name}")
st.write(f"**Vorname:** {st.session_state.vorname}")
st.write(f"**Mail:** {st.session_state.email}")

with st.expander("Profil bearbeiten"):
    st.session_state.vorname = st.text_input("Vorname", value=st.session_state.vorname)
    st.session_state.name = st.text_input("Name", value=st.session_state.name)
    st.session_state.email = st.text_input("E-Mail", value=st.session_state.email)

# Fixkosten
st.subheader("🏠 Fixkosten")
for eintrag in st.session_state.fixkosten:
    st.write(f"- {eintrag}")
if st.button("Fixkosten bearbeiten ✏️"):
    st.switch_page("bearbeiten_fixkosten.py")

# Kategorien
st.subheader("📂 Kategorien")
for kategorie in st.session_state.kategorien:
    st.write(f"- {kategorie}")
if st.button("Kategorien bearbeiten ✏️"):
    st.switch_page("bearbeiten_kategorien.py")

# Sparziele
st.subheader("💰 Sparziele")
for ziel in st.session_state.sparziele:
    st.write(f"- {ziel}")
if st.button("Sparziele bearbeiten ✏️"):
    st.switch_page("bearbeiten_sparziele.py")

# Übersicht aller Daten
st.subheader("📊 Übersicht aller Daten")
st.write("**Fixkosten:**", ", ".join(st.session_state.fixkosten))
st.write("**Kategorien:**", ", ".join(st.session_state.kategorien))
st.write("**Sparziele:**", ", ".join(st.session_state.sparziele))

