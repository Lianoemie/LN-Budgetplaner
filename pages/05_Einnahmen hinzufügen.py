# ----------------------------------------
# Übersicht der gespeicherten Einnahmen
# ----------------------------------------
data = st.session_state.get('data_df', pd.DataFrame())
einnahmen_df = data[data['typ'] == 'einnahme'].copy()

if not einnahmen_df.empty:
    st.subheader("📋 Übersicht deiner Einnahmen")

    # Originalindex merken für Löschung
    einnahmen_df["original_index"] = einnahmen_df.index
    einnahmen_df.index = range(1, len(einnahmen_df) + 1)

    # Gesamtsumme anzeigen
    gesamt = einnahmen_df["betrag"].sum()
    st.metric("💵 Gesamteinnahmen", f"{gesamt:.2f} CHF")

    # Einzelanzeige mit Lösch-Buttons
    for idx, row in einnahmen_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
        col1.write(row["timestamp"])
        col2.write(row["kategorie"])
        col3.write(f"{row['betrag']:.2f} CHF")
        col4.write(row["beschreibung"] if row["beschreibung"] else "-")
        if col5.button("🗑️", key=f"delete_einnahme_{idx}"):
            original_index = row["original_index"]
            st.session_state.data_df.drop(index=original_index, inplace=True)
            DataManager().save_data("data_df")
            st.success("Einnahme gelöscht.")
            st.rerun()

    st.divider()

    # Alle Einnahmen löschen
    if st.button("❌ Alle Einnahmen löschen"):
        st.session_state.data_df = data[data['typ'] != 'einnahme']
        DataManager().save_data("data_df")
        st.success("Alle Einnahmen wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Einnahmen eingetragen.")
