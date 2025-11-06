from machine import Pin
import neopixel
import urandom

class RGBLed:
    def __init__(self, pin=18):
        self.np = neopixel.NeoPixel(Pin(pin), 1)

    def set_color(self, r, g, b):
        self.np[0] = (r, g, b)
        self.np.write()

    def random_color(self):
        r = urandom.getrandbits(8)
        g = urandom.getrandbits(8)
        b = urandom.getrandbits(8)
        if r < 40 and g < 40 and b < 40:
            r = 255
        self.set_color(r, g, b)
