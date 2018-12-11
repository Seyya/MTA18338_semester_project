import numpy as np
import cv2
import alexandria as alex


# grayValue = 0.07 * img[:, :, 2] + 0.72 * img[:, :, 1] + 0.21 * img[:, :, 0]
# gray_img = grayValue.astype(np.uint8)
# return gray_img


def dilate(img_arr, iteration):
    # original code on farmhouse w 3 iterations: 9.73 s
    # modified code -//-:
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


def dilate2(img, iteration):
    kernel = np.array([[255, 255, 255], [255, 0, 255], [255, 255, 255]])
    it = 0
    img_new = img.copy()
    while it != iteration:
        if img == 255:
            img_new[]
        it += 1
        img_arr = img_new.copy()
        return img_new


cv2.imshow('dilation',
           dilate(cv2.imread('binary_test.png', cv2.IMREAD_GRAYSCALE), 3))

cv2.waitKey(0)
cv2.destroyAllWindows()
