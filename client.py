import sys
import socket


def checkCommand(val):
    try:
        info = val.split(" ")
        #print("111", info)
        if len(info) == 2:
            if info[0] == "put":
                #print("222")
                v = int(info[1])
                if 1<=v and v<=24:
                    #print("333")
                    return True
        elif len(info) == 3:
            if info[0] == "move":
                v = int(info[1])
                v1 = int(info[2])
                if v != v1:                  
                    if 1<=v and v<=24:
                        if 1<=v1 and v1<=24:
                            return True
    except Exception as e:
        print("illegal command")
        return False
    #if we are here the command is illegal
    print("illegal command")
    return False

def main():
    print("start client")
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1",8820))

    while (1):
        data = input("enter command:\n\tput number - e.g put 14\n\tmove number number e.g move 4 5:\n")
        if data == "":
             continue
        val = checkCommand(data) 
        if val == False:
            continue
        my_socket.send(data.encode('ascii'))
        data = my_socket.recv(1024)
        print ("server send:" + data.decode('ascii'))


if __name__ == "__main__":
    main()