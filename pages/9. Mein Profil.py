import streamlit as st

# --- Initialisierung ---
if 'name' not in st.session_state:
    st.session_state.update({
        'name': '',
        'vorname': '',
        'mail': '',
        'fixkosten': [],
        'kategorien': [],
        'sparziele': []
    })

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

st.divider()

# --- Helper-Funktion zum Anzeigen und Bearbeiten von Listen ---
def manage_section(section_name, state_key):
    st.subheader(section_name)
    # Bestehende Einträge anzeigen
    for idx, item in enumerate(st.session_state[state_key]):
        cols = st.columns([4, 1])
        new_val = cols[0].text_input(f"{section_name} {idx+1}", value=item, key=f"{state_key}_{idx}")
        if cols[1].button("❌", key=f"delete_{state_key}_{idx}"):
            st.session_state[state_key].pop(idx)
            st.experimental_rerun()
        else:
            st.session_state[state_key][idx] = new_val

    # Neuen Eintrag hinzufügen
    with st.form(f"add_{state_key}", clear_on_submit=True):
        new_item = st.text_input(f"Neuen Eintrag hinzufügen", key=f"new_{state_key}")
        if st.form_submit_button("Hinzufügen"):
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

# --- Übersicht ---
if st.button("📊 Übersicht aller Daten anzeigen"):
    st.subheader("📖 Übersicht")
    st.write(f"**Name:** {st.session_state['name']}")
    st.write(f"**Vorname:** {st.session_state['vorname']}")
    st.write(f"**Mail:** {st.session_state['mail']}")
    st.write("**📌 Fixkosten:**", st.session_state['fixkosten'])
    st.write("**📂 Kategorien:**", st.session_state['kategorien'])
    st.write("**🎯 Sparziele:**", st.session_state['sparziele'])
