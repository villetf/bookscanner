import json
from Book import Book
from constructBook import constructBook
from mqttHelpers import connectToMQTT, sendTopic
from machine import Pin, UART
from time import sleep
from buzzer import soundBuzzer
from ledLight import powerOnLed
from apiCalls import getGoogleBooksData, getOpenLibraryData



try:
   mqttConnection = connectToMQTT()
   soundBuzzer(0.1)
   soundBuzzer(0.1)
except:
   print("Initial MQTT connection failed")

powerOnLed('yellow')
print('Redo att skanna')


uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

powerOnLed('green')
while True:
   if uart.any():
      soundBuzzer(0.1)
      isbn = uart.read()
      isbn = isbn.decode()
      isbn = isbn.strip()
      print("Received:", isbn)
      googleData = getGoogleBooksData(isbn)
      openLibraryData = getOpenLibraryData(isbn)
      newBook = constructBook(isbn, googleData, openLibraryData)
      jsonBook = json.dumps(newBook.__dict__).encode('utf-8')
      print('längd på meddelande:', len(jsonBook))
      try:
          sendTopic(jsonBook, "books/new", mqttConnection)
      except:
          print("Failed sending book via MQTT")
   sleep(0.1)

