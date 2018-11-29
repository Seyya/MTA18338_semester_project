import socket
import struct
from threading import Thread
import cv2

IP = str(socket.gethostbyname(socket.gethostname()))    # the ip of the server (localhost = your own ip)
PORT = 9001         # the port of the server
BUFFER_SIZE = 1024


class ClientThread(Thread):                                     # makes the class clientThread

    def __init__(self, ip, port, sock):                         # constructor
        Thread.__init__(self)
        self.ip = ip                                            # gets the ip from the client
        self.port = port                                        # gets the port from the client
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))      # prints a string with the ip and port of the client

    def run(self):                                # Function for file transfer
        request = conn.recv(BUFFER_SIZE)
        i_am_sending = False
        if len(request) == 1:
            i_am_sending = struct.unpack('?', request)
        if i_am_sending:
            filename = 'farmhouse-ground-floor2.jpg'  # initializing variable with an image
            f = open(filename, 'rb')  # Variable that checks if the file can be opened and read in a binary mode
            while True:
                l = f.read(BUFFER_SIZE)  # Reads the image with a given buffer size (1024)
                while (l):
                    self.sock.send(l)  # As long as l is true it sends the image
                    # print('Sent ',repr(l))
                    l = f.read(
                        BUFFER_SIZE)  # having a second buffer allows the thread to read from two different buffers to inrease transfer speed
                if not l:
                    f.close()  # Closes the file and its availablility
                    self.sock.close()  # closes the socket
                    break
        else:
            message = struct.unpack('hhhhhh', request)
            playerList = []
            amount = 0
            while amount < 6:
                playerList.append(message[amount: amount + 2])
                amount += 2
            print(playerList)
            img = cv2.imread('farmhouse-ground-floor.jpg')
            img_copy = img.copy()
            cv2.imshow('copy', img_copy)
            for pc in playerList:
                cv2.circle(img_copy, (pc[0]*5, pc[1]*3), 50, (255, 0, 0), -1)
            cv2.imwrite('farmhouse-ground-floor2.jpg', img_copy)


# create a stream socket and bind it
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creates a socket for IPv4 addresses with TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # To set options at a socket level, makes the socket use itself and reuse its address
s.bind((IP, PORT))                          # binds the socket to a TCP ip and port
threads = []                                        # Empty threads array
print('Ip Address of the Server::%s' % IP)
while True:
    s.listen(5)                                     # listen to incoming connections to the socket and sets the backlog to 5
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = s.accept()                 # accepts the clients
    print('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, conn)        # creates a new thread for the connected client
    newthread.start()                               # starts the new threads/clients activety
    threads.append(newthread)                       # adds newthreaad to a list

