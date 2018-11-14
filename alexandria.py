import time

import cv2
import numpy as np


class Pos:
    x = 0
    y = 0

    #"Constructor"
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Return x and y
    def place(self):
        return self.x, self.y

    #Create functions for a and b, allowing them to be added together
    def __add__(self, b):
        a = self
        return Pos(a.x + b.x, a.y + b.y)

    #Create a function to allow a and b to be substracted from each other
    def __sub__(self, b):
        a = self
        return Pos(a.x - b.x, a.y - b.y)

    #Create  a function checking if a and b are equal
    def __eq__(self, b):
        a = self
        return a.x == b.x and a.y == b.y

    # def __ne__(self, b):  # apparently only necessary in python 2 and not 3?
    #     a = self
    #     return not a == b

    #Makes a and b hashable
    def __hash__(self):
        return hash((self.x, self.y))

    #Function checking if one is smaller than the other
    def __lt__(self, b):
        a = self
        c = a.__sub__(b)
        res = True
        if a.y != b.y:
            if c.y < 0:
                res = False
        else:
            if c.x < 0:
                res = False
        return res


def cwoffset(point):  # check here  first for erros
    switcher = {
        Pos(1, 0): Pos(1, -1),
        Pos(1, -1): Pos(0, -1),
        Pos(0, -1): Pos(-1, -1),
        Pos(-1, -1): Pos(-1, 0),
        Pos(-1, 0): Pos(-1, 1),
        Pos(-1, 1): Pos(0, 1),
        Pos(0, 1): Pos(1, 1),
        Pos(1, 1): Pos(1, 0)
    }
    #    print(point.place())
    return switcher.get(point)


def clockwise(target, prev):
    return cwoffset(prev - target) + target


def delete_old_cunts(x, y, l, b, tempi):
    for k in range(y, l + 1):
        for g in range(x, b + 1):
            tempi[k, g] = 0  # white, remember to change
    return tempi


def boundary_box(outline, src, tempi, bo):
    xarray = []
    yarray = []
    for j in outline:
        yarray.append(j.x)
        xarray.append(j.y)
    x = min(xarray)
    y = min(yarray)
    l = max(yarray)
    b = max(xarray)
    if bo is True:
        cv2.rectangle(src, (x, y), (b, l), 255, 2)  # black, remember to change
    tempi = delete_old_cunts(x, y, l, b, tempi)
    return tempi


# our god: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
# https://github.com/Dkendal/Moore-Neighbor_Contour_Tracer/blob/master/ContourTrace.cs
def contouring(img):
    # tempi = img.copy()
    h, w = img.shape
    cv2.rectangle(img, (0, 0), (h, w), 0, 2)
    tempi = np.ndarray.copy(img)
    tempo = []
    moreblacks = True
    while moreblacks:
        start = time.time()
        end = time.time()
        onlyrealcuntshavecurves = True
        h, w = tempi.shape
        first = None
        outline = set()
        pixel_found = False
        for x in range(h):
            # something possibly missing here. Just hope it gives no issues. (It does if a pixel is found in the first pixel checked)
            if pixel_found:
                break
            for y in range(w):
                if tempi[x, y] == 255:  # black, remember to change
                    first = Pos(x, y)
                    pixel_found = True
                    break
                firstprev = Pos(x, y)
        if first is None:
            moreblacks = False

        if pixel_found:
            prev = firstprev
            outline.add(first)
            boundary = first
            curr = clockwise(boundary, prev)
            blackmanspotted = 0
            while (
                    curr != first or prev != firstprev) and blackmanspotted <= 8 and end - start < 0.1:  # 0.04 - very much stc
                end = time.time()
                if w >= curr.y >= 0 and h >= curr.x >= 0 and tempi[
                    curr.x, curr.y] == 255:  # black, remember to change - also makes errors with frame sizes above 600?
                    outline.add(curr)
                    prev = boundary
                    boundary = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted = 0
                else:
                    prev = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted += 1
            if blackmanspotted > 8:
                print("Your figures are incomplete you mongrel")
                onlyrealcuntshavecurves = False
            tempi = boundary_box(outline, img, tempi, onlyrealcuntshavecurves)
            tempo.append(outline)
    return img, tempo

#Define the Region of Interest - RoI
def roi_boi(outline, img):  # should be given the outlines given by the second output of contours (contours[1])
    xarray = []
    yarray = []
    it = 0
    for i in range(len(outline)):  # outline contains multiple outlines (one set for each contour)
        salasa = str(it)
        it += 1
        for j in outline[i]:
            yarray.append(j.x)
            xarray.append(j.y)
        x = min(xarray)
        y = min(yarray)
        l = max(yarray)
        b = max(xarray)

        temp = img[y:l, x:b]  # from min to max (min:max)
        try:
            cv2.imshow(salasa, temp)
        except AssertionError:
            print('Error occurred. Probably safe to ignore')


#Create a binary image based on a given threshold
def binary_threshold(img, threshold):
    # original code: 85.5 ns
    # original code w farmhouse img: 1.1 s
    # modified w farmhouse: 76.1 ms
    img[img > threshold] = 255
    img[img < threshold] = 0
    # h, w = img.shape
    # for i in np.arange(h):
    #     for j in np.arange(w):
    #         a = img.item(i, j)
    #         if a > threshold:
    #             b = 255
    #         else:
    #             b = 0
    #         img.itemset((i, j), b)
    return img


def adaptive_thresholding(img):
    #original code w farmhouse resized to 200x200:
    img = cv2.resize(img, (200, 200))   # brug resize hvis billedet er større end 500x500
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
            # print("pos", i, j)
    return adapt_thr


#Manual conversion of an image from RGB to greyscale.
def rgb2grey(img):
    # original code on farmhouse img: a long long long time
    # modified code -//-: 192 ms
    grey_val = 0.07 * img[:, :, 2] + 0.72 * img[:, :, 1] + 0.21 * img[:, :, 0]
    grey_img = grey_val.astype(np.uint8)
    return grey_img

    # h, w, _ = img.shape
    #
    # gray = np.zeros((h, w), np.uint8)
    # for i in range(h):
    #     for j in range(w):
    #         gray[i, j] = np.clip(0.07 * img[i, j, 0] + 0.72 * img[i, j, 1] + 0.21 * img[i, j, 2], 0, 255)
    #
    # cv2.imshow("gray", gray)


#Dilation - make an object larger
def dilate(img_arr, iteration):
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Dilation iteration: " + str(it + 1))
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                if img_arr[i, j] == 255:            #This dilate uses an 8 core.
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


#Erosion - make an object smaller
def erode(img_arr, iteration):
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Erosion iteration: " + str(it + 1))
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                if img_arr[i, j] == 0:              #8-core erode
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


#Manual creation of gaussian blur
def gaussblur(img):
    #Using a 5x5 kernel
    kernel = (1.0 / 57) * np.array(
        [[0, 1, 2, 1, 0],
         [1, 3, 5, 3, 1],
         [2, 5, 9, 5, 2],
         [1, 3, 5, 3, 1],
         [0, 1, 2, 1, 0]])

    # Get height and width
    h, w = img.shape
    #Create a 'copy' of the image, consisting of 0s
    result = np.zeros(img.shape, dtype=np.uint8)

         # compute everything!
    #Have the kernel placed in [0,0] of the image
    for sourceY in np.arange(2, h - 2):
        for sourceX in np.arange(2, w - 2):
            sub_result = 0.0
            for kernelY in np.arange(-2, 3):
                for kernelX in np.arange(-2, 3):    #compute the new values of the pixel the kernel is handling
                    a = img.item(sourceY + kernelY, sourceX + kernelX)
                    p = kernel[2 + kernelY, 2 + kernelX]
                    sub_result = sub_result + (p * a)
            b = sub_result
            result.itemset((sourceY, sourceX), b)   #create a resulting image before returning it
    return result
