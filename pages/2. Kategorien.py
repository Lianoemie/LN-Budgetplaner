import streamlit as st



st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# Session-State initialisieren
if 'kategorien_einnahmen' not in st.session_state:
    st.session_state.kategorien_einnahmen = ["Lohn", "Stipendium"]
if 'kategorien_ausgaben' not in st.session_state:
    st.session_state.kategorien_ausgaben = ["Lebensmittel", "Miete", "Freizeit", "Transport"]

st.title("🗂️ Kategorien verwalten")

# -----------------------------
# Neue Kategorie hinzufügen
# -----------------------------
with st.form("neue_kategorie"):
    st.subheader("➕ Neue Kategorie erfassen")
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

# -----------------------------
# Kategorie löschen
# -----------------------------
st.markdown("---")
st.subheader("🗑️ Kategorie löschen")

with st.form("kategorie_loeschen"):
    loesch_typ = st.selectbox("Art der Kategorie", ["Einnahme", "Ausgabe"])

    if loesch_typ == "Einnahme":
        if st.session_state.kategorien_einnahmen:
            auswahl = st.selectbox("Kategorie wählen", st.session_state.kategorien_einnahmen)
        else:
            auswahl = None
            st.info("Keine Einnahmen-Kategorien vorhanden.")
    else:
        if st.session_state.kategorien_ausgaben:
            auswahl = st.selectbox("Kategorie wählen", st.session_state.kategorien_ausgaben)
        else:
            auswahl = None
            st.info("Keine Ausgaben-Kategorien vorhanden.")

    loeschen = st.form_submit_button("Löschen")

    if loeschen and auswahl:
        if loesch_typ == "Einnahme":
            st.session_state.kategorien_einnahmen.remove(auswahl)
        else:
            st.session_state.kategorien_ausgaben.remove(auswahl)
        st.success(f"Kategorie '{auswahl}' wurde gelöscht.")
        st.rerun()  # Seite neu laden

# -----------------------------
# Kategorien anzeigen (Badges)
# -----------------------------
st.markdown("---")

def zeige_kategorien(titel, kategorien, farbe):
    st.markdown(f"### {titel}")
    if kategorien:
        badges = " ".join([
            f"<span style='background-color:{farbe}; padding:4px 12px; border-radius:20px; color:white; font-size:14px; margin-right:6px'>{k}</span>"
            for k in kategorien
        ])
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.write("Noch keine Kategorien vorhanden.")

zeige_kategorien("📥 Einnahmen-Kategorien", st.session_state.kategorien_einnahmen, farbe="#4CAF50")
zeige_kategorien("📤 Ausgaben-Kategorien", st.session_state.kategorien_ausgaben, farbe="#F44336")
