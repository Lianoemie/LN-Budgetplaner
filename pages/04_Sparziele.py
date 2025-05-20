import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sparziele", page_icon="🎯")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
from utils.helpers import ch_now
LoginManager().go_to_login('Start.py')

# ====== App-Daten laden ======
DataManager().load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

st.title("🎯 Sparziele verwalten")

data = st.session_state.get('data_df', pd.DataFrame())

# -----------------------------
# Neues Sparziel erfassen
# -----------------------------
with st.form("sparziel_formular"):
    st.subheader("Neues Sparziel erstellen")
    name = st.text_input("Name des Sparziels")
    zielbetrag = st.number_input("Zielbetrag (CHF)", min_value=1.0, step=10.0, format="%.2f")
    aktueller_betrag = st.number_input("Bisher gespart (CHF)", min_value=0.0, step=10.0, format="%.2f")
    ziel_datum = st.date_input("Gewünschtes Ziel-Datum", value=datetime.today())
    sparziel_erstellen = st.form_submit_button("Sparziel hinzufügen")

    if sparziel_erstellen and name and zielbetrag > 0:
        neues_ziel = {
            "typ": "sparziel",
            "name": name,
            "zielbetrag": zielbetrag,
            "bisher_gespart": aktueller_betrag,
            "timestamp": str(datetime.today().date()),
            "zieldatum": str(ziel_datum)
        }
        DataManager().append_record('data_df', neues_ziel)
        st.success("Sparziel gespeichert!")
        st.rerun()

# -----------------------------
# Übersicht Sparziele
# -----------------------------
sparziele = data[data["typ"] == "sparziel"].copy()
einzahlungen = data[data["typ"] == "einzahlung"].copy()

# Sicherheits-Check: Spalte "zielname" ergänzen, falls nicht vorhanden
if "zielname" not in einzahlungen.columns:
    einzahlungen["zielname"] = ""

if not sparziele.empty:
    st.subheader("📋 Übersicht deiner Sparziele")

    def motivation(fortschritt):
        if fortschritt == 1:
            return "🎉 Glückwunsch, du hast dein Sparziel erreicht!"
        elif fortschritt >= 0.75:
            return "🚀 Fast geschafft – das Ziel ist zum Greifen nah!"
        elif fortschritt >= 0.5:
            return "💪 Mehr als die Hälfte ist geschafft – stark!"
        elif fortschritt >= 0.25:
            return "🧱 Du hast schon ein gutes Stück geschafft!"
        else:
            return "✨ Jeder Franken zählt – bleib dran!"

    for i, ziel in sparziele.iterrows():
        zielname = ziel['name']
        zielbetrag = ziel['zielbetrag']

        # Zugehörige Einzahlungen summieren
        einzahlungen_zum_ziel = einzahlungen[einzahlungen["zielname"] == zielname]
        summe_einzahlungen = einzahlungen_zum_ziel["betrag"].sum()
        gesamt_gespart = ziel["bisher_gespart"] + summe_einzahlungen

        rest = max(zielbetrag - gesamt_gespart, 0)
        fortschritt = min(gesamt_gespart / zielbetrag, 1.0)

        st.markdown(f"### 🎯 {zielname}")
        st.text(f"Gespart: {gesamt_gespart:.2f} CHF von {zielbetrag:.2f} CHF")
        st.progress(fortschritt)
        st.markdown(f"**💸 Noch fehlend:** {rest:.2f} CHF")
        st.markdown(f"{motivation(fortschritt)}")

        # Einzahlung hinzufügen
        with st.expander(f"➕ Einzahlung hinzufügen für {zielname}"):
            betrag = st.number_input(
                f"Betrag einzahlen für '{zielname}'",
                min_value=0.0,
                step=10.0,
                format="%.2f",
                key=f"einzahlen_{i}"
            )
            if st.button(f"Einzahlen auf '{zielname}'", key=f"button_{i}"):
                if betrag > 0:
                    einzahlung = {
                        "typ": "einzahlung",
                        "zielname": zielname,
                        "betrag": betrag,
                        "timestamp": str(datetime.today().date())
                    }
                    DataManager().append_record('data_df', einzahlung)
                    st.success(f"{betrag:.2f} CHF erfolgreich eingezahlt!")
                    st.rerun()

        # Liste der Einzahlungen anzeigen
        if not einzahlungen_zum_ziel.empty:
            st.markdown(f"**Bisherige Einzahlungen für {zielname}:**")
            for j, row in einzahlungen_zum_ziel.iterrows():
                cols = st.columns([3, 2, 1])
                cols[0].markdown(f"- {row['timestamp']}")
                cols[1].markdown(f"{row['betrag']:.2f} CHF")
                if cols[2].button("🗑️", key=f"delete_einzahlung_{i}_{j}"):
                    st.session_state.data_df.drop(index=j, inplace=True)
                    DataManager().save_app_data('data_df', 'data.csv')
                    st.success("Einzahlung gelöscht.")
                    st.rerun()

        # Sparziel löschen (mit Sicherheitsprüfung)
        if st.button(f"❌ Sparziel '{zielname}' löschen", key=f"delete_sparziel_{i}"):
            df = st.session_state.data_df

            # Spalten ergänzen, falls sie fehlen
            for col in ["typ", "zielname", "name"]:
                if col not in df.columns:
                    df[col] = ""

            # Filter anwenden und Daten neu setzen
            mask = ~(
                ((df["typ"] == "sparziel") & (df["name"] == zielname)) |
                ((df["typ"] == "einzahlung") & (df["zielname"] == zielname))
            )
            st.session_state.data_df = df[mask]

            DataManager().save_app_data('data_df', 'data.csv')
            st.success(f"Sparziel '{zielname}' wurde gelöscht.")
            st.rerun()

        st.divider()
else:
    st.info("Noch keine Sparziele vorhanden. Lege eines an!")
