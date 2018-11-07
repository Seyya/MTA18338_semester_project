import cv2
import numpy as np


def nothing(x):
    pass


def sort_p(alist):
    it = 0
    for i in alist:
        if it + 1 != len(alist):
            x, y = i.pos
            q, p = alist[it + 1].pos

            if y > p:
                a = alist[it]
                b = alist[it + 1]
                alist[it] = b
                alist[it + 1] = a
            elif y == p and x > q:
                a = alist[it]
                b = alist[it + 1]
                alist[it] = b
                alist[it + 1] = a
        it += 1
    return alist


class PlayerToken:
    name = ""
    colour = (0, 0, 0)
    pos = (0, 0)


dennis = PlayerToken()
denice = PlayerToken()
detroit = PlayerToken()
playertokens = [dennis, denice, detroit]  # største y -> mindste y
dennis.name = "R"
denice.name = "G"
detroit.name = "B"
dennis.colour = (0, 0, 255)
denice.colour = (0, 255, 0)
detroit.colour = (255, 0, 0)
cv2.namedWindow("sliders")
cv2.createTrackbar('min_size', 'sliders', 0, 2000, nothing)
cap = cv2.VideoCapture(0)
firstFrame = None
lastFrame = None
playing = True
movement_detected = False
frameDelay = 0

while playing:
    if firstFrame is not None:
        lastFrame = frame
    min_item_size = cv2.getTrackbarPos('min_size', 'sliders')
    # Capture frame-by-frame
    ret, frame = cap.read()
    h, w, layers = frame.shape
    nh = int(h / 2)
    nw = int(w / 2)
    # Frameoperations
    frame = cv2.resize(frame, (nw, nh))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)

    conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #can change contour retrieval mode to find markers, it seems
    conts = conts[1]
    donts = []
    fonts = []
    for c in conts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_item_size:
            continue
        donts.append(c)
    dd = 0  # cuz fuck python
    if len(donts) < len(playertokens):
        movement_detected = True
    for d in donts:  # only go through the "real" contours (aka, not ignored ones)
        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(d)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        try:
            q = int(x + (w / 2))
            p = int(y + (h / 2))
            fonts.append((q, p))
            cp = playertokens[dd]
            if len(donts) == len(playertokens):
                if movement_detected is False:
                    if cp.pos == (0, 0):  # why is blue never true
                        cp.pos = (q, p)
                        continue

            if (np.allclose(lastFrame, frame, 0, 225, True)) is False:  # 225 threshold for movement detection
                frameDelay += 1
                if frameDelay > 300:
                    print("Update")
                    movement_detected = False
                    frameDelay = 0
            else:
                frameDelay = 0
                movement_detected = True
        except IndexError:
            frameDelay = 0
            movement_detected = True
        text = str(cp.name) + " " + str(cp.pos)
        cv2.circle(frame, cp.pos, 5, cp.colour, -1)
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        dd += 1
    ml = 0  # movement limiter
    if movement_detected is False and playertokens[len(playertokens) - 1].pos != (
    0, 0):  # don't bother running if all tokens do not have pos yet (because fuck b apparently)
        fcop = fonts.copy()
        for token in playertokens:
            #            fuckup = 0
            print(len(fcop))
            for f in fonts:  # go through every token and position
                if (token.pos[0] - 5 <= f[0] <= token.pos[0] + 5 and token.pos[1] - 5 <= f[1] <= token.pos[1]) is True:
                    fcop.remove(token.pos)  # remove matching positions from array

                else:
                    if len(fcop) == 1:  # should make fuckup redundant
                        token.pos = fcop[0]
    #                    fuckup += 1
    #                   if fuckup >= len(playertokens): #3 fails, aka no fitting position
    #                        token.pos = fcop[0]

    # Display frame
    #  cv2.imshow('Thrash', thresh)
    #  cv2.imshow('Delta', frameDelta)
    cv2.imshow('First Frame', firstFrame)
    cv2.imshow('Frame', frame)
    # if lastFrame is not None:
    #     cv2.imshow('Prev Frame', lastFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        firstFrame = None

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
