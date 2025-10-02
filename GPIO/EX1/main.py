from machine import Pin
from utime import sleep

# LED sur GPIO16
led = Pin(16, Pin.OUT)

# Bouton sur GPIO20 (résistance externe déjà câblée)
btn = Pin(20, Pin.IN)

mode = 0             # 0 = LED éteinte, 1 = lent, 2 = rapide
last_state = 0       # état précédent du bouton
delay_base = 1       # base du délai (1s = 0.5 Hz)

while True:
    state = btn.value()

    # Détection d'un appui (front descendant : 0->1)
    if state == 1 and last_state == 0:
        mode = (mode + 1) % 3   # cycle entre 0, 1 et 2
        print("Mode:", mode)
        sleep(0.2)  # anti-rebond simple

    last_state = state

    # Gestion des modes
    if mode == 0:
        led.off()
    elif mode == 1:
        led.toggle()
        sleep(delay_base)   # lent = 1 seconde
    elif mode == 2:
        led.toggle()
        sleep(delay_base/4) # rapide = 0.25 seconde
