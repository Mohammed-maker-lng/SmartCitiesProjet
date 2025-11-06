from machine import ADC
from time import ticks_ms, ticks_diff

class DetecteurSon:
    def __init__(self, broche_adc=26, seuil=18000, delai_ms=200):
        """
        broche_adc : GPIO où est branché le capteur (A0 = 26)
        seuil      : valeur à partir de laquelle on considère qu'il y a un pic
        delai_ms   : temps mini entre 2 détections pour éviter le spam
        """
        self.adc = ADC(broche_adc)
        self.seuil = seuil
        self.delai_ms = delai_ms
        self.dernier_pic = 0

    def lire(self):
        """Lit la valeur brute du capteur (0 -> 65535)."""
        return self.adc.read_u16()

    def detecter_pic(self):
        """
        Retourne True si un pic sonore est détecté.
        Sinon retourne False.
        """
        valeur = self.lire()
        maintenant = ticks_ms()

        # son fort + assez de temps depuis le dernier pic
        if valeur > self.seuil and ticks_diff(maintenant, self.dernier_pic) > self.delai_ms:
            self.dernier_pic = maintenant
            return True

        return False
