#in this code you run the server and then run the client
# the server has gui(wx) and the client is just console
# 
# in the client you run command like 4 14 - it means take coin 4 and put it on station 14 on board
# this message is send by tcp message to server side port 8820. 
# in the server there are 3 threads 
#   wx thread
#   server rcv messages from client
#   server send messages to client
# once the server rcv command from client like 4 14 , it send it to wx thread by pub/sub method
# and once the wx thread got the info from clinet, it move black coin to station 14
# then the user move with mouse one of white coins and put it on some station.
# once the drag/drop method finished, event is create , the code check if the white coin is on 
# one of 24 stations. if it is there, then wx thread send in QUEUE some message to server_send thread
# the server_send is wait on out_q for internal messages. once he got it
# it send message to the client with the number of station that coin was moved


import threading
import socket
import sys
import wx 
from threading import Thread
from wx.lib.pubsub import pub
import graph 
from time import sleep
from queue import Queue

from enum import Enum
class Color(Enum):
    BLACK = 0
    WHITE = 1

flag = 0
out_q = Queue()

def server_send(client_socket, client_address):
    print ("server send start")
    global flag
    while flag == 1:
        if out_q.empty() == False:
            data = out_q.get()
            client_socket.send(data.encode('ascii'))
        sleep(0.05)

def server_recv():
    global flag
    port = 8820
    print ("server recv start")
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0',port))

    server_socket.listen(1)

    (client_socket, client_address) = server_socket.accept()
    print ("client accept from {0} at port {1}".format(client_address, port))
    client_socket.settimeout(300)

    flag = 1
    sendThread = threading.Thread(target=server_send, args=(client_socket, client_address))
    sendThread.start()

    while(1):
        try:
            client_info = client_socket.recv(1024)
        except Exception as e:
            flag = 0
            sleep(0.2) #let the server_send thread to be close
            print (e)
            client_socket.close()
            (client_socket, client_address) = server_socket.accept() #be ready for next client
            client_socket.settimeout(300)
            print ("client accept from {0} at port {1}".format(client_address, port))
            continue
        # if the code will not check empty string,then once the client terminate,
        # the server will continusly will get empty string
        if client_info == "":
            flag = 0
            sleep(0.2) #let the server_send thread to be close
            client_socket.close()
            print ("client close the socket")
            (client_socket, client_address) = server_socket.accept()
            print ("client accept from {0} at port {1}".format(client_address, port))
            client_socket.settimeout(300)
            continue
        client_info_str = client_info.decode('ascii')
        print ("server got: " + client_info_str)
        pub.sendMessage("update", msg="server response " +client_info_str)




    
