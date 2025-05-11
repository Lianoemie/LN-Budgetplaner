import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager

st.set_page_config(page_title="Kategorien", page_icon="🗂️")

# Login prüfen
LoginManager().go_to_login("Start.py")
dm = DataManager()

dm = DataManager()

# Wichtig: Daten direkt laden & registrieren, BEVOR etwas anderes kommt
if "username" not in st.session_state:
    st.warning("⚠️ Kein Benutzer eingeloggt. Die Seite funktioniert nicht ohne Login.")
else:
    dm.load_user_data("kategorien_einnahmen", "kategorien_einnahmen.json", initial_value=[])
    dm.load_user_data("kategorien_ausgaben", "kategorien_ausgaben.json", initial_value=[])


# Tabs für Einnahmen und Ausgaben
tab1, tab2 = st.tabs(["💰 Einnahmen", "🧾 Ausgaben"])

# -----------------------------
# Tab 1: Einnahmen-Kategorien
# -----------------------------
with tab1:
    st.subheader("Einnahmen-Kategorien")

    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="input_einnahmen")
    if st.button("➕ Hinzufügen", key="btn_add_einnahmen"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_einnahmen:
            st.session_state.kategorien_einnahmen.append(neue_kategorie)
            dm.save_data("kategorien_einnahmen")
            st.success(f"'{neue_kategorie}' wurde hinzugefügt.")

    if st.session_state.kategorien_einnahmen:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_einnahmen, key="select_del_einnahmen")
        if st.button("🗑️ Löschen", key="btn_del_einnahmen"):
            st.session_state.kategorien_einnahmen.remove(zu_loeschen)
            dm.save_data("kategorien_einnahmen")
            st.success(f"'{zu_loeschen}' wurde gelöscht.")

# -----------------------------
# Tab 2: Ausgaben-Kategorien
# -----------------------------
with tab2:
    st.subheader("Ausgaben-Kategorien")

    neue_kategorie = st.text_input("Neue Kategorie hinzufügen:", key="input_ausgaben")
    if st.button("➕ Hinzufügen", key="btn_add_ausgaben"):
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien_ausgaben:
            st.session_state.kategorien_ausgaben.append(neue_kategorie)
            dm.save_data("kategorien_ausgaben")
            st.success(f"'{neue_kategorie}' wurde hinzugefügt.")

    if st.session_state.kategorien_ausgaben:
        zu_loeschen = st.selectbox("Kategorie löschen:", st.session_state.kategorien_ausgaben, key="select_del_ausgaben")
        if st.button("🗑️ Löschen", key="btn_del_ausgaben"):
            st.session_state.kategorien_ausgaben.remove(zu_loeschen)
            dm.save_data("kategorien_ausgaben")
            st.success(f"'{zu_loeschen}' wurde gelöscht.")
