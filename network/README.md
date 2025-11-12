# Fiche de Projet – Horloge NTP + Servo (Raspberry Pi Pico W)

## 1 Contexte & Objectifs
- **Contexte :** Horloge pilotée par Pico W, synchronisée via NTP, affichage 12h/24h, sélection de fuseau par bouton.
- **Objectifs mesurables :**
  - [ ] Connexion Wi-Fi fiable et synchro NTP fonctionnelle
  - [ ] Changement de fuseau (simple clic)
  - [ ] Bascule 12h/24h (double clic)
  - [ ] Contrôle servo en fonction de l’heure

## 2 Architecture 
- `WifiManager.py` : connexion + `sync_ntp(tz_offset_hours)`
- `Servo.py` : PWM 50 Hz, 500–2500 µs → 0–180°
- `main.py` : thread bouton, logique fuseaux/format, boucle principale

## 3 Matériel
- Pico **W** (MicroPython récent)
- **Bouton poussoir** (utilise `Pin.PULL_UP`)
- Câbles 

## 4 Câblage
| Élément | Broche Pico | Remarque |
|---|---:|---|
| Servo (signal) | **GP16** | PWM 50 Hz |
| Bouton | **GP20** | Entrée `PULL_UP` |









