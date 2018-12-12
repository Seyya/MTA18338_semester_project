import math
import time

import cv2
import numpy as np


class Pos:
    x = 0
    y = 0

    def __init__(self, x, y):  # swapping these breaks
        self.x = int(x)
        self.y = int(y)

    def place(self):
        return self.y, self.x  # swapped to conform with python/cv2

    def __add__(self, b):
        a = self
        return Pos(a.x + b.x, a.y + b.y)

    def __sub__(self, b):
        a = self
        return Pos(a.x - b.x, a.y - b.y)

    def __eq__(self, b):
        a = self
        return a.x == b.x and a.y == b.y

    def __mul__(self, b):
        a = self
        return Pos(a.x * b, a.y * b)

    # def __ne__(self, b):  # apparently only necessary in python 2 and not 3
    #     a = self
    #     return not a == b

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, b):  # swapped x and y in this method as well
        a = self
        c = a.__sub__(b)
        res = True
        if a.x != b.x:
            if c.x < 0:
                res = False
        else:
            if c.y < 0:
                res = False
        return res


def cwoffset(point):  # check here first for errors
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


def delete_old_conts(x, y, l, b, tempi, nond):
    for k in range(y, l + 1):
        for g in range(x, b + 1):
            tempi[k, g] = nond  # white, remember to change
    return tempi


def boundary_box(outline, src, tempi, bo, nond):
    xarray = []
    yarray = []
    for j in outline:
        yarray.append(j.x)
        xarray.append(j.y)
    x = min(xarray)
    y = min(yarray)
    l = max(yarray)
    b = max(xarray)

    # if bo is True:
    #     cv2.rectangle(src, (x, y), (b, l), 127, 2)  # black, remember to change

    tempi = delete_old_conts(x, y, l, b, tempi, nond)
    return tempi


# our lord and savior: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html

def contouring(img, detected):
    notDetected = 255
    if detected == 255:
        notDetected = 0
    # tempi = img.copy()
    h, w = img.shape
    cv2.rectangle(img, (0, 0), (h, w), notDetected, 2)
    tempi = np.ndarray.copy(img)
    tempo = []
    moreblacks = True
    while moreblacks:
        start = time.time()
        end = time.time()
        onlyrealcontshavecurves = True
        h, w = tempi.shape
        first = None
        outline = set()
        pixel_found = False
        for x in range(h):
            # something possibly missing here. Just hope it gives no issues. (It does if a pixel is found in the first pixel checked)
            if pixel_found:
                break
            for y in range(w):
                if tempi[x, y] == detected:  # black, remember to change
                    first = Pos(x, y)
                    pixel_found = True
                    break
                firstprev = Pos(x, y)
        if first is None:
            moreblacks = False

        if pixel_found:
            prev = firstprev  # I know. But fuck you python :)
            outline.add(first)
            boundary = first
            curr = clockwise(boundary, prev)
            blackmanspotted = 0
            while (
                    curr != first or prev != firstprev) and blackmanspotted <= 8 and end - start < 0.1:  # 0.04 - very much stc
                end = time.time()
                if w >= curr.y >= 0 and h >= curr.x >= 0 and tempi[
                    curr.x, curr.y] == detected:  # black, remember to change - also makes errors with frame sizes above 600?
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
                print("Your figures are incomplete")
                onlyrealcontshavecurves = False
            tempi = boundary_box(outline, img, tempi, onlyrealcontshavecurves, notDetected)
            tempo.append(outline)
    return tempo  # probably does not have to return img, so it has been removed temporarily


def roi_boi(outline, img):  # should be given the outlines given by the second output of contours (contours[1])
    it = 0
    sub_images = []
    for i in range(len(outline)):  # outline contains multiple outlines (one set for each contour)
        xarray = []
        yarray = []
        # salasa = str(it)
        it += 1
        for j in outline[i]:
            yarray.append(j.x)
            xarray.append(j.y)
        x = min(xarray)
        y = min(yarray)
        l = max(yarray)
        b = max(xarray)

        temp = img[y:l, x:b]  # from min to max (min:max)
        sub_images.append(temp)
        # try:
        #   cv2.imshow(salasa, temp)
        # except AssertionError:
        #    print('Error occurred. Probably safe to ignore')
        return sub_images


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
    # original code w farmhouse resized to 200x200:
    img = cv2.resize(img, (200, 200))  # brug resize hvis billedet er større end 500x500
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


def dilate(img_arr, iteration):
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


def erode(img_arr, iteration):
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Erosion iteration: " + str(it + 1))
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


def distance_finder(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# finds the perpendicular distance between a line and a point
def range_finder(pt, a, b, c):  # abc for line equation: ax+by+c
    bla = math.sqrt(a * a + b * b)
    if bla != 0:
        return abs((a * pt.x + b * pt.y + c)) / bla  # math
    else:
        return -1


# finds a line function (or linear equation) ax + by + c
def line_finder(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


# functions requires a list of Pos objects, and a user defined epsilon
def square_maker3000(pts, epsilon):  # or: approxPoly_lineShape or RamerDouglasPeucker  # 379, 44
    dmax = 0
    index = 0
    end = len(pts) - 1
    i = 0
    result_list = []
    for pt in pts:
        i += 1
        a, b, c = line_finder(pts[0].x, pts[0].y, pts[end].x, pts[end].y)
        d = range_finder(pt, a, b, c)
        if d > dmax:
            index = i
            dmax = d
    recpts1 = []
    recpts2 = []

    if dmax > epsilon:
        for l in range(0, index):
            recpts1.append(pts[l])
        for p in range(index, end):
            recpts2.append(pts[p])
        recresults1 = square_maker3000(recpts1, epsilon)
        recresults2 = square_maker3000(recpts2, epsilon)

        for r in recresults1:
            result_list.append(r)
        for r in recresults2:
            result_list.append(r)
#        result_list = recresults1, recresults2

    else:
        try:
            result_list = pts[0], pts[end]
        except IndexError:
            return pts
    return result_list


def order_list(alist):  # slow as fuck, but sorts perfectly (when in list format) #TODO optimize me
    i = 0
    again = True
    while again:
        for l in alist:
            i += 1
            if i < len(alist):
                a = l
                b = alist[i]
                if a > b:
                    alist[i] = a  # b = a
                    alist[i - 1] = b  # a = b
                    again = True
                    i = 0
                    break
                else:
                    again = False

    return alist  # return the sorted list


def find_corners(outline):  # corners matter, but not their individuality. No need to preserve them
    setlist = list(outline)
    setlist = order_list(setlist)
    topright = Pos(setlist[0].x, setlist[0].y)  # right when rotated 45
    topleft = setlist[0]  # top when rotated 45
    bottomright = setlist[len(setlist) - 1]  # bot when roated 45
    bottomleft = Pos(setlist[0].x, setlist[0].y)

    for o in setlist:  # might wanna tangle this into the pos object
        if o.y >= topright.y and o.x <= topright.x:
            topright.x = o.x
            topright.y = o.y
        if o.y <= bottomleft.y and o.x >= bottomleft.x:
            bottomleft.x = o.x
            bottomleft.y = o.y

    a = bottomleft.y + 1
    b = topleft.y
    if a == b:
        bottomleft = Pos(setlist[0].x, setlist[0].y)
        for o in setlist:
            if o.y <= bottomleft.y:
                bottomleft.x = o.x
                bottomleft.y = o.y

    return [topright, topleft, bottomright, bottomleft]


def sobel_operator(img):
    height, width = img.shape
    newimg = np.zeros((height, width), np.uint8)
    kernelx = [0] * 9  # g_x
    kernely = [0] * 9  # g_y

    for j in range(1, width - 1):
        for i in range(1, height - 1):
            kernelx[0] = img[i - 1, j - 1] * -3
            kernelx[1] = img[i - 1, j] * 0
            kernelx[2] = img[i - 1, j + 1] * 3
            kernelx[3] = img[i, j - 1] * -10
            kernelx[4] = img[i, j] * 0
            kernelx[5] = img[i, j + 1] * 10
            kernelx[6] = img[i + 1, j - 1] * -3
            kernelx[7] = img[i + 1, j] * 0
            kernelx[8] = img[i + 1, j + 1] * 3

            gx = sum(kernelx)
            kernelx_average = gx / 9

            kernely[0] = img[i - 1, j - 1] * -3
            kernely[1] = img[i - 1, j] * -10
            kernely[2] = img[i - 1, j + 1] * -3
            kernely[3] = img[i, j - 1] * 0
            kernely[4] = img[i, j] * 0
            kernely[5] = img[i, j + 1] * 0
            kernely[6] = img[i + 1, j - 1] * 3
            kernely[7] = img[i + 1, j] * 10
            kernely[8] = img[i + 1, j + 1] * 3

            gy = sum(kernely)
            kernely_average = gy / 9
            # g = math.sqrt(kernelx_average ** 2 + kernely_average ** 2)
            #            theta = (np.arctan(gy/gx))*180/math.pi
            #            if theta == 90 or theta == 0:
            g = math.sqrt(kernelx_average ** 2 + kernely_average ** 2)
            #            else:
            #                g = 0
            newimg[i, j] = g
    return newimg


def runGrassFire(id, location, treshMin, treshMax, sourceImg, result):
    height = sourceImg.shape[0]
    width = sourceImg.shape[1]
    # Create array for new locations to check
    newQueue = []
    # print("The location is: " + str(location))

    # Check pixel above
    y, x = location

    if y - 1 >= 0:
        if result[y - 1, x] == 0:
            # If the pixel is within the treshold, assign ID and add to queue
            if sourceImg[y - 1, x] >= treshMin and sourceImg[y - 1, x] <= treshMax:
                # print("Found pixel above.")

                result[y - 1, x] = id
                newPosition = (y - 1, x)
                # Append the new location coordinates to the queue
                newQueue.append(newPosition)

    # Check pixel to the right
    if x + 1 < width:
        if result[y, x + 1] == 0:
            if sourceImg[y, x + 1] >= treshMin and sourceImg[y, x + 1] <= treshMax:
                # print("Found pixel to the right")

                result[y, x + 1] = id
                newPosition = (y, x + 1)
                newQueue.append(newPosition)

    # Check pixel below
    if y + 1 < height:
        # print("The y-coordinate is: " + str(y))
        if result[y + 1, x] == 0:
            # print("The x and y coordinates are: " + str(y, x))
            if sourceImg[y + 1, x] >= treshMin and sourceImg[y + 1, x] <= treshMax:
                # print("Found pixel below")

                result[y + 1, x] = id
                newPosition = (y + 1, x)
                newQueue.append(newPosition)

    # check pixel to the left
    if x - 1 >= 0:
        if result[y, x - 1] == 0:
            if sourceImg[y, x - 1] >= treshMin and sourceImg[y, x - 1] <= treshMax:
                # print("Found pixel to the left")

                result[y, x - 1] = id
                newPosition = (y, x - 1)
                newQueue.append(newPosition)

    # print("The new queue is: " + str(newQueue))
    return result, newQueue


def findBlob(sourceImg, treshMin, treshMax):
    # Create nesesary variables
    height = sourceImg.shape[0]
    width = sourceImg.shape[1]
    blobID = 1
    queue = []
    result = np.zeros(sourceImg.shape)

    # Loop through each pixel in the image
    for Ypos in range(0, width - 1):
        for Xpos in range(0, height - 1):
            # If the value of x and y is 0..
            if result[Xpos, Ypos] == 0:
                # .. check treshold..
                if sourceImg[Xpos, Ypos] >= treshMin and sourceImg[Xpos, Ypos] <= treshMax:
                    # .. and assign an id before running the grass-fire algorithm
                    # Overwrite the result and add the coordinates to the queue
                    sourceImg[Xpos, Ypos] = blobID
                    position = (Xpos, Ypos)
                    # print("The position is: " + str(position))
                    newResult, newQueue = runGrassFire(blobID, position, treshMin, treshMax, sourceImg, result)
                    result = newResult
                    queue.extend(newQueue)
                    # print("The current BLOB id is: " + str(blobID))

                    # As long as there is coordinates in the queue, keep running the grass-fire algorithm
                    while len(queue) != 0:
                        # print("The length of the queue is: " + str(len(queue)))
                        # print("This is the current queue: " + str(queue))
                        # print("The first element of the queue is: " + str(queue[0]))

                        # Take the first entry in the queue, run algorithm ect. before deleting the first entry in the queue
                        firstInQueue = queue[0]
                        newResult, newQueue = runGrassFire(blobID, firstInQueue, treshMin, treshMax, sourceImg, result)
                        result = newResult
                        queue.extend(newQueue)
                        del queue[0]
                        # print(str(len(queue)))
                    blobID += 1
    return result


def meanSquaredError(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized