import streamlit as st

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# --- Spartipps Page ---
st.title('💡 Spartipps')

st.markdown("""
# Clever sparen mit Studibudget ✨

Hier findest du hilfreiche Tipps, wie du im Alltag einfach und effektiv Geld sparen kannst – ohne auf alles verzichten zu müssen.
""")

st.markdown("""
### 🛒 Einkaufen

- **Einkaufslisten schreiben:**  
  Kaufe gezielt ein und vermeide spontane Käufe.
  
- **Angebote nutzen:**  
  Achte auf Aktionen und Rabatte, plane aber trotzdem bewusst.

- **Saisonal und regional einkaufen:**  
  Frische Produkte sind oft günstiger, wenn sie Saison haben.

### 🚌 Mobilität

- **ÖV statt Auto:**  
  Nutze öffentliche Verkehrsmittel, Fahrräder oder Carsharing-Angebote.

- **Rabatt-Abos:**  
  Profitiere von Studentenrabatten und vergünstigten Abonnements.

### 🎓 Studium und Alltag

- **Secondhand kaufen:**  
  Möbel, Bücher oder Kleidung gebraucht zu kaufen spart viel Geld.

- **Bibliotheken nutzen:**  
  Viele Fachbücher kannst du kostenlos ausleihen statt teuer kaufen.

- **Versicherungen vergleichen:**  
  Prüfe regelmäßig, ob günstigere Angebote für deine Versicherungen existieren.

### 🍴 Ernährung

- **Selber kochen:**  
  Essen gehen oder Take-Away summiert sich schnell – selbst kochen spart bares Geld.

- **Essensreste verwenden:**  
  Plane Mahlzeiten so, dass du Reste sinnvoll weiterverwenden kannst.

### 🎉 Freizeit

- **Gratisangebote nutzen:**  
  Viele Städte bieten kostenlose Events, Museen oder Sportangebote für Studierende.

- **Streaming-Dienste teilen:**  
  Abos gemeinsam nutzen und Kosten teilen.

---
""")

st.info("""
💬 **Tipp:**  
Nicht jeder Spartipp passt zu jedem – such dir die Strategien aus, die zu deinem Leben und deinen Bedürfnissen passen.
Schon kleine Veränderungen können auf lange Sicht einen großen Unterschied machen!
""")
