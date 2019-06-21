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
    while True:
        if out_q.empty() == False:
            data = out_q.get()
            client_socket.send(data.encode('ascii'))
        sleep(0.05)

def server_recv():
    """Run Worker Thread."""
    print ("server recv start")
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0',8820))

    server_socket.listen(1)

    (client_socket, client_address) = server_socket.accept()
    print ("client connect")

    sendThread = threading.Thread(target=server_send, args=(client_socket, client_address))
    sendThread.start()

    while True:
        client_info = client_socket.recv(1024)
        client_info_str = client_info.decode('ascii')
        if client_info_str == "":
            client_socket.close()
            server_socket.close()
            print ("client close the socket")
            sys.exit()
        print ("server got: " + client_info_str)
        pub.sendMessage("update", msg="server response " +client_info_str)
