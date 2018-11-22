import socket
import struct
import threading

import numpy as np


class Server:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Normally 1024  # 20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = []
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    print("listening on %s:%d" % (TCP_IP, TCP_PORT))
    background = np.ndarray

    def handle_client(client_socket, clients):
        request = client_socket.recv(1024)
        if len(request) == 4:  # only 1 player's coordinates recieved
            # pos1, pos2 = struct.unpack('hh', request)
            # add player pos to "players"
            # response = background
            clients[0].send(request)
        else:
            print("Client: Admin")
            if len(clients) > 1:
                for i in range(1, len(clients) - 1):
                    print(i)
                    clients[1].send(request)
            confirmation = struct.pack('hh', 0, 0)
            client_socket.send(confirmation)
            # background = request
            # response = playerpositions
        # client_socket.close()

    while True:
        client, addr = s.accept()
        clients.append(client)
        print("Connecting...")
        print('Connection address: ', addr)
        client_handler = threading.Thread(target=handle_client, args=(client, clients))
        client_handler.start()
