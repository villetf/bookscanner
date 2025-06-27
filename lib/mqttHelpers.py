from lib.mqtt import MQTTClient
import config.keys as keys


def connectToMQTT():
   try:
      client = MQTTClient(client_id=keys.MQTT_CLIENT_ID, server=keys.MQTT_SERVER, port=keys.MQTT_PORT)
      try:
         client.connect()
      except Exception as e:
         print(f"Failed connecting to MQTT: {e}")
      print("Connected to MQTT on %s" % (keys.MQTT_SERVER))
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