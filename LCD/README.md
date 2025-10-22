# Dossier LCD – MicroPython (Raspberry Pi Pico W)

## Description générale

Le projet **LCD** illustre la conception d’un **système de régulation de température** à base de **Raspberry Pi Pico 2W**, programmé en **MicroPython**.  
Il combine plusieurs capteurs et actionneurs pour afficher, comparer et signaler la température ambiante par différents moyens visuels et sonores.

Ce projet fait partie du module **Entrées/Sorties analogiques et numériques** du Pico 2W.

---

## Objectif du projet

Mettre en œuvre un **mini-thermostat interactif** capable de :

- Lire une **valeur de consigne** à l’aide d’un **potentiomètre analogique (A0)**.  
  → La consigne varie entre **15 °C et 35 °C**.  
- Lire la **température réelle** via un **capteur DHT11** (humidité également disponible).  
- Afficher ces deux valeurs sur un **écran LCD1602 I²C** :
Set: XX C
Amb: YY C
- Comparer les deux températures et réagir en conséquence :

| Condition | LED | Buzzer | LCD |
|------------|------|---------|------|
| T° ≤ Consigne | Battement progressif (dimmer) | OFF | Affiche Set / Amb |
| T° > Consigne | Clignotement 0,5 Hz | OFF | Affiche Set / Amb |
| T° > Consigne + 3 °C | Clignotement rapide | ON | Mot **ALARM** clignotant puis défilant |

---

## Matériel & câblage

| Composant | Broche Pico | Détails |
|------------|-------------|---------|
| Potentiomètre | GP26 (A0) | Entrée analogique pour la consigne |
| LED | GP18 | Sortie PWM (battement / clignotement) |
| Buzzer | GP20 | Sortie PWM pour alarme sonore |
| Capteur DHT11 | GP16 | Entrée numérique – mesure T° / H% |
| Écran LCD1602 I²C | SDA = GP8 / SCL = GP9 | Adresse : 0x3E (selon module Grove) |
| Alimentation | 3.3 V | GND commun |

> Conseil : si le DHT11 échoue parfois à lire, prévoir un délai d’environ 2 s entre deux mesures.

---

## Structure du dossier


---

## Fonctionnement du programme

1. Lecture du **potentiomètre** → conversion en température de consigne (15–35 °C).  
2. Lecture du **DHT11** → obtention de la température et de l’humidité ambiantes.  
3. Affichage permanent des deux valeurs sur le LCD.  
4. Comparaison entre température ambiante et consigne :  
   - Si température normale → effet *dimmer* (LED progressive).  
   - Si température légèrement élevée → LED 0,5 Hz.  
   - Si température > consigne + 3 °C → **alarme visuelle + sonore** :  
     - LED clignote vite.  
     - Buzzer activé.  
     - Mot *ALARM* qui clignote puis défile sur l’écran.

---

## Fichiers importants

### `main.py`
Contient la logique principale du thermostat :
- gestion des entrées/sorties,
- lecture du capteur,
- affichage et alarmes.

### `DHT/DHT.py`
Classe simplifiée pour faciliter la lecture de temperature et de l'humidité :


### `LCD/LCD.py`
Classe simplifiée pour afficher facilement du texte sur le LCD :
```python
lcd.message("Texte ligne 1", "Texte ligne 2")
lcd.scroll_text("Texte long à défiler")

