import streamlit as st

st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# Session-State für Kategorien initialisieren
if 'kategorien' not in st.session_state:
    st.session_state.kategorien = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("🗂️ Kategorien verwalten")

# Neue Kategorie hinzufügen
with st.form("kategorie_formular"):
    neue_kategorie = st.text_input("Neue Kategorie eingeben")
    kategorie_hinzufuegen = st.form_submit_button("Kategorie hinzufügen")

    if kategorie_hinzufuegen:
        if neue_kategorie and neue_kategorie not in st.session_state.kategorien:
            st.session_state.kategorien.append(neue_kategorie)
            st.success(f"Kategorie '{neue_kategorie}' hinzugefügt!")
        elif neue_kategorie in st.session_state.kategorien:
            st.warning("Diese Kategorie existiert bereits.")
        else:
            st.error("Bitte gib einen Namen für die Kategorie ein.")

# Anzeige der aktuellen Kategorien
st.subheader("Aktuelle Kategorien:")
st.write(st.session_state.kategorien)
