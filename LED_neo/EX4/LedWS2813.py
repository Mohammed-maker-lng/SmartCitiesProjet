# led_ws2813.py
from machine import Pin
import neopixel

class LedWS2813:
    def __init__(self, broche=18, nb_led=1):
        # 1 LED WS2813 sur la broche donnée (D18 -> GPIO 18)
        self.np = neopixel.NeoPixel(Pin(broche), nb_led)

    def couleur(self, r, v, b):
        # r, v, b de 0 à 255
        self.np[0] = (r, v, b)
        self.np.write()

    def eteindre(self):
        self.couleur(0, 0, 0)
