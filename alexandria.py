
import math
import time
import cv2
import numpy as np


class Pos:
    # Variables for x and y coordinates
    x = 0
    y = 0

    # The init function is a constructor for Pos
    def __init__(self, x, y):  # swapping these breaks
        self.x = int(x)
        self.y = int(y)

    def place(self):
        return self.y, self.x  # swapped to conform with python/cv2

    # All functions after this line are rules of arithmetic for the object
    # e.g. how it should add coordinates together when adding two points
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
    #Switch that creates a clockwise offset
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


# Function that makes neighborhood processing go clockwise
def clockwise(target, prev):
    return cwoffset(prev - target) + target


# Function that will delete contours that has already been detected and stored, afterwards it returns
# the new image. This makes sure contouring can find more than one contour in an image, not the same
def delete_old_conts(x, y, l, b, tempi, nond):
    for k in range(y, l + 1):
        for g in range(x, b + 1):
            tempi[k, g] = nond  # white, remember to change
    return tempi


# Function that draws a boundary box around an object by using a contour
def boundary_box(outline, src, tempi, bo, nond):
    #Stores all x and y coordinates
    xarray = []
    yarray = []
    # Add all x and y coordinates from "outline"
    for j in outline:
        yarray.append(j.x)
        xarray.append(j.y)
    # initialize variales with highest and loweset values in order to make a box from the coordinates
    x = min(xarray)
    y = min(yarray)
    l = max(yarray)
    b = max(xarray)

    # When not commented out it will draw a box with the given coordinates
    # if bo is True:
    #     cv2.rectangle(src, (x, y), (b, l), 127, 2)  # black, remember to change

    tempi = delete_old_conts(x, y, l, b, tempi, nond)
    return tempi


# Function that does contouring on an image, finds the outline of an object on an image, only works on binary image
def contouring(img, detected):
    #Variable that allows for finding a black or white object depending on your binary thresholding
    notDetected = 255
    if detected == 255:
        notDetected = 0

    #initialize preliminary variables and functions to draw a rectangle
    h, w = img.shape
    cv2.rectangle(img, (0, 0), (h, w), notDetected, 2)
    tempi = np.ndarray.copy(img)
    tempo = []
    moreblacks = True
    while moreblacks:
        #Initialize a bunch more variables, such as time, boolean and set variables
        start = time.time()
        end = time.time()
        onlyrealcontshavecurves = True
        h, w = tempi.shape
        first = None
        outline = set()
        pixel_found = False
        # Goes through the image in height direction first, if it finds a pixel of detected value (black or white)
        # It will jump out of the loop. The same is the case for the width of the image
        for x in range(h):
            if pixel_found:
                break
            for y in range(w):
                # a pixel has same value of detected it will be stored as "first" and move onto next part of the code
                if tempi[x, y] == detected:  # black, remember to change
                    first = Pos(x, y)
                    pixel_found = True
                    break
                firstprev = Pos(x, y)
        if first is None:
            moreblacks = False

        # In case pixel_fonud is true this code will start running
        if pixel_found:
            # Initialize variables
            prev = firstprev
            outline.add(first)
            boundary = first
            # Curr variable makes sure the function goes clockwise in the object it is trying to make a contour of
            curr = clockwise(boundary, prev)
            blackmanspotted = 0

            # As long as this statement is true it will run the code as it means the figure most be complete
            # have to be adjusted depending on computer though as one of the conditions is time based
            while (
                    curr != first or prev != firstprev) and blackmanspotted <= 8 and end - start < 0.1:  # 0.04 - very much stc
                end = time.time()
                # If this statement is true it will add the pixel at x/y coordinates to the outline as it must
                # be a part of the object
                if w >= curr.y >= 0 and h >= curr.x >= 0 and tempi[
                    curr.x, curr.y] == detected:  # black, remember to change - also makes errors with frame sizes above 600?
                    outline.add(curr)
                    prev = boundary
                    boundary = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted = 0
                # if it is not true it will check next pixel in clockwise order to see if it is true
                else:
                    prev = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted += 1
            # If it is not true 8 times it means the figure or object most be incomplete thus it is impossible
            # to draw an outline around the object
            if blackmanspotted > 8:
                print("Your figures are incomplete")
                onlyrealcontshavecurves = False
            # Runs the function boundary box with the values found, which allows to draw a box around the contour
            tempi = boundary_box(outline, img, tempi, onlyrealcontshavecurves, notDetected)
            tempo.append(outline)
    return tempo  # probably does not have to return img, so it has been removed temporarily


# Function that takes out a sub image from an image to make a "Region of interest" (RoI)
def roi_boi(outline, img):  # should be given the outlines given by the second output of contours (contours[1])
    #Initialize variabls
    it = 0
    sub_images = []
    for i in range(len(outline)):  # outline contains multiple outlines (one set for each contour)
        xarray = []
        yarray = []
        # salasa = str(it)
        it += 1
        # Get x and y coordinates from outline and store them in x and yarray
        for j in outline[i]:
            yarray.append(j.x)
            xarray.append(j.y)
        # initialize variables with min and max values from the outline. basically the resolution/size of the iamge
        x = min(xarray)
        y = min(yarray)
        l = max(yarray)
        b = max(xarray)

        # store the new sub image in "temp" variable
        temp = img[y:l, x:b]  # from min to max (min:max)
        sub_images.append(temp)
        # try:
        #   cv2.imshow(salasa, temp)
        # except AssertionError:
        #    print('Error occurred. Probably safe to ignore')
        return sub_images


# Function that makes binary thresholding on a greyscale iamge
def binary_threshold(img, threshold):
    # original code: 85.5 ns
    # original code w farmhouse img: 1.1 s
    # modified w farmhouse: 76.1 ms
    # Go through the entire image and check the greyscale value if it higher or lower than the threshold
    # it will be set to either black or white
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


# Function that does binary thresholding by with the method of adaptive thresholding
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


# Function that oconverts a color image to greyscale
def rgb2grey(img):
    # original code on farmhouse img: a long long long time
    # modified code -//-: 192 ms
    # Goes through all pixels in the image and finds the average of the color pixel with a weight added
    # The average is the new value of the pixel which will be a greyscale value
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


# Function that does dilation in a binary image, increase the "white" of the image
def dilate(img_arr, iteration):
    #initialize variables
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Dilation iteration: " + str(it + 1))
        #Goes through the entire image with an offset of 1 as it is using a 3x3 kernel
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                #Checks if the pixel is white, if it is it will set all pixels around it in a 3x3 kernel to white
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


# Function that does dilation in a binary image, increase the "black" of the image
def erode(img_arr, iteration):
    # initialize variables
    h, w = img_arr.shape
    it = 0
    img_new = img_arr.copy()
    while it != iteration:
        print("Erosion iteration: " + str(it + 1))
        # Goes through the entire image with an offset of 1 as it is using a 3x3 kernel
        for j in range(1, w - 1):
            for i in range(1, h - 1):
                # Checks if the pixel is black, if it is it will set all pixels around it in a 3x3 kernel to black
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


# Function that applies gaussian blur to an image by using a 5x5 kernel
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

    # Goes through the image in x and y direction with an offset of 2 due to having a 5x5 kernel
    for sourceY in np.arange(2, h - 2):
        for sourceX in np.arange(2, w - 2):
            sub_result = 0.0
            #Goes through the 5x5 kernel in x and y direction
            for kernelY in np.arange(-2, 3):
                for kernelX in np.arange(-2, 3):
                    #Compute the new value of the pixels
                    a = img.item(sourceY + kernelY, sourceX + kernelX)
                    p = kernel[2 + kernelY, 2 + kernelX]
                    sub_result = sub_result + (p * a)
            b = sub_result
            #Applying the calculated result to the pixel
            result.itemset((sourceY, sourceX), b)
    return result

# Function for the distance formula, finds the distance between two points
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


# functions requires a list of Pos objects, and a user defined epsilon, does not currently work properly but
# the algorithm can be found at: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
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


def order_list(alist):  # pretty slow, but sorts perfectly (when in list format)
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


# Function that find the corners from a given outline, topleft, -right, bottomleft and -right
def find_corners(outline):
    #Initialize a list that consist of outline, then sort the list to go from max to min values.
    setlist = list(outline)
    setlist = order_list(setlist)
    topright = Pos(setlist[0].x, setlist[0].y)  # right when rotated 45
    topleft = setlist[0]  # top when rotated 45
    bottomright = setlist[len(setlist) - 1]  # bot when roated 45
    bottomleft = Pos(setlist[0].x, setlist[0].y)

    # Using a loop to find the most topright and bottomleft values in "setlist"
    for o in setlist:
        if o.y >= topright.y and o.x <= topright.x:
            topright.x = o.x
            topright.y = o.y
        if o.y <= bottomleft.y and o.x >= bottomleft.x:
            bottomleft.x = o.x
            bottomleft.y = o.y

    a = bottomleft.y + 1
    b = topleft.y
    # In case bottomleft and topleft are on the same line it'll be sorted in the right order
    if a == b:
        bottomleft = Pos(setlist[0].x, setlist[0].y)
        for o in setlist:
            if o.y <= bottomleft.y:
                bottomleft.x = o.x
                bottomleft.y = o.y
    # Return the four new points which are the corners of an object
    return [topright, topleft, bottomright, bottomleft]


# Function for sobel edge detection on a binary image
def sobel_operator(img):
    #initialize variables
    height, width = img.shape
    newimg = np.zeros((height, width), np.uint8)
    kernelx = [0] * 9  # g_x
    kernely = [0] * 9  # g_y

    #Following lines are loops that go through a 3x3 kernel in x and y direction with a weight added
    for j in range(1, width - 1):
        for i in range(1, height - 1):
            #Get all the pixel values for each position in the kernel
            kernelx[0] = img[i - 1, j - 1] * -3
            kernelx[1] = img[i - 1, j] * 0
            kernelx[2] = img[i - 1, j + 1] * 3
            kernelx[3] = img[i, j - 1] * -10
            kernelx[4] = img[i, j] * 0
            kernelx[5] = img[i, j + 1] * 10
            kernelx[6] = img[i + 1, j - 1] * -3
            kernelx[7] = img[i + 1, j] * 0
            kernelx[8] = img[i + 1, j + 1] * 3

            # Adds all the pixel values together and find the average of the pixel values
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

            # Adds all the pixel values together and find the average of the pixel values
            gy = sum(kernely)
            kernely_average = gy / 9
            # g = math.sqrt(kernelx_average ** 2 + kernely_average ** 2)
            #            theta = (np.arctan(gy/gx))*180/math.pi
            #            if theta == 90 or theta == 0:
            #Calculate the new value for the pixel by using the x and y kernel
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


# Template matching by using squared difference method.
# Can't find templates at edges of the border 1 pixel offset needed
def temp_matching(img, template):
    srcH, srcW = img.shape[:2]
    templateH, templateW = template.shape[:2]

    # Loop that goes through the image in x and y direction
    for i in range(0, srcH - 100):
        for j in range(0, srcW - 100):
            # Makes a new sub_images with the size of the template, makes it possible to make comparisons between
            # the sub image and template
            tempo_img = img[i:templateH + i, j:templateW + j]
            pixels = (tempo_img.shape[0] * tempo_img.shape[1])

            pix_sum = 0
            for k in range(0, templateH):
                for l in range(0, templateW):
                    # Get the greyscale value for the pixel in template and tempo images
                    tempo_pix = tempo_img[k, l]
                    template_pix = template[k, l]

                    # Calculations to find the squared difference
                    subtract_pix = (tempo_pix - template_pix)
                    pow_pix = math.pow(subtract_pix, 2)
                    pix_sum = pix_sum + pow_pix
            result = pix_sum / pixels
            # If the result is within a certain threshold it will store the coordinates and draw a rectangle
            if result < 5000:
                print(result)
                x = j
                y = i
                cv2.rectangle(img, (x, y), (x + templateH, y + templateW), 0, 2)