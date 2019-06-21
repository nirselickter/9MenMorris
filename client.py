import threading
import socket
import sys
import wx 
from threading import Thread
from wx.lib.pubsub import pub
import graph 
from time import sleep
from queue import Queue

out_q = Queue()

def client_recv(my_socket):
    while True:
        data = my_socket.recv(1024)
        data = data.decode('ascii')
        print ("server send:" + data )
        pub.sendMessage("update", msg="server response " +data)

def client_send():
    print("start client")
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1",8820))

    recvThread = threading.Thread(target=client_recv, args=(my_socket,))
    recvThread.start()

    while True:
        if out_q.empty() == False:
            data = out_q.get()
            my_socket.send(data.encode('ascii'))
        sleep(0.05)

