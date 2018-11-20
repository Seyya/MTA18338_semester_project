import socket
import struct


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
        data = s.recv(BUFFER_SIZE)
        data = struct.unpack('hh', data)
        s.close()

        print("received data: ", data)


dennis = Client(9, 2)
autumn = Client(3, 4)
autumn.discourse()
dennis.discourse()
