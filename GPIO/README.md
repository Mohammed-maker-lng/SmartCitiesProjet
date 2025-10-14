# Dossier GPIO – Entrées / Sorties numériques du Raspberry Pi Pico W

## Description générale

Le dossier **GPIO** regroupe les projets et exercices portant sur la **gestion des entrées et sorties numériques** du **Raspberry Pi Pico W** programmés en **MicroPython**.

Ces projets illustrent comment :

* contrôler des **LEDs** ou d’autres actionneurs à l’aide des broches de sortie,
* lire l’état de **boutons poussoirs** ou capteurs connectés aux broches d’entrée,
* et utiliser les **interruptions matérielles (IRQ)** pour rendre le programme plus réactif.

Chaque script présent dans ce dossier démontre une fonctionnalité différente du module **`machine.Pin`** (et `PWM`/`ADC`) de MicroPython, essentiels pour manipuler le matériel du Pico W.

---

## Projet 1 : LED + Bouton poussoir (avec interruption)

### Objectif

Créer un petit système réactif utilisant :

* une **LED** connectée sur la broche **GPIO16**,
* un **bouton poussoir** sur **GPIO20**,
* et une **interruption matérielle** déclenchée à chaque appui sur le bouton.

L’appui sur le bouton permet de **changer le mode d’éclairage de la LED** parmi trois vitesses de clignotement différentes.

### Matériel & câblage

* LED → **GPIO16** via résistance série (220–330 Ω)
* Bouton poussoir → **GPIO20** (avec **PULL_UP** interne)
* GND commun

### Fonctionnement du programme

1. Initialisation des broches :

   * `Pin(16, Pin.OUT)` pour la LED
   * `Pin(20, Pin.IN, Pin.PULL_UP)` pour le bouton (avec résistance interne activée)
2. Définition d’une fonction d’interruption `bouton_irq()` appelée automatiquement à chaque **front descendant** (appui du bouton).
3. La variable `mode` change à chaque clic :

   * **mode = 0** → LED éteinte
   * **mode = 1** → clignotement lent
   * **mode = 2** → clignotement rapide
4. Une boucle infinie gère l’allumage selon le mode courant.

### Code

```python
from machine import Pin
from utime import sleep

led = Pin(16, Pin.OUT)
btn = Pin(20, Pin.IN, Pin.PULL_UP)
mode = 0

def bouton_irq(pin):
    global mode
    mode = (mode + 1) % 3
    print(f"mode : {mode}")

btn.irq(trigger=Pin.IRQ_FALLING, handler=bouton_irq)

while True:
    if mode == 0:
        led.value(0)
    elif mode == 1:
        led.value(1); sleep(0.5)
        led.value(0); sleep(0.5)
    elif mode == 2:
        led.value(1); sleep(0.25)
        led.value(0); sleep(0.25)
```

