import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager

st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# Login prüfen
LoginManager().go_to_login("Start.py")
dm = DataManager()

st.title("🗂️ Kategorien verwalten")

# Session-State vorbereiten
if "kategorien_einnahmen" not in st.session_state:
    st.session_state.kategorien_einnahmen = dm.load_kategorien("einnahmen")
if "kategorien_ausgaben" not in st.session_state:
    st.session_state.kategorien_ausgaben = dm.load_kategorien("ausgaben")

# Tabs für Einnahmen / Ausgaben
tab1, tab2 = st.tabs(["💰 Einnahmen", "💸 Ausgaben"])

with tab1:
    st.subheader("Einnahmen-Kategorien")
    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="ein_kat")
    if st.button("➕ Hinzufügen", key="btn_add_ein"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_einnahmen:
            st.session_state.kategorien_einnahmen.append(neue_kategorie)
            dm.save_kategorien("einnahmen", st.session_state.kategorien_einnahmen)
            st.success("Kategorie hinzugefügt!")

    if st.session_state.kategorien_einnahmen:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_einnahmen, key="del_ein")
        if st.button("🗑️ Löschen", key="btn_del_ein"):
            st.session_state.kategorien_einnahmen.remove(zu_loeschen)
            dm.save_kategorien("einnahmen", st.session_state.kategorien_einnahmen)
            st.success("Kategorie gelöscht!")

with tab2:
    st.subheader("Ausgaben-Kategorien")
    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="aus_kat")
    if st.button("➕ Hinzufügen", key="btn_add_aus"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_ausgaben:
            st.session_state.kategorien_ausgaben.append(neue_kategorie)
            dm.save_kategorien("ausgaben", st.session_state.kategorien_ausgaben)
            st.success("Kategorie hinzugefügt!")

    if st.session_state.kategorien_ausgaben:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_ausgaben, key="del_aus")
        if st.button("🗑️ Löschen", key="btn_del_aus"):
            st.session_state.kategorien_ausgaben.remove(zu_loeschen)
            dm.save_kategorien("ausgaben", st.session_state.kategorien_ausgaben)
            st.success("Kategorie gelöscht!")
