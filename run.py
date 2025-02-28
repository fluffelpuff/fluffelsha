import time
import requests
import json

# Home Assistant API URL (direkt im selben Netzwerk)
HA_URL = "http://supervisor/core/api"

HEADERS = {
    "Content-Type": "application/json"
}

BUTTON_ENTITY_ID = "fluffelsha.test_button"

# Funktion zum Senden der Benachrichtigung
def send_notification(message):
    """Sendet eine Benachrichtigung an alle Geräte in Home Assistant"""
    data = {
        "message": message,
        "title": "Fluffelsha Test Notification",
        "target": "all"  # Sendet die Benachrichtigung an alle Geräte
    }
    url = f"{HA_URL}/services/notify/mobile_app"
    response = requests.post(url, headers=HEADERS, json=data)
    print(f"Notification sent: {response.status_code}")

# Funktion zur Aktualisierung des Buttons
def update_button(state):
    """Aktualisiert den Status des Buttons in Home Assistant"""
    data = {
        "state": state
    }
    url = f"{HA_URL}/states/{BUTTON_ENTITY_ID}"
    response = requests.post(url, headers=HEADERS, json=data)
    print(f"Button updated: {response.status_code}")

if __name__ == "__main__":
    while True:
        # Simuliere, dass der Button gedrückt wurde
        # Hier kannst du die Logik für das Erkennen des Button-Drucks einfügen
        update_button("pressed")
        send_notification("Der Test-Button wurde gedrückt!")
        
        # Setze den Button nach der Benachrichtigung zurück
        update_button("idle")
        
        time.sleep(10)  # 10 Sekunden warten, bevor die nächste Aktion ausgeführt wird
