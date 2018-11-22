import socket
import struct

import cv2


class Client:
    MESSAGE = ""

    def __init__(self, x, y):
        self.MESSAGE = struct.pack('hh', x, y)

    def discourse(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(self.MESSAGE)
        # data = s.recv(BUFFER_SIZE)
        # data = struct.unpack('hh', data)
        s.close()


#        print("received data: ", data)


class Admin:
    BACKGROUND = None

    def __init__(self, image):
        self.BACKGROUND = image

    def discourse(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(self.BACKGROUND)
        data = s.recv(BUFFER_SIZE)
        # data = struct.unpack('hh', data)
        s.close()

        print("received data: ", data)


adam = Admin(cv2.imread("chickens01.jpg"))
adam.discourse()

a = Client(5, 5)
a.discourse()

b = Client(2, 2)
a.discourse()

c = Client(9, 3)
c.discourse()
