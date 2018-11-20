# https://docs.python.org/3/library/socket.html

import socket
import struct
import threading


class Server:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Normally 1024  # 20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    print("listening on %s:%d" % (TCP_IP, TCP_PORT))

    def handle_client(client_socket):
        request = client_socket.recv(1024)
        pos1, pos2 = struct.unpack('hh', request)
        print("Client:  (%d:%d)" % (pos1, pos2))

        response = struct.pack('hh', pos1, pos2)
        client_socket.send(response)
        client_socket.close()

    while True:
        client, addr = s.accept()
        print("Connecting...")
        print('Connection address: ', addr)
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
