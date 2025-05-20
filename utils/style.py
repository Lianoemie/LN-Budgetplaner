import streamlit as st

def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #ffe6f0, #ffffff);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
