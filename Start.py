import streamlit as st
import pandas as pd

from utils.data_manager import DataManager
# https://moodle.zhaw.ch/pluginfile.php/2103313/mod_resource/content/17/chapters/data_manager_api.html --> Anleitung

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Selia App")  # switch drive 

# load the data from the persistent storage into the session state
data_manager.load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )

st.title('Studibudget')

st.markdown(f"Hallo! ")
st.markdown("Die Anwendung ermöglicht es dir, deine Finanzen zu ordnen und Struktur zu schaffen")
        
st.info("""Studibudget hilft dir, den Überblick über deine Finanzen zu behalten – ersetzt aber keine professionelle Finanzberatung. 
Für eine umfassende Einschätzung deiner finanziellen Situation wende dich bitte an eine Fachperson.""")


st.write("Diese App wurde von Selina Rüdisüli, Elena Stevanovic und Lia Müller  im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")