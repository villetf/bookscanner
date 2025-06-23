from machine import Pin, UART
from time import sleep
from buzzer import soundBuzzer
from ledLight import powerOnLed
from apiCalls import getGoogleBooksData

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

powerOnLed('yellow')

print('Redo att skanna')


while True:
   if uart.any():
      soundBuzzer(0.1)
      data = uart.read()
      data = data.decode()
      print("Received:", data)
      getGoogleBooksData(data)
   sleep(0.1)

