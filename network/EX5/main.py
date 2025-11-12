# main.py
import time
import _thread
from machine import Pin
from WifiManager import WifiManager
from Servo import Servo

timezones = [0, 1, -5, 3]
tz_index = 1
format_24h = True

button = Pin(20, Pin.IN, Pin.PULL_UP)

def tache_bouton(wifi):
    global tz_index, format_24h
    clicks = 0
    last_ms = 0

    while True:
        if button.value() == 0:                      # appui
            now = time.ticks_ms()
            if time.ticks_diff(now, last_ms) > 80:   # anti-rebond
                clicks += 1
                last_ms = now
            while button.value() == 0:
                time.sleep_ms(5)

        if clicks > 0 and time.ticks_diff(time.ticks_ms(), last_ms) > 320:
            if clicks == 1:
                tz_index = (tz_index + 1) % len(timezones)
                wifi.sync_ntp(tz_offset_hours=timezones[tz_index])
                print("Fuseau horaire changé :", timezones[tz_index])
            else:
                format_24h = not format_24h
                print("Format 24h :", format_24h)
            clicks = 0

        time.sleep_ms(15)

def main():
    global tz_index, format_24h
    wifi = WifiManager()
    if not wifi.connecter("WiFi-Home-2C40", "wp4r2drjrknne"):
        print("Pas de Wi-Fi : Probleme SSID ou Password")
    else:
        wifi.sync_ntp(tz_offset_hours=timezones[tz_index])
        _thread.start_new_thread(tache_bouton, (wifi,))

    servo = Servo(broche=16)

    while True:
        t = time.localtime()
        heure = t[3]
        minute = t[4]

        angle = int(heure * 180 / 23)
        servo.angle(angle)

        if format_24h:
            txt = "{:02d}:{:02d}".format(heure, minute)
        else:
            h = heure
            ampm = "AM"
            if h == 0:
                h = 12
            elif h == 12:
                ampm = "PM"
            elif h > 12:
                h -= 12
                ampm = "PM"
            txt = "{:02d}:{:02d} {}".format(h, minute, ampm)

        print("Heure", txt, "-> angle", angle)
        time.sleep(30)

main()
