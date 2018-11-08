import socket
import cv2

TCP_IP = 'localhost'    # connects to localhost (your own pc)
TCP_PORT = 9001         # the port to conect to
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

with open('received_file', 'wb') as f:  # change received_file to desired name of the file
    print('file opened')
    while True:
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print ('file close()')
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
img = cv2.imread("test_file")
cv2.imshow("test", img)
print('connection closed')