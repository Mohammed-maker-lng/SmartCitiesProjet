from machine import ADC
from time import ticks_ms, ticks_diff

class SoundDetector:
    def __init__(self, adc_pin=26, seuil=18000, min_interval_ms=200):
        self.adc = ADC(adc_pin)
        self.seuil = seuil
        self.min_interval_ms = min_interval_ms
        self.last_beat_ms = 0
        self.beat_intervals = []

    def read_level(self):
        return self.adc.read_u16()

    def detect_beat(self):
        v = self.read_level()
        now = ticks_ms()
        if v > self.seuil and ticks_diff(now, self.last_beat_ms) > self.min_interval_ms:
            if self.last_beat_ms != 0:
                interval = ticks_diff(now, self.last_beat_ms)
                self.beat_intervals.append(interval)
                if len(self.beat_intervals) > 20:
                    self.beat_intervals.pop(0)
            self.last_beat_ms = now
            return True
        return False

    def get_instant_bpm(self):
        if not self.beat_intervals:
            return 0
        s = sum(self.beat_intervals) / len(self.beat_intervals)
        if s == 0:
            return 0
        return int(60000 / s)
