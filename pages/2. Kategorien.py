import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager

st.set_page_config(page_title="Kategorien", page_icon="🗂️")

# Login prüfen
LoginManager().go_to_login("Start.py")
dm = DataManager()

# ------------------------------
# Kategorien initial aus Datei laden
# ------------------------------
dm.load_user_data("kategorien_einnahmen", "kategorien_einnahmen.json", initial_value=[])
dm.load_user_data("kategorien_ausgaben", "kategorien_ausgaben.json", initial_value=[])

st.title("🗂️ Kategorien verwalten")

# Tabs: Einnahmen & Ausgaben
tab1, tab2 = st.tabs(["💰 Einnahmen", "💸 Ausgaben"])

# ------------------------------
# Einnahmen-Kategorien
# ------------------------------
with tab1:
    st.subheader("Einnahmen-Kategorien")
    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="input_ein")
    if st.button("➕ Hinzufügen", key="add_ein"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_einnahmen:
            st.session_state.kategorien_einnahmen.append(neue_kategorie)
            dm.save_data("kategorien_einnahmen")
            st.success(f"'{neue_kategorie}' wurde hinzugefügt.")

    if st.session_state.kategorien_einnahmen:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_einnahmen, key="del_ein")
        if st.button("🗑️ Löschen", key="btn_del_ein"):
            st.session_state.kategorien_einnahmen.remove(zu_loeschen)
            dm.save_data("kategorien_einnahmen")
            st.success(f"'{zu_loeschen}' wurde gelöscht.")

# ------------------------------
# Ausgaben-Kategorien
# ------------------------------
with tab2:
    st.subheader("Ausgaben-Kategorien")
    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="input_aus")
    if st.button("➕ Hinzufügen", key="add_aus"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_ausgaben:
            st.session_state.kategorien_ausgaben.append(neue_kategorie)
            dm.save_data("kategorien_ausgaben")
            st.success(f"'{neue_kategorie}' wurde hinzugefügt.")

    if st.session_state.kategorien_ausgaben:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_ausgaben, key="del_aus")
        if st.button("🗑️ Löschen", key="btn_del_aus"):
            st.session_state.kategorien_ausgaben.remove(zu_loeschen)
            dm.save_data("kategorien_ausgaben")
            st.success(f"'{zu_loeschen}' wurde gelöscht.")
