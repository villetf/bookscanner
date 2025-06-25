import json
from Book import Book
from constructBook import constructBook
from mqttHelpers import connectToMQTT, sendTopic
from machine import Pin, UART
from time import sleep
from buzzer import soundBuzzer
from ledLight import powerOnLed
from apiCalls import getGoogleBooksData, getOpenLibraryData

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

powerOnLed('yellow')

print('Redo att skanna')

mqttConnection = connectToMQTT()
sendTopic('{"status": "readyTest"}', "devices/status", mqttConnection)


while True:
   if (not mqttConnection) or (not mqttConnection.is_connected()):
      print("Reconnecting to MQTT...")
      mqttConnection = connectToMQTT()

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
      sendTopic(jsonBook, "books/new", mqttConnection)
   sleep(0.1)

