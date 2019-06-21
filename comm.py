import time
import paho.mqtt.client as paho
import threading
from time import sleep
from queue import Queue
from wx.lib.pubsub import pub

broker="broker.hivemq.com"
broker="iot.eclipse.org"

#note - even the code publish 4 messages, only the last one will be retained!
# http://www.steves-internet-guide.com/mqtt-retained-messages-example/

flag = 0
out_q = Queue()

def server_send(otherside):
    print ("server send start")
    global flag
    client= paho.Client(otherside+"client-001") 
    print("connecting to broker ",broker)
    client.connect(broker)#connect
    while flag == 1:
        if out_q.empty() == False:
            data = out_q.get()     
                       
            #msg = data.encode('latin-1')
            topic = "Morris-"+otherside
            #print (topic, data) 
            client.publish(topic,data)#publish
            
            
        sleep(0.05)


def on_message(client, userdata, message):
    time.sleep(1)
    client_info_str = str(message.payload.decode("utf-8"))
    #print("received message =", message.topic, client_info_str)
    pub.sendMessage("update", msg="server response " +client_info_str)


def server_recv(myside,otherside):
    global flag
    
    client= paho.Client(myside+"client-002") 
    client.on_message=on_message
    print("connecting to broker ",broker)
    client.connect(broker)#connect
    client.loop_start() #start loop to process received messages
    
    topic = "Morris-"+myside
    print("subscribing ", topic)
    data=""
    client.publish(topic,data,retain=True) #clear retain message
    time.sleep(10)
    client.subscribe(topic)#subscribe
    time.sleep(10)

    flag = 1
    sendThread = threading.Thread(target=server_send, args=(otherside,))
    sendThread.start()

    while(flag == 1):
        sleep(0.2) 

#this is for testing - run python comm.py just to check it is working
def main():
    client= paho.Client("client-002") 
    client.on_message=on_message
    print("connecting to broker ",broker)
    client.connect(broker)#connect
    client.loop_start() #start loop to process received messages
    print("subscribing ")
    client.subscribe("Morris-server")#subscribe
    time.sleep(10)

    flag = 1
    

    while(flag == 1):
        sleep(0.2) 

if __name__ == "__main__":
    main()