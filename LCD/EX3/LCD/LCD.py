from machine import I2C, Pin
from time import sleep
from LCD1602 import LCD1602  # ta librairie LCD d'origine

class LCD:
    """
    Classe simplifiée pour gérer un écran LCD1602 (sans RGB)
    via I2C (adresse par défaut 0x3E).
    """

    def __init__(self, scl_pin=9, sda_pin=8, i2c_id=0, lcd_addr=0x3E):
        """Initialise la communication I2C et le module LCD."""
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.lcd = LCD1602(self.i2c, lines=2, dotsize=0)
        self.clear()

    def clear(self):
        """Efface l’écran LCD."""
        self.lcd.clear()

    def print(self, text, line=0, col=0):
        """
        Affiche un texte à une position donnée.
        line = 0 → première ligne
        line = 1 → deuxième ligne
        """
        self.lcd.setCursor(col, line)
        self.lcd.print(text)

    def message(self, line1="", line2=""):
        """Affiche deux lignes de texte d’un coup."""
        self.clear()
        self.print(line1, 0, 0)
        self.print(line2, 1, 0)

    def scroll_text(self, text, delay=0.3):
        """Fait défiler un texte long sur la première ligne."""
        for i in range(len(text)):
            self.clear()
            self.print(text[i:i+16], 0)
            sleep(delay)

    def blink_message(self, line1, line2="", times=3, interval=0.5):
        """Fait clignoter un message plusieurs fois."""
        for _ in range(times):
            self.message(line1, line2)
            sleep(interval)
            self.clear()
            sleep(interval)
        self.message(line1, line2)
