# import necessary packages
import socket
import struct

import cv2

IP = input('Enter the IP Address::')  # make the user input the IP adress to connect to (displayed when hosting server)
# IP = "172.24.218.155"  # for hardcoding IP addr
PORT = 9001  # the port to conect to
BUFFER_SIZE = 1024  # the buffer size


# function to receive background from server
def recieve_bg():
    # connect to a socket and send a boolean message (True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.send(struct.pack('?', True))
    # save the image
    with open('received_file.jpg', 'wb') as f:  # change received_file to desired name of the file
        # print('file opened')
        while True:
            data = s.recv(BUFFER_SIZE)
            # print('data=%s', (data))
            if not data:
                f.close()
                # print('file close()')
                break
            # write image data to a file
            f.write(data)

    # print confirmation for a recieved file, close the socket and return the image to the function caller
    # print('Successfully get the file')
    s.close()
    img = cv2.imread("received_file.jpg")
    return img


# function to send position information to the server
def send_pos(pc_list):
    # connect to a socket and delare a message
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    message = None
    # for each position in the list of positions parsed to the function as argument, add 2 integers to the byte message
    for pc in pc_list:
        if message is None:
            message = struct.pack('hh', pc.x, pc.y)
        else:
            message += struct.pack('hh', pc.x, pc.y)
    # when all positions and the signature for them have been added to the message, send it, and close the socket
    s.send(message)
    s.close()
