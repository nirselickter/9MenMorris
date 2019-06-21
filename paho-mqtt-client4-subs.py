import time
import paho.mqtt.client as paho
broker="broker.hivemq.com"
broker="iot.eclipse.org"

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", message.topic, str(message.payload.decode("utf-8")))

client= paho.Client("client-001") 
client.on_message=on_message
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("Morris-GI")#subscribe
time.sleep(10)
#the code exit after 10 seconds
