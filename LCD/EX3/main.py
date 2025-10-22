from machine import Pin, ADC, PWM
from time import sleep, ticks_ms, ticks_diff
from LCD.LCD import LCD
from DHT11.DHT import DHT

# === Initialisation des composants ===
potentiometre = ADC(26)        # résistance variable (A0)
led = PWM(Pin(18))             # LED sur GP18
buzzer = PWM(Pin(20))          # buzzer sur GP20
capteur = DHT(16)              # capteur DHT11 sur GP16
lcd = LCD()                    # écran LCD

led.freq(1000)
buzzer.freq(1000)

# === Variables ===
temperature_ambiante = 25.0
humidite = 0

# === Fonctions utilitaires ===
def convertir_pot_en_temperature(valeur):
    """Convertit la valeur ADC (0–65535) en température entre 15°C et 35°C."""
    return 15 + (valeur / 65535) * 20

def clignoter_led(frequence_hz=0.5, intensite=65535):
    """Fait clignoter la LED à la fréquence donnée (Hz)."""
    periode = 1 / frequence_hz
    led.duty_u16(intensite)
    sleep(periode / 2)
    led.duty_u16(0)
    sleep(periode / 2)

def effet_progressif_led():
    """Fait un battement progressif (dimmer) de la LED."""
    for i in range(0, 65535, 3000):
        led.duty_u16(i)
        sleep(0.005)
    for i in range(65535, 0, -3000):
        led.duty_u16(i)
        sleep(0.005)

def activer_buzzer(etat=True):
    """Active ou désactive le buzzer."""
    buzzer.duty_u16(30000 if etat else 0)

def afficher_alarm_avec_effets():
    """Fait clignoter et défiler le mot 'ALARM' sur le LCD."""
    texte = "    ALARM    "  # espaces pour effet de défilement

    # --- Étape 1 : clignotement 3 fois ---
    for _ in range(3):
        lcd.message("ALARM", "Temp trop elevee")
        sleep(0.4)
        lcd.clear()
        sleep(0.4)

    # --- Étape 2 : défilement horizontal ---
    for i in range(len(texte) - 15):
        lcd.message(texte[i:i+16], "Temp trop elevee")
        sleep(0.2)

# === Boucle principale ===
dernier_temps = ticks_ms()

while True:
    # Lecture toutes les ~1 s
    if ticks_diff(ticks_ms(), dernier_temps) >= 1000:
        dernier_temps = ticks_ms()

        # Lecture du potentiomètre
        valeur_pot = potentiometre.read_u16()
        temperature_consigne = convertir_pot_en_temperature(valeur_pot)

        # Lecture du capteur DHT (si erreur, on garde la dernière valeur)
        nouvelle_temp, nouvelle_hum = capteur.lire_mesures()
        if nouvelle_temp is not None:
            temperature_ambiante = nouvelle_temp
            humidite = nouvelle_hum

        # Affichage normal du LCD
        lcd.message(f"Set: {int(temperature_consigne)}C",
                    f"Amb: {int(temperature_ambiante)}C")

        # Calcul de la différence
        difference = temperature_ambiante - temperature_consigne

        # --- État 1 : Température normale ---
        if difference <= 0:
            activer_buzzer(False)
            effet_progressif_led()

        # --- État 2 : Légèrement trop chaud ---
        elif 0 < difference <= 3:
            activer_buzzer(False)
            clignoter_led(0.5)

        # --- État 3 : Trop chaud (alarme) ---
        elif difference > 3:
            activer_buzzer(True)
            afficher_alarm_avec_effets()
            activer_buzzer(False)

    sleep(0.05)
