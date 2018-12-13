import cv2

import alexandria as al

fuck = al.binary_threshold(al.rgb2grey(cv2.resize(cv2.imread("test.png"), (300, 300))), 100)
cv2.imshow("bibo", fuck)
conts = al.contouring(fuck, False)
print(len(conts))

for cunt in conts:
    csi = 0
    for c in cunt:
        cv2.circle(fuck, c.place(), 2, 127, 1)
        csi += 1
cv2.imshow("lol", fuck)
cv2.waitKey(0)
