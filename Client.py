import socket                   # Import socket module
import cv2

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
k = 'hello server!'
s.send(k.encode())

with open('test_file', 'wb') as f: #change test_File to desired name of the file
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
img = cv2.imread("test_file")
cv2.imshow("test", img)
cv2.waitKey()