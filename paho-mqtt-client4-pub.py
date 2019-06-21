import time
import paho.mqtt.client as paho
broker="broker.hivemq.com"
broker="iot.eclipse.org"


client= paho.Client("client-001") 
print("connecting to broker ",broker)
client.connect(broker)#connect

#note - even the code publish 4 messages, only the last one will be retained!
# http://www.steves-internet-guide.com/mqtt-retained-messages-example/
for i in range(4):
    msg= "type:put,player:1,x:0,y:"+str(i)
    print (i,msg)
    client.publish("Morris-GI",msg,retain=True)#publish
    time.sleep(2)
client.disconnect() #disconnect

