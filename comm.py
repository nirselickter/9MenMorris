import threading
import socket
import sys
import wx 
from threading import Thread
from wx.lib.pubsub import pub
import graph 
from time import sleep
from queue import Queue

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
            flag = 1
            sendThread = threading.Thread(target=server_send, args=(client_socket, client_address))
            sendThread.start()
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
            flag = 1
            sendThread = threading.Thread(target=server_send, args=(client_socket, client_address))
            sendThread.start()
            continue
        client_info_str = client_info.decode('ascii')
        print ("server got: " + client_info_str)
        pub.sendMessage("update", msg="server response " +client_info_str)

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


    
