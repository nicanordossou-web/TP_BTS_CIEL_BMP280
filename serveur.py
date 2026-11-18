
import serial
import json

# Connexion a l'ESP32
esp32 = serial.Serial("COM4", 115200, timeout=2)

print("SERVEUR PYTHON DEMARRE")
print("En attente des mesures du BMP280...")

while True:
    ligne = esp32.readline().decode("utf-8", errors="replace").strip()

    if ligne:
        try:
            donnees = json.loads(ligne)

            print("Capteur :", donnees["capteur"])
            print("Temperature :", donnees["temperature"], "°C")
            print("Pression :", donnees["pression"], "hPa")

        except json.JSONDecodeError:
            print("Message :", ligne)
