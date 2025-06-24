from Book import Book
from lib.mqttHelpers import connectToMQTT, sendTopic
from machine import Pin, UART
from time import sleep
from buzzer import soundBuzzer
from ledLight import powerOnLed
from apiCalls import getGoogleBooksData

uart = UART(0, baudrate=600, tx=Pin(0), rx=Pin(1))

powerOnLed('yellow')

print('Redo att skanna')

mqttConnection = connectToMQTT()
sendTopic('{"status": "readyTest"}', "devices/status", mqttConnection)


while True:
   if uart.any():
      soundBuzzer(0.1)
      data = uart.read()
      data = data.decode()
      print("Received:", data)
      googleData = getGoogleBooksData(data)
      newBook = Book()
   sleep(0.1)

