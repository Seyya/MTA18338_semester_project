import cv2

import alexandria as al


def find_corners(contour):
    topright = 0, 0
    topleft = 0, 0
    bottomright = 0, 0
    bottomleft = 0, 0

    for c in contour:
        if c.x == (0, 0):
            print("")
    return


image = cv2.imread("marker_1265.png")
image = al.rgb2grey(image)
image = al.binary_threshold(image, 127)
al.contouring(image, 0)

cv2.imshow("Test", image)
cv2.waitKey(0)


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
