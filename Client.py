import socket
import struct

import cv2

# IP = input('Enter the IP Address::')  # connects to localhost (your own pc)
IP = "172.24.222.5"
PORT = 9001  # the port to conect to
BUFFER_SIZE = 1024


def recieve_bg():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.send(struct.pack('?', True))
    with open('received_file.jpg', 'wb') as f:  # change received_file to desired name of the file
        print('file opened')
        while True:
            data = s.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print('file close()')
                break
            # write data to a file
            f.write(data)

    print('Successfully get the file')
    s.close()
    img = cv2.imread("received_file.jpg")
    return img


def send_pos(pc_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    message = None
    for pc in pc_list:
        if message is None:
            message = struct.pack('hh', pc.x, pc.y)
        else:
            message += struct.pack('hh', pc.x, pc.y)
    s.send(message)
    s.close()
