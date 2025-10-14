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

---

## Projet 2 : Sonnerie (mélodie) sur buzzer **+ volume** géré dans un **thread séparé**

### Objectif

* Jouer une **mélodie** sur un **buzzer** (`PWM`) avec une **LED** qui clignote au rythme des notes.
* Pouvoir **changer de mélodie** avec un **bouton** (IRQ).
* **Gérer le volume** via un **potentiomètre** (`ADC`) **dans un thread à part** pour une lecture fluide et sans bloquer le jeu des notes.

### Matériel & câblage

* Buzzer (passif) → **GPIO16** (PWM)
* LED → **GPIO18** (OUT)
* Potentiomètre → **GPIO26** (ADC0) + 3V3 + GND
* Bouton poussoir → **GPIO20** (IN, **PULL_DOWN**) + 3V3

> Les broches utilisées ici (16, 18, 20, 26) sont **propres au Projet 2** et ne doivent pas être utilisées simultanément avec le Projet 1 si vous câbler sur la même plaque.

### Principe du thread volume

Un **thread** lit en continu le potentiomètre et calcule un **duty cycle** corrigé (**racine carrée** pour une sensation sonore plus linéaire). La boucle principale **ne s’occupe que de la fréquence et du rythme** : elle joue les notes et **applique le duty calculé par le thread**. Si le volume tombe très bas, le son est **coupé** (mute).

### Code

```python
from machine import Pin, ADC, PWM
from time import sleep, ticks_ms, ticks_diff
import _thread, math

# --- Buzzer sur GP16 (PWM) ---
buzzer = PWM(Pin(16))
buzzer.duty_u16(0)  # démarrer muet

# --- LED sur GP18 ---
led = Pin(18, Pin.OUT)

# --- Potentiomètre sur GP26 (ADC0) ---
pot = ADC(Pin(26))

# --- Bouton poussoir sur GP20 ---
button = Pin(20, Pin.IN, Pin.PULL_DOWN)

# --- Variables partagées ---
melodie_index = 0             # 0 = mélodie 1, 1 = mélodie 2
_duty_value = 0               # duty courant calculé par le thread volume
_last_irq_ms = 0              # anti-rebond IRQ

# --- Thread: lecture potar + calcul du volume ---
# Calcule en continu un duty (0..32768) avec correction psychoacoustique

def _volume_thread():
    global _duty_value
    # Filtre passe-bas simple pour lisser le volume
    alpha = 0.2
    duty_smoothed = 0
    while True:
        raw = pot.read_u16()                 # 0..65535
        vol = raw / 65535.0                  # 0..1
        vol_corr = math.sqrt(vol)            # courbe plus "linéaire" à l'oreille
        duty_target = int(vol_corr * 32768)  # ~50% max pour limiter la saturation
        duty_smoothed = int(alpha * duty_target + (1 - alpha) * duty_smoothed)
        _duty_value = duty_smoothed
        sleep(0.05)

_thread.start_new_thread(_volume_thread, ())

# --- Définition des mélodies ---
# Mélodie 1 : Happy Birthday (extrait)
notes1 = [
    264, 264, 297, 264, 352, 330,
    264, 264, 297, 264, 396, 352,
    264, 264, 528, 440, 352, 330, 297,
    466, 466, 440, 352, 396, 352
]
durations1 = [
    0.25, 0.25, 0.5, 0.5, 0.5, 1.0,
    0.25, 0.25, 0.5, 0.5, 0.5, 1.0,
    0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1.0,
    0.25, 0.25, 0.5, 0.5, 0.5, 1.0
]

# Mélodie 2 : Frère Jacques (simplifiée)
notes2 = [
    264, 297, 330, 264,
    264, 297, 330, 264,
    330, 352, 396,
    330, 352, 396,
    396, 440, 396, 352, 264,
    396, 440, 396, 352, 264
]
durations2 = [
    0.5, 0.5, 0.5, 0.5,
    0.5, 0.5, 0.5, 0.5,
    0.5, 0.5, 1.0,
    0.5, 0.5, 1.0,
    0.25, 0.25, 0.25, 0.25, 1.0,
    0.25, 0.25, 0.25, 0.25, 1.0
]

melodies = [(notes1, durations1), (notes2, durations2)]

# --- IRQ: changer de mélodie ---

def _changer_melodie(pin):
    global melodie_index, _last_irq_ms
    now = ticks_ms()
    if ticks_diff(now, _last_irq_ms) < 200:  # anti-rebond ~200 ms
        return
    _last_irq_ms = now
    melodie_index = (melodie_index + 1) % len(melodies)
    print("👉 Mélodie changée :", melodie_index)

button.irq(trigger=Pin.IRQ_RISING, handler=_changer_melodie)

# --- Boucle principale ---
while True:
    notes, durations = melodies[melodie_index]

    # Coupure si volume très faible (mute logiciel)
    if _duty_value < 50:
        buzzer.duty_u16(0)
        sleep(0.1)
        continue

    for freq, d in zip(notes, durations):
        # Mute immédiat si volume retombe à ~0
        if _duty_value < 50:
            buzzer.duty_u16(0)
            break

        buzzer.freq(freq)
        buzzer.duty_u16(_duty_value)  # volume fixé par le thread

        led.value(1)
        sleep(d)
        led.value(0)

        buzzer.duty_u16(0)  # petite pause entre les notes
        sleep(0.05)

    sleep(1)  # pause entre répétitions
```

### Points clés

* **Volume dans un thread séparé** : la lecture `ADC` et le calcul du duty sont **asynchrones**, ce qui évite les à-coups lors du jeu des notes.
* **Correction psychoacoustique** : `sqrt()` réduit la sensation de non-linéarité du potentiomètre.
* **Anti-rebond** pour le bouton via `ticks_ms()`.
* **Sécurité** : on limite le duty à ~50% (`32768`) pour éviter la saturation du buzzer (souvent inutile au-delà et parfois désagréable).

### Utilisation

1. Régler le potentiomètre au-dessus de zéro pour activer le son.
2. Appuyer sur le bouton (**GPIO20**) pour **alterner** entre les deux mélodies.
3. Tourner le potentiomètre pour **monter/descendre le volume** en temps réel.

---
