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
    return cwoffset(prev - target) + target


def delete_old_cunts(x, y, l, b, tempi):
    for k in range(y, l + 1):
        for g in range(x, b + 1):
            tempi[k, g] = 255  # white, remember to change
    return tempi


def boundary_box(outline, src, tempi, bo):
    xarray = []
    yarray = []
    for j in outline:
        yarray.append(j.x)
        xarray.append(j.y)
    x = min(xarray)
    y = min(yarray)
    l = max(yarray)
    b = max(xarray)
    if bo is True:
        cv2.rectangle(src, (x, y), (b, l), 0, 2)  # black, remember to change
    tempi = delete_old_cunts(x, y, l, b, tempi)
    return tempi


# our god: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
# https://github.com/Dkendal/Moore-Neighbor_Contour_Tracer/blob/master/ContourTrace.cs
def contouring(img):  # lad den kalde igen og igen, men
    tempi = img.copy()
    moreblacks = True
    while moreblacks:
        onlyrealcuntshavecurves = True
        h, w = tempi.shape
        first = None
        outline = set()
        pixel_found = False
        for x in range(h):
            # something possibly missing here. Just hope it gives no issues. (It does if a pixel is found in the first pixel checked)
            if pixel_found:
                break
            for y in range(w):
                if tempi[x, y] == 0:  # black, remember to change
                    first = Pos(x, y)
                    pixel_found = True
                    break
                firstprev = Pos(x, y)
        if first is None:
            print("No white pixels found")
            moreblacks = False

        if pixel_found:
            prev = firstprev  # I know. But fuck you python :)
            outline.add(first)
            boundary = first
            curr = clockwise(boundary, prev)
            blackmanspotted = 0
            while (curr != first or prev != firstprev) and blackmanspotted <= 8:
                if w >= curr.y >= 0 and h >= curr.x >= 0 and tempi[curr.x, curr.y] == 0:  # black, remember to change
                    outline.add(curr)
                    prev = boundary
                    boundary = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted = 0
                else:
                    prev = curr
                    curr = clockwise(boundary, prev)
                    blackmanspotted += 1
            if blackmanspotted > 8:
                print("Your figures are incomplete you mongrel")
                onlyrealcuntshavecurves = False

            print(onlyrealcuntshavecurves)
            tempi = boundary_box(outline, img, tempi, onlyrealcuntshavecurves)
    return img