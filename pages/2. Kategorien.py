import streamlit as st

st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# Session-State initialisieren
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("🗂️ Kategorien verwalten")

# Kategorie hinzufügen
with st.form("neue_kategorie"):
    kategorie = st.text_input("Name der neuen Kategorie")
    kategorie_typ = st.selectbox("Für was ist die Kategorie gedacht?", ["Einnahme", "Ausgabe"])
    hinzufügen = st.form_submit_button("Hinzufügen")

    if hinzufügen:
        if not kategorie:
            st.error("Bitte gib einen Namen ein.")
        else:
            liste = st.session_state.kategorien_einnahmen if kategorie_typ == "Einnahme" else st.session_state.kategorien_ausgaben
            if kategorie in liste:
                st.warning("Diese Kategorie existiert bereits.")
            else:
                liste.append(kategorie)
                st.success(f"Kategorie '{kategorie}' als {kategorie_typ} hinzugefügt.")

# Übersicht der Kategorien
st.subheader("📥 Einnahmen-Kategorien")
st.write(st.session_state.kategorien_einnahmen)

st.subheader("📤 Ausgaben-Kategorien")
st.write(st.session_state.kategorien_ausgaben)
