import socket
from threading import Thread


TCP_IP = 'localhost'    # the ip of the server (localhost = your own ip)
TCP_PORT = 9001         # the port of the server
BUFFER_SIZE = 1024


class ClientThread(Thread):                                     # makes the class clientThread

    def __init__(self, ip, port, sock):                         # constructor
        Thread.__init__(self)
        self.ip = ip                                            # gets the ip from the client
        self.port = port                                        # gets the port from the client
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))      # prints a string with the ip and port of the client

    def run(self):                                #
        filename = 'farmhouse-ground-floor.jpg'
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)               #
            while (l):
                self.sock.send(l)                 #
                # print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)           #
            if not l:
                f.close()                         #
                self.sock.close()                 #
                break


# create a stream socket and bind it
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    s.listen(5)     # sets the backlog to 5
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = s.accept()     # accepts the clients
    print('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, conn)        # creates a new thread for the connected client
    newthread.start()       # starts the new threads/clients activety
    threads.append(newthread)       # adds newthreaad to a list

