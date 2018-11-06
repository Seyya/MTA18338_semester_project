import time

import cv2
import numpy as np


def binary_threshold2image(img, threshold):
    h, w = img.shape
    for i in np.arange(h):
        for j in np.arange(w):
            a = img.item(i, j)
            if a > threshold:
                b = 255
            else:
                b = 0
            img.itemset((i, j), b)
    return img


def binary_threshold2video(frame, threshold):
    h, w = frame.shape
    ts = time.time()
    gray = np.zeros((h, w), np.uint8)
    binary = np.zeros((h, w), np.uint8)

    for i in range(h):
        for j in range(w):
            gray[i, j] = np.clip(0.07 * frame[i, j, 0] + 0.72 * frame[i, j, 1] + 0.21 * frame[i, j, 2], 0, 255)
            binary[i, j] = gray[i, j]

            if binary[i, j] > threshold:
                b = 255
            else:
                b = 0
            binary.itemset((i, j), b)

    t = (time.time() - ts)
    return binary


def adaptive_thresholding(img):
    #img = cv2.resize(img, (200, 200))   # brug resize hvis billedet er større end 500x500
    height, width = img.shape
    img_out = img.copy()

    for i in range(1, height - 7):  # loop that goes through the height of the image with offset 1
        for j in range(1, width - 7):  # Loop that goes through the width of the image with offset 1
            sum = 0
            pix_value = img.item(i, j)  # gets the value of a certain pixel at height/width

            for k in range(-11, 2):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
                for l in range(-11, 2):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
                    neighbor_pixels = img.item(i + k, j + l)  # Get the value of the pixels in a 3x3 shape
                    sum = sum + neighbor_pixels

            b = sum / 169  # sum of all neighbourhood pixel values divided by amount of pixels to get average pixel value
            if pix_value > b:  # compares pixvalue with mean value to set it to black or white
                b = 255
            else:
                b = 0
            img_out.itemset((i, j), b)  # apply the changes threshold changes to the image
            adapt_thr = img_out.copy()
            print("pos", i,j)
    return adapt_thr


def adaptive_thresholding2video(frame_gray): # needs greyscale frame to work
    #frame_resize = cv2.resize(img, (200, 200))   # brug resize hvis den skal opdater hurtigere, og ændre frame variable til resize variable
    height, width = frame_gray.shape[:2]
    frame_out = np.zeros((height, width), np.uint8)

    for i in range(1, height - 7):  # loop that goes through the height of the image with offset 1
        for j in range(1, width - 7):  # Loop that goes through the width of the image with offset 1
            sum = 0
            pix_value = frame_gray.item(i, j)  # gets the value of a certain pixel at height/width

            for k in range(-11, 2):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
                for l in range(-11, 2):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
                    neighbor_pixels = frame_gray.item(i + k, j + l)  # Get the value of the pixels in a 3x3 shape
                    sum = sum + neighbor_pixels

            b = sum / 169  # sum of all neighbourhood pixel values divided by amount of pixels to get average pixel value
            if pix_value > b:  # compares pixvalue with mean value to set it to black or white
                b = 255
            else:
                b = 0
            frame_out.itemset((i, j), b)  # apply the changes threshold changes to the image
            adapt_thr = frame_out.copy()
            print("pos", i,j)
    return adapt_thr


def rgb2grey2image(img):
    h, w = img
    ts = time.time()

    gray = np.zeros((h, w), np.uint8)
    for i in range(h):
        for j in range(w):
            gray[i, j] = np.clip(0.07 * img[i, j, 0] + 0.72 * img[i, j, 1] + 0.21 * img[i, j, 2], 0, 255)

    t = (time.time() - ts)
    cv2.imshow("gray", gray)


def rgb2grey2video(frame):
    h, w = frame.shape[:2]
    gray = np.zeros((h, w), np.uint8)
    for i in range(h):
        for j in range(w):
            gray[i, j] = np.clip(0.07 * frame[i, j, 0] + 0.72 * frame[i, j, 1] + 0.21 * frame[i, j, 2], 0, 255)

    return gray


def dilateboi(img_arr, iteration):
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Dilation iteration: " + str(it + 1))
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                if img_arr[i, j] == 255:
                    img_new[i - 1, j - 1] = 255
                    img_new[i - 1, j] = 255
                    img_new[i - 1, j + 1] = 255
                    img_new[i, j - 1] = 255
                    img_new[i, j + 1] = 255
                    img_new[i + 1, j - 1] = 255
                    img_new[i + 1, j] = 255
                    img_new[i + 1, j + 1] = 255
        it += 1
        img_arr = img_new.copy()
    return img_new


def erodeboi(img_arr, iteration):
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Erotion iteration: " + str(it + 1))
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                if img_arr[i, j] == 0:
                    img_new[i - 1, j - 1] = 0
                    img_new[i - 1, j] = 0
                    img_new[i - 1, j + 1] = 0
                    img_new[i, j - 1] = 0
                    img_new[i, j + 1] = 0
                    img_new[i + 1, j - 1] = 0
                    img_new[i + 1, j] = 0
                    img_new[i + 1, j + 1] = 0
        it += 1
        img_arr = img_new.copy()
    return img_new


def gaussblur(img):
    kernel = (1.0 / 57) * np.array(
        [[0, 1, 2, 1, 0],
         [1, 3, 5, 3, 1],
         [2, 5, 9, 5, 2],
         [1, 3, 5, 3, 1],
         [0, 1, 2, 1, 0]])

    # Get height and width
    h, w = img.shape
    result = np.zeros(img.shape, dtype=np.uint8)

    # compute everything!
    for sourceY in np.arange(2, h - 2):
        for sourceX in np.arange(2, w - 2):
            sub_result = 0.0
            for kernelY in np.arange(-2, 3):
                for kernelX in np.arange(-2, 3):
                    a = img.item(sourceY + kernelY, sourceX + kernelX)
                    p = kernel[2 + kernelY, 2 + kernelX]
                    sub_result = sub_result + (p * a)
            b = sub_result
            result.itemset((sourceY, sourceX), b)
    return result






