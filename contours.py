import cv2
import numpy as np

image = cv2.imread("Untitled.png", 0)
h, w = image.shape

img = np.zeros((h, w), np.uint8)
for x in range(h):
    for y in range(w):
        if image[x, y] >= 250:
            img[x, y] = 255
        else:
            img[x, y] = 0


class Pos:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def place(self):
        return self.x, self.y

    def __add__(self, b):
        a = self
        return Pos(a.x + b.x, a.y + b.y)

    def __sub__(self, b):
        a = self
        return Pos(a.x - b.x, a.y - b.y)

    def __eq__(self, b):
        a = self
        return a.x == b.x and a.y == b.y

    # def __ne__(self, b):  # apparently only necessary in python 2 and not 3?
    #     a = self
    #     return not a == b

    def __hash__(self):
        return hash((self.x, self.y))


def cwoffset(point):  # check here  first for erros
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
    #   fix = prev - target
    #   fix = Pos(cwoffset(fix.place())[0], cwoffset(fix.place())[1])   # Botcher King
    return cwoffset(prev - target) + target


def boundary_box(outline):
    xarray = []
    yarray = []
    for j in outline:
        yarray.append(j.x)
        xarray.append(j.y)
    x = min(xarray)
    y = min(yarray)
    l = max(yarray)
    b = max(xarray)
    cv2.rectangle(img, (x, y), (b, l), (0, 0, 255), 2)


# our god: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
# https://github.com/Dkendal/Moore-Neighbor_Contour_Tracer/blob/master/ContourTrace.cs
def contouring(img):  # lad den kalde igen og igen, men
    h, w = img.shape
    first = None
    outline = set()
    pixel_found = False
    for x in range(h):
        # something possibly missing here. Just hope it gives no issues. (It does if a pixel is found in the first pixel checked)
        if pixel_found:
            break
        for y in range(w):
            if img[x, y] == 0:  # replace 0 with True once binary function is fixed?
                first = Pos(x, y)
                pixel_found = True
                break
            firstprev = Pos(x, y)
    if first is None:
        print("No black pixels found")

    if pixel_found:
        prev = firstprev  # I know. But fuck you python :)
        outline.add(first)
        boundary = first
        curr = clockwise(boundary, prev)
        while curr != first or prev != firstprev:
            if w >= curr.y >= 0 and h >= curr.x >= 0 and img[curr.x, curr.y] == 0:

                outline.add(curr)
                prev = boundary
                boundary = curr
                curr = clockwise(boundary, prev)
            else:
                prev = curr
                curr = clockwise(boundary, prev)
        boundary_box(outline)
    return img


cv2.imshow("twat", contouring(img))
cv2.waitKey(0)
