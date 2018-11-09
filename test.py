import cv2
import numpy as np  # import necessary libraries


def nothing(x):  # does nothing
    pass


def sort_p(alist):  # functions well, but sbould not be used
    it = 0  # iteration counter
    for i in alist:
        if it + 1 != len(alist):
            x, y = i.pos
            q, p = alist[it + 1].pos  # assign x and y positions from two pos next to each other in the list

            if y > p:  # if i.y is larger than alist[it+1].y, then swap their place (to sort the array)
                a = alist[it]
                b = alist[it + 1]
                alist[it] = b
                alist[it + 1] = a
            elif y == p and x > q:  # same for x, but y pos is checked first by IP, so naturally this only matters if they occupy the same y pos
                a = alist[it]
                b = alist[it + 1]
                alist[it] = b
                alist[it + 1] = a
        it += 1
    return alist  # return the sorted list


class PlayerToken:  # class to contain playtertoken objects, with name, colours and positions
    name = ""
    colour = (0, 0, 0)
    pos = (0, 0)


dennis = PlayerToken()
denice = PlayerToken()
detroit = PlayerToken()
playertokens = [dennis, denice, detroit]  # array of players
dennis.name = "R"
denice.name = "G"
detroit.name = "B"
dennis.colour = (0, 0, 255)
denice.colour = (0, 255, 0)
detroit.colour = (255, 0, 0)  # all "players" for testing created
cv2.namedWindow("sliders")  # next line references this window
cv2.createTrackbar('min_size', 'sliders', 0, 2000, nothing)  # create trackbar to change thresholding values in runtime
cap = cv2.VideoCapture(0)  # capture video from webcam
firstFrame = None
lastFrame = None
playing = True
movement_detected = False
frameDelay = 0

while playing:  # while True, should come with some exit statement in final edition (probably)
    if firstFrame is not None:
        lastFrame = frame  # if there has been a first frame, then this is the last frame (firstframe = lastframe, first iteration, as frame is only assigned again later in the loop)
    min_item_size = cv2.getTrackbarPos('min_size', 'sliders')  # variable to store threshold from trackbar window
    # Capture frame-by-frame
    ret, frame = cap.read()
    h, w, layers = frame.shape
    nh = int(h / 2)  # create halved h/w values from .shape on the newest frame
    nw = int(w / 2)
    # Frameoperations
    frame = cv2.resize(frame, (nw, nh))  # resize using the half values
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # make frame gray
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blur the frame with guassian
    if firstFrame is None:
        firstFrame = gray  # if this is the first frame, let it be so
        continue

    frameDelta = cv2.absdiff(firstFrame,
                             gray)  # check the difference between the first frame and gray(current frame). Different pixels will be white
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  # threshold the above delta frame

    thresh = cv2.dilate(thresh, None, iterations=2)  # dilate the frame

    conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)  # can change contour retrieval mode to find markers, it seems; can be replaced with new contouring code from alexandria
    conts = conts[1]  # don't remember wtf this does
    donts = []
    fonts = []
    for c in conts:  # go through all contours
        if cv2.contourArea(c) < min_item_size:  # if the contour is too small, ignore it
            continue
        donts.append(c)
    dd = 0  # counts iterations. Cuz fuck python
    if len(donts) < len(
            playertokens):  # if the contours not filtered out due to their size is less than the amount of tokens:
        movement_detected = True  # consider movement to be detected, to avoid further processing
    for d in donts:  # only go through the "real" contours (aka, not ignored ones)
        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(d)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        try:  # to catch errors
            q = int(x + (w / 2))  # find center values basede on bounding rectangels
            p = int(y + (h / 2))
            fonts.append((q, p))  # add the position of centers for each contours to "fonts"
            cp = playertokens[dd]  # current player
            if len(donts) == len(playertokens):  # if the amount of contours found is equal to the amount of players
                if movement_detected is False:  # and no movement has been detected
                    if cp.pos == (0, 0):  # why is blue never true (translated: shit doesn't work for some reason)
                        cp.pos = (
                        q, p)  # if the position is 0,0 (default, unused/unplaced) set the position to the found contour
                        continue  # and get out of the loop

            if (np.allclose(lastFrame, frame, 0, 225,
                            True)) is False:  # 225: threshold for movement detection; compare frames for differences
                frameDelay += 1  # if frames are the same, count them
                if frameDelay > 300:  # if more than 300 frames (5/10 seconds, don't remember, use fps counter) have been the same
                    print("Update")
                    movement_detected = False  # movement has not been detected / nothing new has been detected and pos can be updated
                    frameDelay = 0  # reset the frame counter
            else:
                frameDelay = 0  # if frames are not the same, reset the frame counter
                movement_detected = True  # and also something moved
        except IndexError:  # if it tries to compare contour #'s above playertokens[] #'s, it will get this error. This is fine
            frameDelay = 0  # reset counter, because we only want to detect players, everything else is considered "movement"
            movement_detected = True  # ^
        text = str(cp.name) + " " + str(cp.pos)
        cv2.circle(frame, cp.pos, 5, cp.colour,
                   -1)  # draw a circle in the center of the contour/on the player's position
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)  # put their name and position on the box
        dd += 1  # one iteration done, rinse and repeat
    ml = 0  # movement limiter; experimental
    if movement_detected is False and playertokens[len(playertokens) - 1].pos != (
    0, 0):  # don't bother running if all tokens do not have pos yet (because fuck b apparently)
        fcop = fonts.copy()
        for token in playertokens:
            #            fuckup = 0
            print(len(fcop))  # debug
            for f in fonts:  # go through every token and position
                if (token.pos[0] - 5 <= f[0] <= token.pos[0] + 5 and token.pos[1] - 5 <= f[1] <= token.pos[1]) is True:
                    fcop.remove(token.pos)  # remove matching positions from array

                else:
                    if len(
                            fcop) == 1:  # should make fuckup redundant, as 1 remaining position means only 1 changed pos remains
                        token.pos = fcop[0]
    #                    fuckup += 1
    #                   if fuckup >= len(playertokens): #3 fails, aka no fitting position
    #                        token.pos = fcop[0]

    # Display frame
    #  cv2.imshow('Thrash', thresh)
    #  cv2.imshow('Delta', frameDelta)
    cv2.imshow('First Frame', firstFrame)  # show old shit
    cv2.imshow('Frame', frame)  # show new shit
    # if lastFrame is not None:
    #     cv2.imshow('Prev Frame', lastFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        firstFrame = None  # if you press q, reset the first frame (comparison frame), to "update" in a sense

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
