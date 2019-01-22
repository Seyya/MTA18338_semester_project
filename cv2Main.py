# import the necessary packages
import os
import sys

import cv2
import numpy as np
from skimage import exposure

import alexandria as al

# the program has to find the folder with the Client file in it, in order to function.
# This depends on where the user has saved the files, and is fixable with a proper installer/packager for an executable
sys.path.append('C:/Users/chris/PycharmProjects/P3_semester_project/Client')
import Client


def findSquares(image):
    # calculate ratio for resizing, create a copy to save the unedited image and resize the other image
    ratio = image.shape[0] / 300.0
    orig = image.copy()
    image = al.resize(image, height=300)
    # convert the image to grayscale, blur it, and find edges in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 400)
    # find contours in the edged image
    im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    warps = []
    conts = []
    theonecont = False  # fixes contour duplicates
    for c in contours:
        # if the contour is too small, ignore it. This should be changed alongisde camera distance,
        # as the markers might shrink too much with perspective
        if cv2.contourArea(c) < 25:
            continue
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the approximated contour has four points, then it is likely to be a marker
        if len(approx) == 4:
            screenCnt = approx
            # with the contour of the marker, the top-left, top-right, bottom-right, and bottom-left points are
            # determined
            pts = screenCnt.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # the top-left point has the smallest sum whereas the bottom-right has the largest sum
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # compute the difference between the points -- the top-right will have the minumum difference
            # and the bottom-left will have the maximum difference
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # multiply the rectangle by the original ratio
            rect *= ratio
            # with the rectangle of points, the width of the image is calculated
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

            # ...and the height of the new image
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            # the maximum of width and height values are the final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))

            # construct the destination points which will be used to map the screen to a top-down view
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            # calculate the perspective transform matrix and warp the perspective to grab marker
            M = cv2.getPerspectiveTransform(rect, dst)
            warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
            # convert the warped image to grayscale and then adjust the intensity of the pixels to have
            # minimum and maximum values of 0 and 255, respectively
            warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
            warp = exposure.rescale_intensity(warp, out_range=(0, 255))
            # to stop the markers being found twice, every second is filtered out
            if theonecont:
                warps.append(warp)
                conts.append(c)
                theonecont = False
            else:
                theonecont = True
    return warps, conts


# capture video stream and define variables for while statement and player tokens
cap = cv2.VideoCapture(0)
RUNNING = True
# Add new position object to track more templates here and in playerList
one = al.Pos(0, 0)
two = al.Pos(0, 0)
three = al.Pos(0, 0)
four = al.Pos(0, 0)
five = al.Pos(0, 0)
six = al.Pos(0, 0)
seven = al.Pos(0, 0)
playerList = [one, two, three, four, five, six, seven]
# Define variable for framedelay, counters and the array of templates
framedelay = 0
backgroundCounter = False
templates = []

# loop through all templates found in the 'Templates' folder. Increases as more are added automatically
dirsize = len(os.listdir('Templates'))
for i in range(0, dirsize + 1):
    # template files must follow this naming convention, and a confirmation will be printed when a template is read
    template = cv2.imread('Templates/temp%s.jpg' % i, 0)
    print("read: temp%s.jpg" % i)
    templates.append(template)

while RUNNING:

    # read and show the video stream
    ret, image = cap.read()
    cv2.imshow('camera', image)
    # run the function to find the markers in the current frame
    wasps = 0
    warps, conts = findSquares(image)
    drawn = al.resize(image, height=300)
    temp_match_arr = []
    posList = []
    # loop through all contours, draw boundingboxes around them, find their center and add them to the list of positions
    for wa in warps:
        c = conts[wasps]
        wasps += 1
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(drawn, (x, y), (x + w, y + h), (0, 255, 0), 2)
        temp_match_arr.append(wa)
        center = al.Pos(x + (w / 2), y + (h / 2))
        posList.append(center)

    # loop through all the templates, warp them and do template matching. If the template matches, update the position
    # of the correlating player
    t = -1
    for template in templates:
        t += 1
        ma = 0
        for img in temp_match_arr:
            img = cv2.resize(img, (template.shape[1], template.shape[0]))
            rows, cols = img.shape
            for i in range(0, 4):
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90 * i, 1)
                dst = cv2.warpAffine(img, M, (cols, rows))
                if al.meanSquaredError(dst, template) < 6500:  # TODO: fine tune me
                    cv2.imshow("Found: " + str(t), al.resize(img, height=300))
                    playerList[t] = posList[ma]

            ma += 1
    # check if 30 frames have passed (~1 second) and send the positions to the server if it has
    if framedelay > 30:
        Client.send_pos(playerList)
        # reset the entries in playerList, the position-sending delay and the backgorund delay
        for derp in range(0, len(playerList)):
            playerList[derp].x = 0
            playerList[derp].y = 0
        framedelay = 0
        backgroundCounter = True

    else:
        framedelay += 1
    # bg_ch is currently hardcoded, but should be changed to be received from the server upon user request
    bg_ch = False  # send this as a message from server ("hey i updated map") Should probably run once regardless
    if bg_ch:  # if the request/variable is true: send the background and confirm the send
        cv2.imshow("Background", Client.recieve_bg())
        print("Background recieved from server")
    cv2.imshow("Ay", drawn)
    # if the pos has been sent, backgroundCounter == True, meaning a background will exist and the software won't crash
    if backgroundCounter:
        try:
            # read the recieved background and show it.
            background = cv2.imread('Maps/map_with_players.jpg')
            cv2.namedWindow('background', cv2.WINDOW_NORMAL)
            cv2.imshow('background', background)
        except AssertionError:
            print('assertion error')
    cv2.waitKey(1)

# show our images

# cv2.imshow("edge", edged)
cv2.waitKey(1)
