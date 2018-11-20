import cv2

import alexandria as al


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


def find_corners(outline):  # corners matter, but not their individuality. No need to preserve
    setlist = list(outline)
    setlist = order_list(setlist)
    topright = al.Pos(setlist[0].x, setlist[0].y)  # right when rotated 45
    topleft = setlist[0]  # top when rotated 45
    bottomright = setlist[len(setlist) - 1]  # bot when roated 45
    bottomleft = al.Pos(setlist[0].x, setlist[0].y)

    for o in setlist:  # might wanna tangle this into the pos object from alexandria
        if o.y >= topright.y and o.x <= topright.x:
            topright.x = o.x
            topright.y = o.y
        if o.y <= bottomleft.y and o.x >= bottomleft.x:
            bottomleft.x = o.x
            bottomleft.y = o.y

    a = bottomleft.y + 1
    b = topleft.y
    if a == b:
        bottomleft = al.Pos(setlist[0].x, setlist[0].y)
        for o in setlist:
            if o.y <= bottomleft.y:
                bottomleft.x = o.x
                bottomleft.y = o.y
    #    print(o.place())
    return [topright, topleft, bottomright, bottomleft]


cap = cv2.VideoCapture(0)

while True:
    ret, image = cap.read()
    image = cv2.resize(image, (200, 200))
    image = al.rgb2grey(image)
    image = al.binary_threshold(image, 127)
    outlines = al.contouring(image, 0)
    for out in outlines:
        corners = find_corners(out)
        for c in corners:
            cv2.circle(image, c.place(), 2, 127, 5)

    cv2.imshow("Test 2", image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
