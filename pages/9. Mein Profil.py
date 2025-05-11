import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
import json
import os

# ====== Login ======
LoginManager().go_to_login('Start.py')

# Mail aus Login holen (angenommen, LoginManager setzt das bereits)
if 'mail' not in st.session_state or not st.session_state['mail']:
    st.error("Bitte zuerst einloggen!")
    st.stop()

mail = st.session_state['mail']

# --- Daten Laden ---
DATA_DIR = "user_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

filepath = os.path.join(DATA_DIR, f"{mail}.json")
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        user_data = json.load(f)
else:
    user_data = {
        'name': '',
        'vorname': '',
        'mail': mail,
        'fixkosten': [],
        'kategorien': [],
        'sparziele': []
    }

# --- Initialisierung im Session-State ---
for key, value in user_data.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("📚 Studibudget")

# --- Profil ---
st.header("👤 Mein Profil")
with st.form("profil_form", clear_on_submit=False):
    name = st.text_input("Name:", value=st.session_state['name'])
    vorname = st.text_input("Vorname:", value=st.session_state['vorname'])
    mail_display = st.text_input("Mail (nicht bearbeitbar):", value=mail, disabled=True)
    if st.form_submit_button("Speichern"):
        st.session_state['name'] = name
        st.session_state['vorname'] = vorname
        user_data.update({'name': name, 'vorname': vorname})
        with open(filepath, 'w') as f:
            json.dump(user_data, f)
        st.success("Profil gespeichert!")

st.info(f"**Name:** {st.session_state['name']}  \n"
        f"**Vorname:** {st.session_state['vorname']}  \n"
        f"**Mail:** {mail}")

st.divider()

# --- Helper-Funktion ---
def manage_section(section_name, state_key):
    st.subheader(section_name)
    indices_to_delete = []
    for idx, item in enumerate(st.session_state[state_key]):
        cols = st.columns([4, 1])
        new_val = cols[0].text_input(f"{section_name} {idx+1}", value=item, key=f"{state_key}_{idx}")
        if cols[1].button("❌", key=f"delete_{state_key}_{idx}"):
            indices_to_delete.append(idx)
        else:
            st.session_state[state_key][idx] = new_val

    for idx in sorted(indices_to_delete, reverse=True):
        st.session_state[state_key].pop(idx)
        st.experimental_rerun()

    new_item = st.text_input(f"Neuen Eintrag hinzufügen ({section_name}):", key=f"new_{state_key}")
    if st.button("➕ Hinzufügen", key=f"add_{state_key}"):
        if new_item:
            st.session_state[state_key].append(new_item)
            st.success(f"{section_name} hinzugefügt!")
            st.experimental_rerun()

    # Änderungen speichern
    user_data[state_key] = st.session_state[state_key]
    with open(filepath, 'w') as f:
        json.dump(user_data, f)

# --- Abschnitte ---
manage_section("📌 Fixkosten", "fixkosten")
st.divider()

manage_section("📂 Kategorien", "kategorien")
st.divider()

manage_section("🎯 Sparziele", "sparziele")
st.divider()
