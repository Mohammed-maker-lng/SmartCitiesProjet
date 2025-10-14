# Dossier AD-PWM – Signaux numériques et modulation de largeur d'impulsion (PWM) du Raspberry Pi Pico W

## Description générale

Le dossier **AD-PWM** regroupe les projets et exercices portant sur la **génération de son avec un buzzer**, la **modulation de largeur d'impulsion (PWM)**, le **clignotement d'une LED en fonction de la mélodie**, et la **possibilité de changer la mélodie via un bouton poussoir** du **Raspberry Pi Pico W**, programmés en **MicroPython**.

Ces projets illustrent comment :

- **Générer des sons avec un buzzer** et **moduler le volume** via un **potentiomètre**, contrôlant ainsi l'intensité sonore du buzzer en fonction de la lecture analogique du potentiomètre.
- **Clignoter une LED** au rythme des notes de la mélodie, synchronisant visuellement l'audio généré par le buzzer.
- **Changer la mélodie** en appuyant sur un **bouton poussoir**, permettant de sélectionner entre différentes mélodies.

Chaque script présent dans ce dossier montre comment manipuler le module **`machine.Pin`** pour générer des signaux à largeur d’impulsion modulée (**PWM**) pour le buzzer et la LED, tout en intégrant la gestion des entrées analogiques via **ADC** pour la variation du volume sonore et l'utilisation des interruptions (**IRQ**) pour changer de mélodie avec le bouton poussoir.

## Projet 1 : Sonnerie (mélodie) sur buzzer **+ volume** géré dans un **thread séparé**

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
