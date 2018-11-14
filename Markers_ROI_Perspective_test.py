import cv2
import numpy as np

import alexandria as al


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    if capture.isOpened():  # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:
        # important stuff starts here
        frame = cv2.resize(frame, (200, 200))
        gray = al.rgb2grey(frame)
        bina = al.binary_threshold(gray, 127)
        conts, outlines = al.contouring(bina, 0)
        twats = al.roi_boi(outlines, bina)
        cv2.approxPolyDP(twats, (0, 0))  # TODO fix approxpolydp. you have what you need. you cunt, git good
        # stops here

        cv2.imshow('Test Frame', conts)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
