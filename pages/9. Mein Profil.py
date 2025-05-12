import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
import json
import os

# ====== Login ======
LoginManager().go_to_login('Start.py')

# Nutzerdaten initialisieren
if 'users' not in st.session_state:
    st.session_state.users = {}

st.title("📘 StudiBudget")
st.header("🧑‍💼 Mein Profil")

# --- Login/E-Mail-Eingabe ---
st.subheader("Identifikation")
email = st.text_input("E-Mail", key="profil_email")

# Benutzerdatensatz initialisieren, wenn E-Mail eingegeben
if email:
    if email not in st.session_state.users:
        st.session_state.users[email] = {
            "vorname": "",
            "nachname": "",
            "fixkosten": [],
            "kategorien": [],
            "sparziele": [],
        }

    user_data = st.session_state.users[email]

    # --- Profilfelder anzeigen & bearbeiten ---
    st.subheader("Persönliche Informationen")
    user_data["vorname"] = st.text_input("Vorname", value=user_data["vorname"])
    user_data["nachname"] = st.text_input("Nachname", value=user_data["nachname"])

    # --- Übersicht: Fixkosten ---
    st.subheader("🏠 Fixkosten")
    for eintrag in user_data["fixkosten"]:
        st.write(f"- {eintrag}")
    if st.button("Fixkosten bearbeiten ✏️"):
        st.session_state.current_user_email = email
        st.switch_page("bearbeiten_fixkosten.py")

    # --- Übersicht: Kategorien ---
    st.subheader("📂 Kategorien")
    for kategorie in user_data["kategorien"]:
        st.write(f"- {kategorie}")
    if st.button("Kategorien bearbeiten ✏️"):
        st.session_state.current_user_email = email
        st.switch_page("bearbeiten_kategorien.py")

    # --- Übersicht: Sparziele ---
    st.subheader("💰 Sparziele")
    for ziel in user_data["sparziele"]:
        st.write(f"- {ziel}")
    if st.button("Sparziele bearbeiten ✏️"):
        st.session_state.current_user_email = email
        st.switch_page("bearbeiten_sparziele.py")

    # --- Übersicht aller Daten ---
    st.subheader("📊 Übersicht aller Daten")
    st.write("**Fixkosten:**", ", ".join(user_data["fixkosten"]))
    st.write("**Kategorien:**", ", ".join(user_data["kategorien"]))
    st.write("**Sparziele:**", ", ".join(user_data["sparziele"]))
