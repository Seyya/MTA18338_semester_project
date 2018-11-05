import numpy as np
import cv2
import time

img = cv2.imread('test2.png', 0)  # greyscale image
# img_color = cv2.imread("test.jpg") # color image
height, width = img.shape[:2]   # dimensions of the image
# H, W = img_color.shape[:2]     # dimensions of the image

img1 = cv2.imread('book.jpg', cv2.IMREAD_GRAYSCALE)  # imports image (used for adaptive thresholding)
resize_img = cv2.resize(img1, (200, 150))     # resizes image to another resolution
img_out = resize_img.copy()                 # makes a copy of the resized image
height = resize_img.shape[0]                # array of the size of the resized image's height
width = resize_img.shape[1]                 # array of the size of the resized image's width

cap = cv2.VideoCapture(0)      # variale used to enable camera


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


def adaptive_thresholding():
    neighbor_pixel = np.zeros((height, width), np.uint8)         # zeros array with the height and width dimension
    # test = np.zeros((height, width), np.uint8)                 # zeros array with the height and width dimension
    # threshold = 100                                            # global threshold, not used for adaptive threshold

    for i in np.arange(1, height-1):                      # loop that goes through the height of the image with offset 1
        for j in np.arange(1, width-1):                    # Loop that goes through the width of the image with offset 1
            sum = 0
            pix_value = resize_img.item(i, j)                   # gets the value of a certain pixel at height/width
            # print("test2", test)
            for k in np.arange(-1, 2):         # loop that goes through the pixels in a 3x3 of the pixel at height/width
                for l in np.arange(-1, 2):     # loop that goes through the pixels in a 3x3 of the pixel at height/width
                    neighbor_pixels = resize_img.item(i+k, j+l)  # Get the value of the pixels in a 3x3 shape
                    print("test", neighbor_pixels)               # prints the values of the pixels
                    sum = sum + (neighbor_pixels / 9)            # gets the mean value of all the pixels
            b = sum                                              # variable that is set to whatever the mean value is
            if pix_value > b:                        # compares pixvalue with mean value to set it to black or white
                b = 255
            else:
                b = 0
            print("b", b)
            img_out.itemset((i, j), b)                          # apply the changes threshold changes to the image


def rgb2grey2image():

    # (1) Loop to calculate
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


# blur = cv2.GaussianBlur(img_out,(5,5), cv2.BORDER_DEFAULT)     #filters to test stuff for adaptive thresholding
# blur = cv2.medianBlur(img, 5)

adaptive_thresholding()

cv2.imshow("test", img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()

# while True:            #for video things

    # ret, frame = cap.read()
    # H = frame.shape[0]
    # W = frame.shape[1]

    # gray = rgb2grey2video()
    # binary = binary_threshold2video()

    # cv2.imshow("Source", binary)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
