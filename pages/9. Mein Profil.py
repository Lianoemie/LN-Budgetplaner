import streamlit as st

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# --- Sichere Initialisierung des Session States ---
default_state = {
    'name': '',
    'vorname': '',
    'mail': '',
    'fixkosten': [],
    'kategorien': [],
    'sparziele': []
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("📚 Studibudget")

# --- Mein Profil ---
st.header("👤 Mein Profil")
with st.form("profil_form", clear_on_submit=False):
    name = st.text_input("Name:", value=st.session_state['name'])
    vorname = st.text_input("Vorname:", value=st.session_state['vorname'])
    mail = st.text_input("Mail:", value=st.session_state['mail'])
    if st.form_submit_button("Speichern"):
        st.session_state['name'] = name
        st.session_state['vorname'] = vorname
        st.session_state['mail'] = mail
        st.success("Profil gespeichert!")

# --- Direkte Anzeige der Profildaten ---
st.info(f"**Name:** {st.session_state['name']}  \n"
        f"**Vorname:** {st.session_state['vorname']}  \n"
        f"**Mail:** {st.session_state['mail']}")

st.divider()

# --- Helper-Funktion zum Anzeigen und Bearbeiten von Listen ---
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

    # Löschen nach der Schleife (vermeidet Indexfehler)
    for idx in sorted(indices_to_delete, reverse=True):
        st.session_state[state_key].pop(idx)
        st.experimental_rerun()

    # Neuen Eintrag hinzufügen
    new_item = st.text_input(f"Neuen Eintrag hinzufügen ({section_name}):", key=f"new_{state_key}")
    if st.button("➕ Hinzufügen", key=f"add_{state_key}"):
        if new_item:
            st.session_state[state_key].append(new_item)
            st.success(f"{section_name} hinzugefügt!")
            st.experimental_rerun()

# --- Fixkosten ---
manage_section("📌 Fixkosten", "fixkosten")
st.divider()

# --- Kategorien ---
manage_section("📂 Kategorien", "kategorien")
st.divider()

# --- Sparziele ---
manage_section("🎯 Sparziele", "sparziele")
st.divider()
