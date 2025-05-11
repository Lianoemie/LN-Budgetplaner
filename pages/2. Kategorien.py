import streamlit as st

st.set_page_config(page_title="Kategorien verwalten", page_icon="🗂️")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now

LoginManager().go_to_login('Start.py')
# ====== End Login Block ======

dm = DataManager()

# ==============================
# Kategorien laden aus DataFrame
# ==============================
df_kategorien = dm.load_dataframe(session_state_key="kategorien_df", file_name="kategorien.csv")

# Listen extrahieren
einnahmen_kategorien = df_kategorien[df_kategorien["typ"] == "Einnahme"]["kategorie"].tolist()
ausgaben_kategorien = df_kategorien[df_kategorien["typ"] == "Ausgabe"]["kategorie"].tolist()

# Falls leer, Defaultwerte hinzufügen
if not einnahmen_kategorien:
    einnahmen_kategorien = ["Lohn", "Stipendium"]
if not ausgaben_kategorien:
    ausgaben_kategorien = ["Lebensmittel", "Miete", "Freizeit", "Transport", "Geschenke"]

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
            liste = einnahmen_kategorien if kategorie_typ == "Einnahme" else ausgaben_kategorien
            if kategorie in liste:
                st.warning("Diese Kategorie existiert bereits.")
            else:
                new_entry = {
                    "kategorie": kategorie,
                    "typ": kategorie_typ,
                    "zeitpunkt": ch_now()
                }
                dm.append_record(session_state_key='kategorien_df', record_dict=new_entry)
                st.success(f"Kategorie '{kategorie}' als {kategorie_typ} hinzugefügt.")
                st.rerun()

# -----------------------------
# Kategorie löschen
# -----------------------------
st.markdown("---")
st.subheader("🗑️ Kategorie löschen")

with st.form("kategorie_loeschen"):
    loesch_typ = st.selectbox("Art der Kategorie", ["Einnahme", "Ausgabe"])
    kategorien = einnahmen_kategorien if loesch_typ == "Einnahme" else ausgaben_kategorien

    if kategorien:
        auswahl = st.selectbox("Kategorie wählen", sorted(kategorien))
    else:
        auswahl = None
        st.info(f"Keine {loesch_typ}-Kategorien vorhanden.")

    loeschen = st.form_submit_button("Löschen")

    if loeschen and auswahl:
        # Zeile im DataFrame löschen
        df_kategorien = df_kategorien[~((df_kategorien["kategorie"] == auswahl) & (df_kategorien["typ"] == loesch_typ))]
        dm.save_dataframe(session_state_key="kategorien_df", file_name="kategorien.csv", dataframe=df_kategorien)

        st.success(f"Kategorie '{auswahl}' wurde gelöscht.")
        st.rerun()

# -----------------------------
# Kategorien anzeigen
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

zeige_kategorien("📥 Einnahmen-Kategorien", einnahmen_kategorien, farbe="#4CAF50")
zeige_kategorien("📤 Ausgaben-Kategorien", ausgaben_kategorien, farbe="#F44336")

# Optional: Session zurücksetzen (nur beim Entwickeln verwenden)
# if st.button("🔄 Testdaten zurücksetzen"):
#     dm.save_dataframe("kategorien_df", "kategorien.csv", pd.DataFrame([
#         {"kategorie": "Lohn", "typ": "Einnahme", "zeitpunkt": ch_now()},
#         {"kategorie": "Stipendium", "typ": "Einnahme", "zeitpunkt": ch_now()},
#         {"kategorie": "Lebensmittel", "typ": "Ausgabe", "zeitpunkt": ch_now()},
#         {"kategorie": "Miete", "typ": "Ausgabe", "zeitpunkt": ch_now()},
#         {"kategorie": "Freizeit", "typ": "Ausgabe", "zeitpunkt": ch_now()},
#         {"kategorie": "Transport", "typ": "Ausgabe", "zeitpunkt": ch_now()},
#         {"kategorie": "Geschenke", "typ": "Ausgabe", "zeitpunkt": ch_now()},
#     ]))
#     st.success("Testdaten zurückgesetzt. Seite neu laden.")
