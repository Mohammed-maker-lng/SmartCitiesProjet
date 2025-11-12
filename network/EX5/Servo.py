# servo.py
from machine import Pin, PWM

class Servo:
    def __init__(self, broche=16, freq=50):
        self.pwm = PWM(Pin(broche))
        self.pwm.freq(freq)
        self.min_us = 500
        self.max_us = 2500
        self.period_us = 1000000 // freq  

    def _us_to_duty(self, us):
        return int(us * 65535 // self.period_us)

    def angle(self, deg):
        if deg < 0:
            deg = 0
        if deg > 180:
            deg = 180
        us = self.min_us + (self.max_us - self.min_us) * deg // 180
        duty = self._us_to_duty(us)
        self.pwm.duty_u16(duty)
