from machine import Pin

greenLed = Pin(17, Pin.OUT)
redLed = Pin(16, Pin.OUT)

def powerOnLed(color):
   if color == 'green':
      print("Powering on green LED")
      greenLed.on()
      redLed.off()
   elif color == 'red':
      redLed.on()
      greenLed.off()
   elif color == 'yellow':
      greenLed.on()
      redLed.on()
   else:
      greenLed.off()
      redLed.off()