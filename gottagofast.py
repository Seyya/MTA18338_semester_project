import cv2
import numpy as np
import alexandria as alex
import scipy
from scipy import ndimage
from scipy import signal


def adaptive_thresholding(img, kernel):
    # original code w farmhouse resized to 200x200: 1.84 s
    # modified code w farmhouse -//- :
    # img = cv2.resize(img, (200, 200))  # brug resize hvis billedet er større end 500x500
    # height, width = img.shape
    # img_out = img.copy()

    # kernel = 13  # kernel size
    # k_offset = int(kernel / 2)

    # left = img[img[i, j] - k_offset:img[i, j]]
    # right = img[img[i, j] - k_offset:img[i, j]]
    # img[img > avg_neigh_value] = 255
    # img[img < avg_neigh_value] = 0

    # neighbors = np.ones((kernel, kernel), np.uint8)
    # neighbors = cv2.GaussianBlur(img, (13, 13), 0)
    neighbors = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    #avg_neigh = scipy.ndimage.convolve(img, neighbors)
    #avg_neigh = scipy.ndimage.generic_filter()
    # avg_neigh = scipy.ndimage.mean(img, kernel)
    # avg_neigh = scipy.ndimage.median_filter(img, size=kernel)
    # avg_neigh = scipy.signal.correlate2d(img, neighbors, 'same', 'wrap')
    img[img >= avg_neigh] = 255
    img[img < avg_neigh] = 0
    # img[img < scipy.ndimage.convolve(img, neighbors)] = 0

    # for i in range(2, height - 2):  # loop that goes through the height of the image with offset 1
    #     for j in range(2, width - 2):  # Loop that goes through the width of the image with offset 1
    #         # neigh_sum = 0
    # cur_pix_value = img.item(i, j)  # gets the value of a certain pixel at height/width

    # for k in range(-2, 3):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
    #     for l in range(-2, 3):  # loop that goes through the pixels in a 13x13 of the pixel at height/width
    #         neighbor_pixels = img.item(i + k, j + l)  # Get the value of the pixels in a 3x3 shape
    #         neigh_sum = neigh_sum + neighbor_pixels

    # avg_neigh_value = int(
    #     neigh_sum / (
    #                 kernel * kernel))  # sum of all neighbourhood pixel values divided by amount of pixels to get average pixel value
    # if cur_pix_value > avg_neigh_value:  # compares cur_pix_value with mean value to set it to black or white
    #     new_value = 255
    # else:
    #     new_value = 0
    # img_out.itemset((i, j), new_value)  # apply the threshold changes to the image
    # adapt_thr = img_out.copy()
    # print("pos", i, j)
    # return adapt_thr
    return img


cv2.imshow('adaptive_binary', adaptive_thresholding(cv2.imread('test3.jpg', cv2.IMREAD_GRAYSCALE), 3))
cv2.imshow('opencv adaptive_binary',
           cv2.adaptiveThreshold(cv2.imread('test3.jpg', cv2.IMREAD_GRAYSCALE), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 3, 0))

cv2.waitKey(0)
cv2.destroyAllWindows()
