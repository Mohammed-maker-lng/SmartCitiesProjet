from machine import Pin, ADC, PWM
from time import sleep
import _thread, math

# --- Buzzer sur GP16 ---
buzzer = PWM(Pin(16))

# --- LED sur GP15 ---
led = Pin(18, Pin.OUT)

# --- Potentiomètre sur GP26 ---
pot = ADC(Pin(26))
valeur_pot = 0   # valeur lue par le potentiomètre

# --- Bouton poussoir sur GP14 ---
button = Pin(20, Pin.IN, Pin.PULL_DOWN)
melodie_index = 0   # 0 = première mélodie, 1 = deuxième mélodie

# --- Lecture du potentiomètre dans un thread ---
def lire_pot():
    global valeur_pot
    while True:
        valeur_pot = pot.read_u16()
        sleep(0.1)

# Lancer le thread
import _thread
_thread.start_new_thread(lire_pot, ())

# --- Définition des mélodies ---
# Mélodie 1 : Happy Birthday
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

# Liste des mélodies disponibles
melodies = [(notes1, durations1), (notes2, durations2)]

# --- Fonction appelée en interruption quand on appuie sur le bouton ---
def changer_melodie(pin):
    global melodie_index
    melodie_index = (melodie_index + 1) % len(melodies)
    print("👉 Mélodie changée :", melodie_index)

# Attacher l’interruption sur front montant (pression du bouton)
button.irq(trigger=Pin.IRQ_RISING, handler=changer_melodie)

# --- Boucle principale ---
while True:
    notes, durations = melodies[melodie_index]

    # Si le potentiomètre est à 0 → coupe le son
    if valeur_pot < 500:
        buzzer.duty_u16(0)
        sleep(0.1)
        continue

    # Joue la mélodie sélectionnée
    for freq, d in zip(notes, durations):
        # Arrêt immédiat si volume tombe à 0
        if valeur_pot < 500:
            buzzer.duty_u16(0)
            break

        buzzer.freq(freq)

        # --- Volume progressif avec correction ---
        vol_norm = valeur_pot / 65535
        vol_corr = math.sqrt(vol_norm)
        duty = int(vol_corr * 32768)  # ~50% max duty
        buzzer.duty_u16(duty)

        # --- LED clignote en même temps que la note ---
        led.value(1)
        sleep(d)
        led.value(0)

        # Pause courte entre les notes
        buzzer.duty_u16(0)
        sleep(0.05)

    sleep(1)  # pause entre chaque répétition
