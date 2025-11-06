# Projet MicroPython – Détection sonore + LED RGB

## Description
Ce projet a pour but de réaliser un petit système “audio-reactif” avec un Raspberry Pi Pico équipé d’un Grove Shield. Le principe est simple :
1. on écoute le signal provenant d’un micro analogique (branché sur une entrée ADC),
2. on détecte les “pics” (sons plus forts que le bruit de fond),
3. à chaque pic, on change la couleur d’une LED RGB de type NeoPixel,
4. on essaye d’estimer la fréquence de ces pics pour en déduire un BPM approximatif,
5. on enregistre périodiquement ce BPM dans un fichier texte sur la carte.

L’intérêt de ce projet est de séparer le code en plusieurs modules pour que le programme principal (`main.py`) reste lisible et que la partie “capteur” et la partie “LED” puissent être réutilisées dans d’autres exercices.

Le code est organisé en **trois fichiers** :

- `main.py` : contient la boucle principale, crée les objets des autres modules et orchestre le tout.
- `sound.py` : s’occupe de lire le micro, d’appliquer un seuil, de filtrer les détections trop rapprochées et de calculer un BPM à partir des derniers intervalles détectés.
- `rgb.py` : s’occupe uniquement de la LED NeoPixel (initialisation, changement de couleur, couleur aléatoire).

---

## Matériel
- **Raspberry Pi Pico ou Pico W**
- **Grove Shield pour Pico** (pour avoir les connecteurs A0 / D18 déjà prêts)
- **Micro analogique Grove** branché sur **A0** → côté Pico c’est l’entrée **ADC 26**
- **LED RGB NeoPixel** (1 seul pixel suffit) branchée sur **D18** → côté Pico c’est le **GPIO 18**
- **MicroPython** déjà flashé sur la carte
- Un outil de transfert (Thonny, mpremote, VS Code + extension, …)
---

## Structure du projet

```text
/
├── main.py    ← boucle principale
├── sound.py   ← détection de son + calcul BPM
└── rgb.py     ← gestion LED NeoPixel
