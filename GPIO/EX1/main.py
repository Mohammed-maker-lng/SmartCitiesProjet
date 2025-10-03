from machine import Pin
from utime import sleep

# LED sur GPIO16
led = Pin(16, Pin.OUT)

# Bouton sur GPIO20 avec résistance interne pull-up
btn = Pin(20, Pin.IN, Pin.PULL_UP)

mode = 0

# Fonction d’interruption
def bouton_irq(pin):
    global mode #fait reference a la variable global mode

    print("click")
    mode = (mode+1)%3
    print (f"mode : {mode}")


# Ici on déclenche sur front descendant (1 -> 0 = appui du bouton)
btn.irq(trigger=Pin.IRQ_FALLING, handler=bouton_irq)

# Boucle infinie pour garder le programme en vie
while True:

    if mode == 0 : 
        led.value(0)

    elif mode == 1 : 
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)


    elif mode == 2 : 
        led.value(1)
        sleep(0.25)
        led.value(0)
        sleep(0.25)
