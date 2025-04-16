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

st.title('BMI Rechner')

st.markdown(f"✨ Hallo! ✨")
st.markdown("🏃 Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen und im Zeitverlauf zu verfolgen 📊")
        
# Add some health advice
st.info("""Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit. 
Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

st.write("Diese App wurde von Samuel Wehrli im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")