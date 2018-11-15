import math

import cv2

import alexandria as al


# finds the perpendicular distance between a line and a point
def range_finder(pt, a, b, c):  # abc for line equation: ax+by+c
    return abs((a * pt.x + b * pt.y + c)) / (math.sqrt(a * a + b * b))  # math


# finds a line function (or linear equation) ax + by + c
def line_finder(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


# functions requires a list of Pos objects, and a user defined epsilon
def square_maker3000(pts, epsilon):  # or: approxPoly_lineShape or RamerDouglasPeucker
    dmax = 0
    index = 0
    end = len(pts) - 1
    i = 0
    for pt in pts:
        i += 1
        a, b, c = line_finder(pts[0].x, pts[0].y, pts[end].x, pts[end].y)
        d = range_finder(pt, a, b, c)
        if d > dmax:  # only the last pts checked will submit to this
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

        result_list = recresults1, recresults2
    else:
        result_list = pts[0], pts[end]
    return result_list


# pts = [(0, 0), (0, 5), (5, 5), (6, 3), (5, 0)]
img = cv2.imread("marker_1383.png")
th = al.rgb2grey(img)
# bina = al.binary_threshold(grey, 127)
for o in outlines:
    o = list(o)
    o.sort(reverse=True)
    smol = square_maker3000(o, 1)
    for s in smol:
        cv2.circle(conts, s.place(), 5, 127, -1)

# pts = [al.Pos(0, 0), al.Pos(0, 5), al.Pos(5, 5), al.Pos(6, 3), al.Pos(5, 0)]
# print(pts)
# print(square_maker3000(pts, 3))
