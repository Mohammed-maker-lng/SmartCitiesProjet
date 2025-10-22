from machine import Pin
import dht
from time import sleep

class DHT:
    def __init__(self, pin=18):
        self.sensor = dht.DHT11(Pin(pin))

    def lire_mesures(self):
        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            return temp, hum
        except OSError:
            print("Erreur de lecture du capteur DHT11")
            return None,None

    def afficher_mesures(self):
        temp, hum = self.lire_mesures()
        if temp is not None:
            print(f"Temp : {temp} °C | Hum : {hum} %")
