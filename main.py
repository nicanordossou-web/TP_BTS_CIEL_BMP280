
from machine import Pin, SoftI2C
from bmp280 import BMP280
import time
import ujson

# Initialisation I2C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Initialisation du capteur
capteur = BMP280(i2c, address=0x76)

print("ESP32 pret : transmission des mesures")

while True:
    temperature, pression = capteur.read()

    # Preparation des donnees au format JSON
    donnees = {
        "capteur": "BMP280",
        "temperature": round(temperature, 2),
        "pression": round(pression, 2)
    }

    # Envoi des donnees au PC par USB serie
    print(ujson.dumps(donnees))

    time.sleep(2)
