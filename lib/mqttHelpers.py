from time import sleep

from lib.mqtt import MQTTClient
import keys


def connectToMQTT():
   try:
      client = MQTTClient(client_id=keys.MQTT_CLIENT_ID, server=keys.MQTT_SERVER, port=keys.MQTT_PORT)
      sleep(0.1)
      client.connect()
      print("Connected to %s" % (keys.MQTT_SERVER))
      return client
   except Exception as error:
      print("Failed to connect to MQTT server: %s" % error)



def sendTopic(topicObject, topicName, client):
   print(topicObject)
   print(client)
   try:
      client.publish(topic=topicName, msg=topicObject)
      print("DONE")
   except Exception as e:
      print("FAILED")
      print(e)
      # We must add error hadling here if WiFi being unavailable here