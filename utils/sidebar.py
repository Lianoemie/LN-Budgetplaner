import streamlit as st

def show_sidebar_userbox():
    if "user" in st.session_state:
        with st.sidebar:
            st.markdown(f"👤 Eingeloggt als: **{st.session_state['user']}**")
            if st.button("🚪 Logout"):
                st.session_state.clear()
                st.experimental_rerun()
