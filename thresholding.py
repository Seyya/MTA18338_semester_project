import numpy as np
import cv2
import time

img = cv2.imread('test2.png', 0)  #greyscale image
#img_color = cv2.imread("test.jpg") #color image
height, width = img.shape[:2]   #dimensions of the image
#H, W = img_color.shape[:2]     #dimensions of the image
cap = cv2.VideoCapture(0)       #variale used to enable camera



def binary_threshold2image():
    threshold = 150

    for i in np.arange(height):
        for j in np.arange(width):
            a = img.item(i, j)
            if a > threshold:
                b = 255
            else:
                b = 0
            img.itemset((i, j), b)


def binary_threshold2video():
    threshold = 150
    ts = time.time()
    gray = np.zeros((H, W), np.uint8)
    binary = np.zeros((H, W), np.uint8)

    for i in range(H):
        for j in range(W):
            gray[i, j] = np.clip(0.07 * frame[i, j, 0] + 0.72 * frame[i, j, 1] + 0.21 * frame[i, j, 2], 0, 255)
            binary[i, j] = gray[i, j]

            if binary[i, j] > threshold:
                b = 255
            else:
                b = 0
            binary.itemset((i, j), b)

    t = (time.time() - ts)
    print("Loop: {:} ms".format(t * 1000))
    return binary



def rgb2grey2image():

    ## (1) Loop to calculate
    ts = time.time()

    gray = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            gray[i, j] = np.clip(0.07 * img_color[i, j, 0] + 0.72 * img_color[i, j, 1] + 0.21 * img_color[i, j, 2], 0, 255)

    t = (time.time() - ts)
    print("Loop: {:} ms".format(t))
    cv2.imshow("gray", gray)


def rgb2grey2video():

    gray = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            gray[i, j] = np.clip(0.07 * frame[i, j, 0] + 0.72 * frame[i, j, 1] + 0.21 * frame[i, j, 2], 0, 255)

    return gray



def rgb2greyOpenCV2image():

    ts = time.time()
    w = np.array([[[0.07, 0.72, 0.21]]])
    gray2 = cv2.convertScaleAbs(np.sum(img_color * w, axis=2))
    t = (time.time() - ts)
    print("Loop: {:} ms".format(t * 1000))
    cv2.imshow("gray2", gray2)


def rgb2greyOpenCV2video():

    w = np.array([[[0.07, 0.72, 0.21]]])
    gray2 = cv2.convertScaleAbs(np.sum(frame * w, axis=2))

    return gray2


while True:
    ret, frame = cap.read()
    H = frame.shape[0]
    W = frame.shape[1]

    #gray = rgb2grey2video()
    binary = binary_threshold2video()

    cv2.imshow("Source", binary)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
