from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(15, Pin.OUT))

def soundBuzzer(duration):
   buzzer.freq(2000)
   buzzer.duty_u16(32768)
   sleep(duration)
   buzzer.duty_u16(0)
   sleep(0.05)