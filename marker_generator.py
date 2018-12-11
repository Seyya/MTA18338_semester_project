# Generates a marker
# maybe using Hamming coding
# if I am that smart (I'm not)

import numpy as np
import cv2
from scipy import ndimage


def generate_image(MARKER_SIZE=7):
    # creates a 7x7 marker by default. the marker has a black border all the way around the "code"
    # which is a randomly generated selection of binary pixels, not an actual code (so far)
    # on the inside of the border, the upper left corner is white and the other corners are black
    # this is to help with orientation and to ensure identical-but-mirrored markers cant be confused with each other
    # accepts an optional parameter to adjust the size of the marker to e.g. 9x9. remember that 2 squares go to
    # the border, so a 7x7 marker has a code of 5x5
    img = np.zeros((MARKER_SIZE, MARKER_SIZE), int)
    img[1:MARKER_SIZE - 1, 1:MARKER_SIZE - 1] = np.random.randint(0, 2, [MARKER_SIZE - 2, MARKER_SIZE - 2]) * 255
    img[1, 1] = 255  # set the orientation marker
    img[1, MARKER_SIZE - 2] = 0  # set the other three corners to black
    img[MARKER_SIZE - 2, MARKER_SIZE - 2] = 0
    img[MARKER_SIZE - 2, 1] = 0
    # if you want to adjust the image size (not the marker itself i.e. how many squares there are) adjust the zoom
    return ndimage.zoom(img, zoom=12, order=0)


# want to save the markers individually instead of just overwriting them? change the file name each time
cv2.imwrite('marker_test.png', generate_image())
print('Done!')
