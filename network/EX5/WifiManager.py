# wifi_manager.py
import network
import time
import ntptime
import machine

class WifiManager:
    def __init__(self):
        try:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
        except Exception as e:
            print("Erreur lors de l'initialisation du Wi-Fi :", e)
            self.wlan = None

    def scanner(self):
        """Affiche les réseaux Wi-Fi disponibles."""
        if self.wlan is None:
            print("Wi-Fi non initialiser.")
            return

        try:
            reseaux = self.wlan.scan()
            print("Réseaux Wi-Fi disponibles :")
            for net in reseaux:
                ssid = net[0].decode()
                print(f"- {ssid}")
        except Exception as e:
            print("Erreur pendant le scan Wi-Fi :", e)

    def connecter(self, ssid, password, timeout=10):
        if self.wlan is None:
            print("Wi-Fi non initialiser.")
            return False

        try:
            print(f"Connexion à '{ssid}' ...")
            self.wlan.connect(ssid, password)

            t0 = time.time()
            while not self.wlan.isconnected() and (time.time() - t0) < timeout:
                time.sleep(0.5)

            if self.wlan.isconnected():
                print("Connecté !")
                print("Config réseau :", self.wlan.ifconfig())
                return True
            else:
                print("Impossible de se connecter (timeout).")
                return False

        except Exception as e:
            print("Erreur pendant la connexion Wi-Fi :", e)
            return False

    def sync_ntp(self, tz_offset_hours=1):
        try:
            # appelle le serveur NTP et met l'heure système en UTC
            print("Synchronisation NTP...")
            ntptime.host = "pool.ntp.org"
            ntptime.settime()
            print("UTC synchronisé.")

            now = time.time() + int(tz_offset_hours * 3600)
            t = time.localtime(now)
            rtc = machine.RTC()
            # (year, month, day, weekday, hours, minutes, seconds, subseconds)
            rtc.datetime((t[0], t[1], t[2], t[6], t[3], t[4], t[5], 0))
            print("Heure locale mise à jour :", "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5]))
            return True

        except Exception as e:
            print("Erreur lors de la synchronisation NTP :", e)
            return False
