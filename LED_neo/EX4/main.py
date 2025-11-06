from time import ticks_ms, ticks_diff, sleep_ms
from sound import SoundDetector
from rgb import RGBLed

def main():
    s = SoundDetector()
    led = RGBLed()
    last_minute = ticks_ms()
    while True:
        if s.detect_beat():
            led.random_color()
        bpm = s.get_instant_bpm()
        now = ticks_ms()
        if ticks_diff(now, last_minute) >= 60000:
            if bpm > 0:
                try:
                    with open("bpm_log.txt", "a") as f:
                        f.write("BPM: {}\n".format(bpm))
                except:
                    pass
            last_minute = now
        sleep_ms(20)

main()
