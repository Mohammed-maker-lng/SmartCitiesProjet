from time import sleep_ms
from urandom import getrandbits

from LedWS2813 import LedWS2813     # fichier où tu as mis la classe LED
from DetecteurSon import DetecteurSon   # ton fichier ci-dessus

def couleur_aleatoire(led):
    # génère une couleur RGB (0..255)
    r = getrandbits(8)
    v = getrandbits(8)
    b = getrandbits(8)
    led.couleur(r, v, b)

def main():
    led = LedWS2813(broche=18)
    led.eteindre()

    detecteur = DetecteurSon(broche_adc=26, seuil=18000, delai_ms=150)

    while True:
        if detecteur.detecter_pic():
            # à chaque pic sonore : nouvelle couleur
            couleur_aleatoire(led)

        sleep_ms(20)

main()
