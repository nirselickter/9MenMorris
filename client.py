import sys
import socket

my_socket = socket.socket()
my_socket.connect(("127.0.0.1",8820))

while (1):
    data = input("enter move (coin, number - e.g 4 14):")
    if data == "":
         continue
    my_socket.send(data.encode('ascii'))
    data = my_socket.recv(1024)
    print ("server send:" + data.decode('ascii'))


