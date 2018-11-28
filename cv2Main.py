# import the necessary packages
import cv2
import numpy as np
from skimage import exposure

import Client
import alexandria as al


def mean_squared_error(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


# this code section is straight up copy pasted from the library imutils bc i cant import it and it does some kind of
# magic that cannot be recreated
# TODO make function our own/incorporate into own code and/or move to alexandria
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


def findSquares(image):
    # ratio = image.shape[0] / 300.0
    # dim = int(image.shape[1] / ratio), 300
    # orig = image.copy()
    # image = cv2.resize(image, dim)

    ratio = image.shape[0] / 300.0
    orig = image.copy()
    image = resize(image, height=300)

    # convert the image to grayscale, blur it, and find edges in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = contours[0]
    # cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    cv2.imshow("edgy", edged)
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    # loop over our contours
    warps = []
    conts = []
    theonecont = False  # fixes contour duplicates
    for c in contours:
        if cv2.contourArea(c) < 50:  # if the contour is too small, ignore it #TODO change me
            continue
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            # now that we have our screen contour, we need to determine
            # the top-left, top-right, bottom-right, and bottom-left
            # points so that we can later warp the image -- we'll start
            # by reshaping our contour to be our finals and initializing
            # our output rectangle in top-left, top-right, bottom-right,
            # and bottom-left order
            pts = screenCnt.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # the top-left point has the smallest sum whereas the
            # bottom-right has the largest sum
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # compute the difference between the points -- the top-right
            # will have the minumum difference and the bottom-left will
            # have the maximum difference
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # multiply the rectangle by the original ratio
            rect *= ratio
            # now that we have our rectangle of points, let's compute
            # the width of our new image
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

            # ...and now for the height of our new image
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            # take the maximum of the width and height values to reach
            # our final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))

            # construct our destination points which will be used to
            # map the screen to a top-down, "birds eye" view
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            # calculate the perspective transform matrix and warp
            # the perspective to grab the screen
            M = cv2.getPerspectiveTransform(rect, dst)
            warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
            # convert the warped image to grayscale and then adjust
            # the intensity of the pixels to have minimum and maximum
            # values of 0 and 255, respectively
            warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
            warp = exposure.rescale_intensity(warp, out_range=(0, 255))
            if theonecont:
                warps.append(warp)
                conts.append(c)
                theonecont = False
            else:
                theonecont = True
    return warps, conts
    # the pokemon we want to identify will be in the top-right
    # corner of the warped image -- let's crop this region out
    #    (h, w) = warp.shape
    #    (dX, dY) = (int(w * 0.4), int(h * 0.45))
    #    crop = warp[10:dY, w - dX:w - 10]

    # save the cropped image to file
    # cv2.imwrite("cropped.png", crop)


cap = cv2.VideoCapture(0)
RUNNING = True

one = al.Pos(30000, 30000)
two = al.Pos(100, 100)
three = al.Pos(20, 20)
playerList = [one, two, three]

templates = []
for i in range(0, 3):
    template = cv2.imread('temp%s.jpg' % i, 0)
    print("read: temp%s.jpg" % i)
    templates.append(template)

while RUNNING:
    # https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/
    # https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
    ret, image = cap.read()
    # image = cv2.imread("phone_test.jpg")
    wasps = 0
    warps, conts = findSquares(image)
    drawn = resize(image, height=300)
    temp_match_arr = []
    posList = []
    for wa in warps:
        c = conts[wasps]
        wasps += 1
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(drawn, (x, y), (x + w, y + h), (0, 255, 0), 2)
        temp_match_arr.append(wa)
        center = al.Pos(x + (w / 2), y + (h / 2))
        posList.append(center)

    t = -1
    for template in templates:
        t += 1
        ma = -1
        for img in temp_match_arr:
            img = cv2.resize(img, (template.shape[1], template.shape[0]))
            rows, cols = img.shape
            for i in range(0, 4):
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90 * i, 1)
                dst = cv2.warpAffine(img, M, (cols, rows))
                if mean_squared_error(dst, template) < 10000:  # TODO: fine tune me
                    cv2.imshow("Found: " + str(t), resize(img, height=300))
                    playerList[t] = posList[ma]
            ma += 1
    Client.send_pos(playerList)
    bg_ch = True  # send this as a message from server ("hey i updated map fu") Should prolly run once regardless
    if bg_ch:
        cv2.imshow("Background", Client.recieve_bg())
        print("Background recieved from server")
    cv2.imshow("Ay", drawn)
    cv2.waitKey(0)

# show our images

# cv2.imshow("edge", edged)
cv2.waitKey(0)