# 🧠 Projet Raspberry Pi Pico W – MicroPython

## 🔍 Description générale
Ce dépôt contient l’ensemble des exercices et ressources liés à l’utilisation du **Raspberry Pi Pico W** avec **MicroPython**.  
Chaque sous-répertoire correspond à un thème ou à un ensemble d’expériences pratiques.

---

## ⚙️ 1. Raspberry Pi Pico W

Le **Raspberry Pi Pico W** est une carte de développement basée sur le microcontrôleur **RP2040** double cœur ARM Cortex-M0+ cadencé à 133 MHz.  
Elle dispose de :
- **26 broches GPIO** utilisables pour le numérique, l’analogique, la PWM, l’I²C, le SPI et l’UART.
- **Mémoire** : 264 Ko de RAM et 2 Mo de Flash.
- **Connectivité Wi-Fi** intégrée (module Infineon CYW43439).
- **Alimentation** via USB 5 V ou entrée 3.3 V.

### 📸 Brochage (Pinout)
![Brochage du Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)
> Source : [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)

---

## 🐍 2. MicroPython

**MicroPython** est une implémentation légère du langage Python conçue pour les microcontrôleurs.  
Elle permet de programmer le Pico W très facilement, avec une syntaxe identique à Python classique.

### Avantages :
- Syntaxe simple et lisible  
- Exécution directe sur le microcontrôleur  
- Possibilité d’utiliser le **REPL** (console interactive) pour tester les commandes en temps réel

---

## 🧰 3. Environnement de travail

### Logiciels utilisés :
- **Thonny IDE** : environnement simple pour écrire et transférer le code vers le Pico W.
- **Drivers** USB du Pico (installés automatiquement via Thonny).
- **Git / GitHub** : pour la gestion de versions et le partage du code.
- **VS Code** (optionnel) pour l’édition de fichiers en local.

---

## 📂 4. Structure du dépôt

Ce dépôt est organisé en plusieurs sous-répertoires, chacun avec son propre fichier `README.md` décrivant le contenu.

| Répertoire | Description |
|-------------|--------------|
| [GPIO](./GPIO) | LED simple, bouton-poussoir, interruption |
| [AD-PWM](./AD-PWM) | Lecture du potentiomètre, PWM (LED, musique, servo) |
| [LCD](./LCD) | Documentation des fonctions de la librairie, affichage du potentiomètre |
| [LED_neo](./LED_neo) | Utilisation des LEDs Neopixel, documentation, effets arc-en-ciel |
| [sensors](./sensors) | Mesures : température, humidité, luminosité, détection PIR |
| [network](./network) | Accès réseau avec le RPi Pico W |

---

## 📚 5. Ressources utiles

- [Documentation officielle Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/)
- [Tutoriels MicroPython](https://docs.micropython.org/en/latest/)
- [Brochage PDF (Raspberry Pi)](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf)
- [Téléchargement de Thonny IDE](https://thonny.org/)

---

## 👨‍💻 Auteur
Projet réalisé dans le cadre du cours **IoT – Smart Systems** à la **HEPL**,  
par *Mohammed Al-Zubaidi*.

Licence : [MIT License](./LICENSE)
