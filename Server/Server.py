# import necessary packages
import socket
import struct
from threading import Thread

import cv2

IP = str(socket.gethostbyname(socket.gethostname()))    # the ip of the server (localhost = your own ip)
PORT = 9001         # the port of the server
BUFFER_SIZE = 1024  # the buffer size


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
        # depending on the length of the request (boolean is 1 and positions are > 1), interpret received data
        if len(request) == 1:
            i_am_sending = struct.unpack('?', request)
        # if image request was given in the above line (True)
        if i_am_sending:
            filename = 'maps/perfect_Ratio_map.jpg'  # initializing variable with an image
            f = open(filename, 'rb')  # Variable that checks if the file can be opened and read in a binary mode
            while True:
                l = f.read(BUFFER_SIZE)  # Reads the image with a given buffer size (1024)
                while (l):
                    self.sock.send(l)  # As long as l is true it sends the image
                    # A second buffer allows the thread to read from two different buffers to inrease transfer speed
                    l = f.read(BUFFER_SIZE)
                if not l:
                    f.close()  # Closes the file and its availablility
                    self.sock.close()  # closes the socket
                    break
        else:
            # unlike Client, Server does not have a dynamic resizing of the message (this could be done by sending a
            # preliminary message with the amount of players first, followed by the original message)
            h_str = 'hhhhhhhhhhhhhh'  # increase amount of h by 2 for each template

            # unpack the message and add the positions to the playerList
            message = struct.unpack(h_str, request)
            playerList = []
            amount = 0
            while amount < len(h_str):
                playerList.append(message[amount: amount + 2])
                amount += 2
            print(playerList)
            # load a copy of the image to draw positions on, and draw circle unto the new image based on player
            # positions recieved from client. Colours are hardcoded in pc_colours
            img = cv2.imread('../Maps/perfect_ratio_map.jpg')
            img_copy = img.copy()
            cv2.imshow('copy', img_copy)
            pc_colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (127, 127, 0), (0, 127, 127), (127, 0, 127), (2, 2, 2)]
            cc = 0
            for pc in playerList:
                if pc[0] != 0 and pc[1] != 0:
                    cv2.circle(img_copy, (pc[0] * 2 + 100, pc[1] * 2 + 100), 25, pc_colours[cc], -1)
                    cc += 1
                else:
                    cv2.circle(img_copy, (pc[0], pc[1]), 25, pc_colours[cc], -1)
                    cc += 1
            # write the updated image to file (with player locations visualized)
            cv2.imwrite('../Maps/map_with_players.jpg', img_copy)


# create a stream socket and bind it
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creates a socket for IPv4 addresses with TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # To set options at a socket level, makes the socket use itself and reuse its address
s.bind((IP, PORT))  # binds the socket to a TCP ip and port
threads = []  # Empty threads array
print('Ip Address of the Server::%s' % IP)
while True:
    s.listen(5)                                     # listen to incoming connections to the socket and sets the backlog to 5
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = s.accept()                 # accepts the clients
    print('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, conn)        # creates a new thread for the connected client
    newthread.start()                               # starts the new threads/clients activety
    threads.append(newthread)                       # adds newthreaad to a list

