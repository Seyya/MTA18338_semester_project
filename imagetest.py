import cv2

import alexandria as al

fuck = al.binary_threshold(al.rgb2grey(cv2.imread("test4_template_test.png")), 200)
conts = al.contouring(fuck, False)

for cunt in conts:
    csi = 0
    for c in cunt:
        cv2.circle(fuck, c.place(), 2, 127, 1)
        csi += 1
cv2.imshow("lol", fuck)
cv2.waitKey(0)
